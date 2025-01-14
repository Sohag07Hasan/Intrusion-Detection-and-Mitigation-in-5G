import os
import random
import pandas as pd
import numpy as np
from scapy.all import *
from collections import defaultdict
from datetime import datetime
import pickle
import time
import pdb
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

#importing API functions
#from utils import CoreNetworkAPI
from utils import monitor_attacks, create_mapping_data, delete_files, monitor_attacks_based_on_time, should_write_features_now


#FLOW_DURATION = 1 #seconds
PCKT_NUMBER = 5
UDP_DURATION = 400 #seconds
LABEL = ""

DIR_PATH = "./pcaps/benign/"
MIN_PCKT = 2
OVERLAP = False
INTERFACE = "eth2"

STATE_SIZE = 5
ACTION_SIZE = 3


##ML Variables
#scaller_save_path = "./scaler_k_3_n_5_f_55.pkl"
model_save_path = f"./rf_models/RF_model_k_{PCKT_NUMBER}_n_5_f_55_no_overlap_iperf.pkl"
#path_of_pth_file = "./rl_models/RL_5GNIDD/model_50000_3.pth" #5GNIDD
path_of_pth_file = "./rl_models/model_500000_1002.pth" #INSDN



if OVERLAP:    
    DATASET_PATH = "./overlap_dataset_"+str(PCKT_NUMBER)+".csv"
else:
    DATASET_PATH = "./dataset_"+str(PCKT_NUMBER)+".csv"

PCKT_CONTAINER = {}   # { flow_id: [pckt_list]  }
TIMESTAMP = {}        # {flow_id: timestamp }
#FLOW_TIME = {}        # {flow_id: timestamp}
FLOW_COUNTER = {}     # {flow_id: counter}
SUB_FLOW_COUNTER = {} # {flow_id: counter}
FEATURES = []         # [{ flow_id, protocol, bytes_received in last 1s
                      # packet received in last 1s, avg pckt size in last 1s, Label}]
GRACEFUL_TRACKER = {} # {flow_id: FIN_COUNT} # if FIN count is 2, then TCP session is terminated gracefully


def process_pcap(pkt, file_id = "id"):
    #print(f"Opening {fpath}")

    global FEATURES, PCKT_CONTAINER, FLOW_COUNTER, TIMESTAMP, SUB_FLOW_COUNTER
    layers = pkt.layers()
    #import pdb;pdb.set_trace()
    if type(IP()) in layers: 
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        protocol = str(pkt[IP].proto)
        try:
            if protocol=="6" or protocol=="17" or protocol=="1": # TCP(6), UDP(17), ICMP(1)
                if protocol == "1":
                    sport = str(0)
                    dport = str(0)
                else:
                    sport = str(pkt[IP].sport)
                    dport = str(pkt[IP].dport)
            else:
                return
        except Exception as ex:
            print("Exception")
            return

        fwd_id = src_ip+"_"+dst_ip+"_"+sport+"_"+dport+"_"+protocol
        bwd_id = dst_ip+"_"+src_ip+"_"+dport+"_"+sport+"_"+protocol

        if fwd_id in PCKT_CONTAINER.keys():
            check_flow_termination(pkt, fwd_id, protocol, file_id)
            #calculate_features(pkt, fwd_id, protocol)
        elif bwd_id in PCKT_CONTAINER.keys():
            check_flow_termination(pkt, bwd_id, protocol, file_id)
            #calculate_features(pkt, bwd_id, protocol)
        else:
            if fwd_id in FLOW_COUNTER.keys():
                PCKT_CONTAINER[fwd_id] = [pkt]
                TIMESTAMP[fwd_id] = pkt.time
            elif bwd_id in FLOW_COUNTER.keys():
                PCKT_CONTAINER[bwd_id] = [pkt]
                TIMESTAMP[bwd_id] = pkt.time
            else:
                FLOW_COUNTER[fwd_id] = 1
                SUB_FLOW_COUNTER[fwd_id] = 1
                PCKT_CONTAINER[fwd_id] = [pkt]
                TIMESTAMP[fwd_id] = pkt.time

    #if len(FEATURES) >= 100:
    if should_write_features_now():
        save_features()
        # empty the global variables
        PCKT_CONTAINER = {}   # { flow_id: [pckt_list]  }
        TIMESTAMP = {}        # {flow_id: timestamp }
        #FLOW_TIME = {}        # {flow_id: timestamp}
        FLOW_COUNTER = {}
        SUB_FLOW_COUNTER = {}
        FEATURES = []         # [{ flow_id, protocol, bytes_received in last 1s

