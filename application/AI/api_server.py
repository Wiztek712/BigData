from flask import Flask, request, jsonify
from model import EnhancedCNN
import torch

app = Flask(__name__)

model = EnhancedCNN(num_classes=12)
model.load_state_dict(torch.load('/home/quentin/BigData/application/AI/deepest_model.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    image_bytes = request.files['image'].read()
    
    prediction = model.predict(image_bytes)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
