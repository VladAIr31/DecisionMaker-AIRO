import torch
import threading
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from RL.util import extract_features

class SimpleModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class ModelManager:
    def __init__(self, model, lr=1e-3):
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.lock = threading.Lock()
        self.data_series = []
        self.outputs = []
        self.performance_feedback = []

    def feed_data(self, data):
        with self.lock:
            self.data_series.append(data)
            output = self.model(data)
            # Clamp the output to ensure it is at least 1
            output = torch.clamp(output, min=1)
            self.outputs.append(output)
            return output.item()

    def receive_feedback(self, feedback):
        with self.lock:
            self.performance_feedback.append(feedback)
            self.update_model()

    def update_model(self):
        self.optimizer.zero_grad()
        total_loss = torch.tensor(self.performance_feedback, dtype=torch.float32)
        total_loss.backward()
        self.optimizer.step()
        self.data_series = []
        self.outputs = []
        self.performance_feedback = []

input_size = 20
hidden_size = 64
output_size = 1

model = SimpleModel(input_size, hidden_size, output_size)
model_manager = ModelManager(model)

def compiler_hook(message_dict, response_fn):
    general_features, _, _ = extract_features(message_dict)
    # TODO: feed block features and subloop features    
    
    # print(f"{client} : {threading.get_ident()}")
    # output = model_manager.feed_data(general_features)
    # output = int(output)
    output = 1 # TODO: remove
    # print(output)
    response_fn(output)