# Load Scaller Modesl
#with open(scaller_save_path, 'rb') as f:
#    loaded_scaler = pickle.load(f)

# Load RF Models
with open(model_save_path, 'rb') as f:
    loaded_model = pickle.load(f)

# class DQN(nn.Module):
#     def __init__(self, state_size, action_size):
#         super(DQN, self).__init__()
#         self.fc1 = nn.Linear(state_size*101, 512)
#         self.fc2 = nn.Linear(512, 256)
#         self.fc3 = nn.Linear(256, 128)
#         self.fc4 = nn.Linear(128, 64) 
#         self.fc5 = nn.Linear(64, action_size)

#     def forward(self, x): 
#         x = F.relu(self.fc1(x.flatten()))
#         x = F.relu(self.fc2(x))
#         x = F.relu(self.fc3(x))
#         x = F.relu(self.fc4(x))
#         return self.fc5(x)

class DQN(nn.Module):
    def __init__(self, state_size, action_size, dropout_prob=0.3):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size*101, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 64) 
        self.fc5 = nn.Linear(64, action_size)
    
        # Define dropout layers with the specified probability
        self.dropout = nn.Dropout(p=dropout_prob)

    def forward(self, x): 
        x = F.relu(self.fc1(x.flatten()))
        x = self.dropout(x)  # Apply dropout after activation
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.relu(self.fc3(x))
        x = self.dropout(x)
        x = F.relu(self.fc4(x))
        x = self.dropout(x)
        return self.fc5(x)


rl_model = DQN(STATE_SIZE, ACTION_SIZE)
#rl_model.load_state_dict(torch.load(path_of_pth_file))
rl_model.load_state_dict(torch.load(path_of_pth_file, map_location=torch.device('cpu')))
rl_model.eval()

STATE = {}
STATE_COUNTER = {}



def save_features():
    # saving features to file here to avoid overflow of memory
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH) 
        df2 = pd.DataFrame(FEATURES)
        df = pd.concat([df,df2], axis=0, join='outer') # doing append using concat method
        df.to_csv(DATASET_PATH, index=False)
    else:
        df = pd.DataFrame(FEATURES)
        df.to_csv(DATASET_PATH, index=False)



