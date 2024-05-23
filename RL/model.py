import torch
import threading
from RL.util import extract_features

def compiler_hook(message_dict, response_fn):
    client = message_dict['client']
    general_features, block_features, subloop_features = extract_features(message_dict)
    # TODO: feed block features and subloop features    
    
    # print(f"{client} : {threading.get_ident()}")
    
    response_fn(2)