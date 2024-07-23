
## Extract Features
## Scaling
### Infernece
### Saving

import os
import random
import pandas as pd
import numpy as np
from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
from datetime import datetime
import pickle
import time
from collections import Counter
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm


import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import deque

##importing API functions
from utils import release_pdu, change_throughput, update_file

###ML Variables
scaller_save_path = "./ml_models/scalers_5gnidd/scalers/scaler_k_3_n_1_f_11.pkl"
model_save_path = "./ml_models/models_5gnidd/models/RF_model_k_3_n_1_f_11.pkl"
path_of_pth_file = "./rl_models/RL_5GNIDD/model_50000_3.pth" #5GNIDD
#path_of_pth_file = "./rl_modesl/RL_InSDN/model_50000_3.pth" #INSDN


##Flow Control Variables
PCKT_NUMBER = 3
UDP_DURATION = 400  # seconds not in use
LABEL = "attack"
INTERFACE = "eth2"  # Interface connected with upf
MIN_PCKT = 2
OVERLAP = True

STATE_SIZE = 5 # highest 5 subflows
ACTION_SIZE = 3 # wait, attack, benign

if OVERLAP:
    DATASET_PATH = "./overlap_dataset_live.csv"
else:
    DATASET_PATH = "./dataset_live.csv"

PCKT_CONTAINER = defaultdict(list)  # { flow_id: [pckt_list] }
TIMESTAMP = {}  # {flow_id: timestamp}
FLOW_COUNTER = defaultdict(int)  # {flow_id: counter}
SUB_FLOW_COUNTER = defaultdict(int)  # {flow_id: counter}
FEATURES = []  # [{ flow_id, protocol, bytes_received in last 1s, packet received in last 1s, avg pckt size in last 1s, Label}]
GRACEFUL_TRACKER = {}  # {flow_id: FIN_COUNT} # if FIN count is 2, then TCP session is terminated gracefully


def packet_callback(pkt):
    global FEATURES, PCKT_CONTAINER, FLOW_COUNTER, TIMESTAMP, SUB_FLOW_COUNTER

    if IP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        protocol = pkt[IP].proto
        sport = pkt[TCP].sport if TCP in pkt else pkt[UDP].sport if UDP in pkt else 0
        dport = pkt[TCP].dport if TCP in pkt else pkt[UDP].dport if UDP in pkt else 0

        flow_id = f"{src_ip}_{dst_ip}_{sport}_{dport}_{protocol}"
        rev_flow_id = f"{dst_ip}_{src_ip}_{dport}_{sport}_{protocol}"

        if flow_id in PCKT_CONTAINER or rev_flow_id in PCKT_CONTAINER:
            active_flow_id = flow_id if flow_id in PCKT_CONTAINER else rev_flow_id
            PCKT_CONTAINER[active_flow_id].append(pkt)
            if len(PCKT_CONTAINER[active_flow_id]) >= PCKT_NUMBER:
                calc_features_and_run_ids(PCKT_CONTAINER[active_flow_id], active_flow_id, protocol)
                SUB_FLOW_COUNTER[active_flow_id] += 1
                if OVERLAP:
                    PCKT_CONTAINER[active_flow_id].pop(0)
                else:
                    del PCKT_CONTAINER[active_flow_id]
        else:
            PCKT_CONTAINER[flow_id].append(pkt)
            TIMESTAMP[flow_id] = pkt.time
            FLOW_COUNTER[flow_id] += 1
            SUB_FLOW_COUNTER[flow_id] += 1

    if len(FEATURES) >= 100:
        save_features()


## Load Scaller Modesl
with open(scaller_save_path, 'rb') as f:
    loaded_scaler = pickle.load(f)

## Load RF Models
with open(model_save_path, 'rb') as f:
    loaded_model = pickle.load(f)

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size*100, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 64) 
        self.fc5 = nn.Linear(64, action_size)

    def forward(self, x): 
        x = F.relu(self.fc1(x.flatten()))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        return self.fc5(x)


rl_model = DQN(STATE_SIZE, ACTION_SIZE)
#rl_model.load_state_dict(torch.load(path_of_pth_file))
rl_model.load_state_dict(torch.load(path_of_pth_file, map_location=torch.device('cpu')))
rl_model.eval()

STATE = {}
STATE_COUNTER = {}