def check_flow_termination(pkt, flow_id, protocol, file_id):
    if len(PCKT_CONTAINER[flow_id])<PCKT_NUMBER: # flow duration is not complete
        PCKT_CONTAINER[flow_id].append(pkt)
        #print("appending")
    
    else: # pckt count is complete
        calc_features(PCKT_CONTAINER[flow_id], flow_id, protocol, file_id)
        SUB_FLOW_COUNTER[flow_id] += 1
        if OVERLAP:
            PCKT_CONTAINER[flow_id].pop(0)
        else:
            del PCKT_CONTAINER[flow_id]
        return


    if protocol == "6": # check for TCP
        FLAGS = pkt['TCP'].flags
        # abrupt termination
        RST = 0x04
        if (FLAGS & RST):
            calc_features(PCKT_CONTAINER[flow_id], flow_id, protocol, file_id)
            FLOW_COUNTER[flow_id] += 1
            SUB_FLOW_COUNTER[flow_id] = 1
            del PCKT_CONTAINER[flow_id]

        # graceful termination
        FIN = 0x01
        if (FLAGS & FIN): # FIN activated
            if flow_id in GRACEFUL_TRACKER.keys():
                # flow is terminated
                del GRACEFUL_TRACKER[flow_id]
                calc_features(PCKT_CONTAINER[flow_id], flow_id, protocol, file_id)
                FLOW_COUNTER[flow_id] += 1
                SUB_FLOW_COUNTER[flow_id] = 1
                del PCKT_CONTAINER[flow_id]

            else:
                GRACEFUL_TRACKER[flow_id] = 1

    elif protocol == "17": # check flow duration for UDP
        current_time = pkt.time
        duration = current_time - TIMESTAMP[flow_id]
        if duration >= UDP_DURATION:
            calc_features(PCKT_CONTAINER[flow_id], flow_id, protocol, file_id)
            FLOW_COUNTER[flow_id] += 1
            SUB_FLOW_COUNTER[flow_id] = 1
            del PCKT_CONTAINER[flow_id]
            #del FLOW_TIME[flow_id]


def predict_attack(features, flow_id):
    state_size = STATE_SIZE  # highest 5 subflows
    action_size = ACTION_SIZE  # wait, attack, benign

    df = pd.DataFrame([features])
    df_encoded = pd.get_dummies(df, columns=['protocol'], prefix='protocol')

    for protocol in [1, 6, 17]:
        column_name = f'protocol_{protocol}'
        if column_name not in df_encoded.columns:
            df_encoded[column_name] = 0
        else:
            df_encoded[column_name] = df_encoded[column_name].astype(int)  # Avoid True and False

    df_encoded = df_encoded[['protocol_17', 'protocol_6', 'protocol_1', 'flow_duration', 'tot_fwd_pkt', 'tot_fwd_pkt_len', 'fwd_pkt_len_mean',
                             'pkt_per_second', 'byte_per_second', 'iat_mean', 'iat_std']]

    transformed_features = df_encoded.values.astype(float)
    prediction = loaded_model.predict(transformed_features)
    if prediction[0] == 0:
        rf_prediction = 'Attack'
        #print(f"RF prediction: Attack")
    else:
        rf_prediction = 'Benign'
        #print(f"RF prediction: Benign")
    if flow_id in STATE.keys():
        tree_counter = np.zeros(101, dtype=int)
        tree_counter[-1] = PCKT_NUMBER
        for i, tree in enumerate(loaded_model.estimators_):
            tree_counter[i] = tree.predict(transformed_features)[0]  # Extract single element
        STATE[flow_id][STATE_COUNTER[flow_id]] = tree_counter

        # import pdb;pdb.set_trace()
       
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
        #import pdb;pdb.set_trace()
        STATE[flow_id] = -1 * np.ones((state_size, 101), dtype=int)
        STATE_COUNTER[flow_id] = 0

        tree_counter = np.zeros(101, dtype=int)
        tree_counter[-1] = PCKT_NUMBER
        for i, tree in enumerate(loaded_model.estimators_):
            tree_counter[i] = tree.predict(transformed_features)[0]  # Extract single element
        STATE[flow_id][STATE_COUNTER[flow_id]] = tree_counter
       
       # Convert NumPy array to PyTorch tensor
        state_tensor = torch.tensor(STATE[flow_id], dtype=torch.float32)
        
        with torch.no_grad():
            q_values = rl_model(state_tensor)
        action = np.argmax(q_values.cpu().data.numpy())

        STATE_COUNTER[flow_id] += 1

    return action, rf_prediction



