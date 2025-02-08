import torch
import torch.nn as nn
import torch.optim as optim

batch_size = 32
num_classes = 12
learning_rate = 0.001
num_epochs = 10

class EnhancedCNN(nn.Module):
    def __init__(self):
        super(EnhancedCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16),  # Normalize feature maps for faster convergence
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),  # Add a third convolutional layer
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 256),  # More neurons for higher capacity
            nn.ReLU(),
            nn.Dropout(0.5),  # Add dropout for regularization
            nn.Linear(256, num_classes),
        )
        
    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x
    
device = "cuda" if torch.cuda.is_available() else "cpu"
deepModel = EnhancedCNN().to(device)
optimizer = optim.Adam(deepModel.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

model = EnhancedCNN().to(device)
model.load_state_dict(torch.load("ai_model/model/deepest_model64.pth", map_location=torch.device('cpu')))
model.eval()

def getModel():
    return model