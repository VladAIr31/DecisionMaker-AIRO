import torch
from RL.util import extract_features

def compiler_hook(message_dict):
    general_features, block_features, subloop_features  = extract_features(message_dict)
    # print(general_features.shape,block_features.shape,subloop_features)
    print(general_features)