def calc_features(pkt_list, flow_id, protocol, file_id):
#    print(f"Calculating Features for {flow_id}")
    if len(pkt_list)>MIN_PCKT:
        # src_ip_dst_ip_src_port_dst_port_protocol_flow_counter_subflow_counter_file_id
        f_id_to_save = flow_id + "_" + str(FLOW_COUNTER[flow_id]) + "_" + str(SUB_FLOW_COUNTER[flow_id]) + "_" +file_id
        feat_dict = {"flow_id": f_id_to_save, "protocol": int(protocol)}

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


        prediction, rf_prediction = predict_attack(feat_dict, flow_id)

        if prediction == 0:
            rl_prediction = "Wait"
            #print("RL prediction: Wait")
        elif prediction == 1:
            rl_prediction = "Attack"
            #print("RL prediction: Attack")
            #print("Throttle the malicious IP")
            #monitor_attacks(flow_id)
            monitor_attacks_based_on_time(flow_id)
        elif prediction == 2:
            rl_prediction = "Benign"
            #print("RL prediction: Benign")
        else:
            #print("Unknown prediciton from RL agent")
            pass

        #print (f"Attack Detected: {f_id_to_save}")

        feat_dict["flow_id"] = f_id_to_save

        feat_dict["RL_label"] = rl_prediction
        feat_dict["RF_label"] = rf_prediction

        #print(feat_dict)
        FEATURES.append(feat_dict)


def calc_flow_features(pkt_list, flow_duration):
    pkt_per_second = flow_duration/len(pkt_list)

    pkt_byte = 0
    iat = []
    for i, pkt in enumerate(pkt_list):
        pkt_byte += len(pkt)
        if i==0:
            iat.append(0)
            prev_time = pkt.time
        else:
            iat.append(float(pkt.time-prev_time))
            prev_time = pkt.time
    byte_per_second = flow_duration/pkt_byte
    iat_mean = np.mean(iat)
    iat_std = np.std(iat)

    return pkt_per_second, byte_per_second, iat_mean, iat_std


def calc_fwd_pkt_features(pkt_list, flow_id):
    src_ip = flow_id.split("_")[0]
    fwd_pkt_count = 0
    fwd_pkt_len = 0
    count = 0
    fwd_pkt_len_mean = []
    for pkt in pkt_list:
        if pkt[IP].src == src_ip:
            count += 1
            fwd_pkt_count += 1
            fwd_pkt_len += len(pkt)
            fwd_pkt_len_mean.append(len(pkt))
    if count==0:
        return 0, 0, 0
    else:
        return fwd_pkt_count, fwd_pkt_len, np.mean(fwd_pkt_len_mean)


##This function will initialize IDS systems
def initialize_ids():
    print('initializeing IDS')      
    file_list = [
        './mapping_data.txt',
        './attack_records.csv',
        DATASET_PATH
    ]
    delete_files(file_list=file_list)
    create_mapping_data(mapping_data="mapping_data.txt")


if __name__ == "__main__":
    if INTERFACE is None:
        filenames = os.listdir(DIR_PATH)

        for i, fname in tqdm(enumerate(filenames)):
            cap = PcapNgReader(DIR_PATH+fname)
            for pkt in cap:
                process_pcap(pkt, str(i))
            # save the rest of the features once all the pckts are traversed
            for f_id in list(PCKT_CONTAINER.keys()):
                protocol = f_id.split("_")[-1]
                calc_features(PCKT_CONTAINER[f_id], f_id, protocol, str(i))
                SUB_FLOW_COUNTER[f_id] += 1

            #save_features()

            # empty the global variables
            PCKT_CONTAINER = {}   # { flow_id: [pckt_list]  }
            TIMESTAMP = {}        # {flow_id: timestamp }
            #FLOW_TIME = {}        # {flow_id: timestamp}
            FLOW_COUNTER = {}
            SUB_FLOW_COUNTER = {}
            FEATURES = []         # [{ flow_id, protocol, bytes_received in last 1s
    else:
        print('initializeing IDS')
        initialize_ids()
        print(f"Starting packet capture on interface {INTERFACE}")
        sniff(iface=INTERFACE, prn=process_pcap, store=False)
