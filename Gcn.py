import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

input_features = 5


# Step 1: Define the graph data structure
edge_index = torch.tensor([[0, 1, 1, 2], [1, 0, 2, 1]], dtype=torch.long)
x = torch.randn(3, input_features)  # 3 nodes, each with 5 features
y = torch.tensor([0, 1, 0], dtype=torch.long)  # Class labels for each node

data = Data(x=x, edge_index=edge_index, y=y)

# Step 2: Define a simple Graph Neural Network (GNN) model
class SimpleGNN(torch.nn.Module):
    def __init__(self):
        super(SimpleGNN, self).__init__()
        self.conv1 = GCNConv(input_features, 16)  # Input features: 5, Output features: 16
        self.conv2 = GCNConv(16, 2)  # Output features: 2

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)

model = SimpleGNN()

# Step 3: Define the training loop
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.NLLLoss()

def train():
    model.train()
    optimizer.zero_grad()
    output = model(data)
    loss = criterion(output, data.y)
    loss.backward()
    optimizer.step()
    return loss.item()

# Train for a few epochs (you may need more epochs for a real-world scenario)
for epoch in range(100):
    loss = train()
    print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')

# Step 4: Make predictions on a new graph
new_data = Data(x=torch.randn(1, input_features), edge_index=torch.tensor([[0], [0]], dtype=torch.long))
model.eval()
with torch.no_grad():
    prediction = model(new_data)

print("Prediction:", torch.argmax(prediction).item())