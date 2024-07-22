import os
import random
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import deque

state_size = 5 # highest 5 subflows
action_size = 3 # wait, attack, benign

rf_model_path = ""
rf_scaler_path = ""
path_of_pth_file = ""

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


model = DQN(state_size, action_size)
model.load_state_dict(torch.load(path_of_pth_file))
model.eval()


with open(rf_model_path, 'rb') as f:
    rf_model = pickle.load(f)

with open(rf_scaler_path, 'rb') as f:
    scaler = pickle.load(f)


# for each subflow features
state = -1 * np.ones((state_size, 100), dtype=int)
data = scaler.transform(array.reshape(1,-1))


tree_counter = np.zeros(100, dtype=int)
for i,tree in enumerate(rf_model.estimators_):
    tree_counter[i] = tree.predict(data)

state[sub_flow_num] = tree_counter

with torch.no_grad():
    q_values = model(state)

# 0 means wait, 1 means attack, 2 means benign
action = np.argmax(q_values.cpu().data.numpy())
