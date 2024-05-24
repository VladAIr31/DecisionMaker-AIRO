import torch

def extract_block_features(block):
    return [
        block.get('numArith', 0),
        block.get('numBranches', 0),
        block.get('numCalls', 0),
        block.get('numInstructions', 0),
        block.get('numLoads', 0),
        block.get('numPHINodes', 0),
        block.get('numPredecessors', 0),
        block.get('numStores', 0),
        block.get('numSuccessors', 0)
    ]

def extract_general_features(data):
    return [
        data.get('depth', 0),
        data['header'].get('numArith', 0),
        data['header'].get('numBranches', 0),
        data['header'].get('numCalls', 0),
        data['header'].get('numInstructions', 0),
        data['header'].get('numLoads', 0),
        data['header'].get('numPHINodes', 0),
        data['header'].get('numStores', 0),
        int(data.get('isInnermost', False)),
        int(data.get('isRotatedForm', False)),
        data['latch'].get('numArith', 0),
        data['latch'].get('numBranches', 0),
        data['latch'].get('numCalls', 0),
        data['latch'].get('numInstructions', 0),
        data['latch'].get('numLoads', 0),
        data['latch'].get('numPHINodes', 0),
        data['latch'].get('numStores', 0),
        data.get('numBackEdges', 0),
        data.get('numBlocks', 0),
        data.get('numExitBlocks', 0)
    ]

def extract_subloop_features(subloops):
    features = []
    if subloops:
        for subloop in subloops:
            features.extend([
                subloop.get('depth', 0),
                int(subloop.get('isInnermost', False)),
                subloop.get('numBlocks', 0),
                subloop.get('numSubLoops', 0)
            ])
    return features

def extract_features(data):
    block_features = []
    if data.get('blocks'):
        for block in data['blocks']:
            block_features.append(extract_block_features(block))

    general_features = extract_general_features(data)
    subloop_features = extract_subloop_features(data.get('subloops', []))

    block_tensor = torch.tensor(block_features, dtype=torch.float32)
    general_tensor = torch.tensor(general_features, dtype=torch.float32)
    subloop_tensor = torch.tensor(subloop_features, dtype=torch.float32)
    
    return general_tensor, block_tensor, subloop_tensor