def predict_attack(features, flow_id):
    state_size = STATE_SIZE  # highest 5 subflows
    action_size = ACTION_SIZE  # wait, attack, benign

    df = pd.DataFrame([features])
    df_encoded = pd.get_dummies(df, columns=['protocol'], prefix='protocol')

    for protocol in [1, 6, 17]:
        column_name = f'protocol_{protocol}'
        if column_name not in df_encoded.columns:
            df_encoded[column_name] = 0

    df_encoded = df_encoded.astype(int)  # Avoid True and False

    df_encoded = df_encoded[['protocol_17', 'protocol_6', 'protocol_1', 'flow_duration', 'tot_fwd_pkt', 'tot_fwd_pkt_len', 'fwd_pkt_len_mean',
                             'pkt_per_second', 'byte_per_second', 'iat_mean', 'iat_std']]

    transformed_features = loaded_scaler.transform(df_encoded.values)
    prediction = loaded_model.predict(transformed_features)
    print(f"RF prediction: {prediction[0]}")

    if flow_id in STATE.keys():

        tree_counter = np.zeros(100, dtype=int)
        for i, tree in enumerate(loaded_model.estimators_):
            tree_counter[i] = tree.predict(transformed_features)[0]  # Extract single element
        STATE[flow_id][STATE_COUNTER[flow_id]] = tree_counter
        
        # Convert NumPy array to PyTorch tensor
        state_tensor = torch.tensor(STATE[flow_id], dtype=torch.float32)
        
        with torch.no_grad():
            q_values = rl_model(state_tensor)
        action = np.argmax(q_values.cpu().data.numpy())

        STATE_COUNTER[flow_id] += 1
        if STATE_COUNTER[flow_id] >= state_size:
            del STATE[flow_id]
            del STATE_COUNTER[flow_id]

    else:
        STATE[flow_id] = -1 * np.ones((state_size, 100), dtype=int)
        STATE_COUNTER[flow_id] = 0

        tree_counter = np.zeros(100, dtype=int)
        for i, tree in enumerate(loaded_model.estimators_):
            tree_counter[i] = tree.predict(transformed_features)[0]  # Extract single element
        STATE[flow_id][STATE_COUNTER[flow_id]] = tree_counter
        
        # Convert NumPy array to PyTorch tensor
        state_tensor = torch.tensor(STATE[flow_id], dtype=torch.float32)
        
        with torch.no_grad():
            q_values = rl_model(state_tensor)
        action = np.argmax(q_values.cpu().data.numpy())

        STATE_COUNTER[flow_id] += 1

    return action



def calc_features_and_run_ids(pkt_list, flow_id, protocol):
    if len(pkt_list) > MIN_PCKT:
        f_id_to_save = f"{flow_id}_{FLOW_COUNTER[flow_id]}_{SUB_FLOW_COUNTER[flow_id]}"

        #feat_dict = {"flow_id": f_id_to_save, "protocol": protocol}
        feat_dict = {"protocol": protocol}

        flow_duration = pkt_list[-1].time - TIMESTAMP[flow_id]
        feat_dict["flow_duration"] = float(flow_duration)

        fwd_pkt_features = calc_fwd_pkt_features(pkt_list, flow_id)
        feat_dict["tot_fwd_pkt"] = fwd_pkt_features[0]
        feat_dict["tot_fwd_pkt_len"] = fwd_pkt_features[1]
        feat_dict["fwd_pkt_len_mean"] = fwd_pkt_features[2]

        flow_features = calc_flow_features(pkt_list, flow_duration)
        feat_dict["pkt_per_second"] = flow_features[0]
        feat_dict["byte_per_second"] = flow_features[1]
        feat_dict["iat_mean"] = flow_features[2]
        feat_dict["iat_std"] = flow_features[3]

        prediction = predict_attack(feat_dict, flow_id)

        if prediction == 0:
            print("RL prediction: Wait")
        elif prediction == 1:
            print("RL prediction: Attack")
            print("Throttle the malicious IP")
            change_throughput("10.61.0.3")
        elif prediction == 2:
            print("RL prediction: Benign")
        else:
            print("Unknown prediciton from RL agent")

        #print (f"Attack Detected: {f_id_to_save}")

        feat_dict["flow_id"] = f_id_to_save
        feat_dict["label"] = prediction #LABEL is for using for Traffic
        FEATURES.append(feat_dict)



def calc_flow_features(pkt_list, flow_duration):
    pkt_per_second = len(pkt_list) / flow_duration if flow_duration > 0 else 0
    pkt_byte = sum(len(pkt) for pkt in pkt_list)
    byte_per_second = pkt_byte / flow_duration if flow_duration > 0 else 0

    iat = [pkt_list[i].time - pkt_list[i - 1].time for i in range(1, len(pkt_list))]
    iat_mean = np.mean(iat) if iat else 0
    iat_std = np.std(iat) if iat else 0

    return pkt_per_second, byte_per_second, iat_mean, iat_std


def calc_fwd_pkt_features(pkt_list, flow_id):
    src_ip = flow_id.split("_")[0]
    fwd_pkt_count = sum(1 for pkt in pkt_list if pkt[IP].src == src_ip)
    fwd_pkt_len = sum(len(pkt) for pkt in pkt_list if pkt[IP].src == src_ip)
    fwd_pkt_len_mean = np.mean([len(pkt) for pkt in pkt_list if pkt[IP].src == src_ip]) if fwd_pkt_count > 0 else 0

    return fwd_pkt_count, fwd_pkt_len, fwd_pkt_len_mean


def save_features():
    global FEATURES
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        df2 = pd.DataFrame(FEATURES)
        df = pd.concat([df, df2], axis=0, join='outer')  # doing append using concat method
        df.to_csv(DATASET_PATH, index=False)
    else:
        df = pd.DataFrame(FEATURES)
        df.to_csv(DATASET_PATH, index=False)
    FEATURES = []


if __name__ == "__main__":
    print(f"Starting packet capture on interface {INTERFACE}")
    sniff(iface=INTERFACE, prn=packet_callback, store=False)