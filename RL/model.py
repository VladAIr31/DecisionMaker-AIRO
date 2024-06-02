import torch
import torch.nn as nn
import torch.optim as optim
from RL.util import extract_features

class SimpleModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(input_size, output_size)
    
    def forward(self, x):
        return self.fc(x)

class ModelManager:
    def __init__(self, model, optimizer):
        self.model = model
        self.optimizer = optimizer
        self.prediction_history = []

    # State is called for all the memmbers of the 'game'
    def state(self, state_dict, response_fn):
        general_features, _, _ = extract_features(state_dict)
        self.model.train()
        output_tensor = self.model(general_features)
        output_tensor = torch.clamp(output_tensor, min=1, max=100)
        output = int(output_tensor.item())
        with open("outputs",'a') as f:
            f.write(f"{output}\n")
        # print(f"Output {output}")
        self.prediction_history.append(output_tensor)
        response_fn(output)
        # response_fn(1)
    
    # At the end of the game a penalty is given for the game, the model should minimze said penalty
    def evaluate_run(self, penalty):
        print(f"Penalty {penalty}")
        self.model.train()
        for prediction in self.prediction_history:
            self.optimizer.zero_grad()
            loss = penalty * prediction / torch.sum(prediction)
            loss.backward()
            # Gradient clipping
            self.optimizer.step()
        self.prediction_history = []

input_size = 20
output_size = 1
model = SimpleModel(input_size, output_size)
optimizer = optim.SGD(model.parameters(), lr=0.01)

MM = ModelManager(model, optimizer)
