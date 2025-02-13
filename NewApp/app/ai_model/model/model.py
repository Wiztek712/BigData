import torch
import torch.nn as nn
import torch.optim as optim
import gridfs
from pymongo import MongoClient
from io import BytesIO
from hostname import DB_URL

batch_size = 32
num_classes = 23
learning_rate = 0.001
num_epochs = 10

client = MongoClient(DB_URL)
db = client["mydatabase"]
fs = gridfs.GridFS(db)

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

def get_model():
    """Fetches and loads a PyTorch model state_dict from MongoDB GridFS."""
    model_filename = "final_model.pth"
    model_file = fs.find_one({"filename": model_filename})
    
    if not model_file:
        raise FileNotFoundError(f"No model found with filename: {model_filename}")
    
    # Read file content into a buffer
    model_data = BytesIO(model_file.read())

    # Load only the state_dict
    state_dict = torch.load(model_data, map_location=torch.device('cpu'))  
    return state_dict  # Return only the state_dict

# Initialize the model
device = "cuda" if torch.cuda.is_available() else "cpu"
deepModel = EnhancedCNN().to(device)  # Make sure EnhancedCNN() is defined
optimizer = optim.Adam(deepModel.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

# Load the state dict
pthFile = get_model()
deepModel.load_state_dict(pthFile)  # Corrected this line
deepModel.eval()  # Set model to evaluation mode

def getModel():
    return deepModel