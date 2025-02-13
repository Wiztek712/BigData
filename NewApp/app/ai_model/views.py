from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import torch
import pandas as pd
import json
import gridfs
from io import BytesIO
import requests
from .model.model import EnhancedCNN, getModel
from .model.process import process
from pymongo import MongoClient
from hostname import DB_URL

UPLOAD_DIR = "ai_model/model/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
# word_class_mapping = [['apple', 0], ['banana', 1], ['bicycle', 2], ['car', 3], ['cat', 4], ['dog', 5], ['guitar', 6], ['house', 7], ['star', 8], ['sword', 9], ['tent', 10], ['tree', 11]]
# word_class_mapping = [['apple',  0],  ['banana', 1], ['bench',  2], ['bicycle', 3], ['car', 4], ['cat', 5], ['dog', 6], ['elbow', 7], ['fish', 8], ['guitar', 9], ['hammer', 10], ['house', 11], ['ice cream', 12], ['moon', 13], ['pencil', 14], ['sailboat', 15], ['star', 16], ['sword', 17], ['t-shirt', 18], ['tent', 19], ['tree', 20], ['umbrella', 21], ['wine bottle', 22]]
client = MongoClient(DB_URL)
srv = client["mydatabase"]
word_collection = srv["word_mapping"]
# model_collection = srv["fs.files"]
# fs = gridfs.GridFS(srv)

def get_word_list():
    """Fetch word list from the Flask server."""
    list = []
    try:
        documents = word_collection.find()
        for word in documents:
            list.append([word['word'], word['class']])
        return list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching word list: {e}")
        return list

word_class_mapping = get_word_list()

model = getModel()
# print("model: ", getModel())

@csrf_exempt
def download_model(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        return JsonResponse({"message": "File uploaded successfully", "file_path": file_path})
    
    return JsonResponse({"error": "No file provided"}, status=400)

@csrf_exempt
def predict(request):
    # print("copy")
    if request.method == 'POST':
        # print(request.body)
        try:
            # destination_path = "ai_model/model/raw_prediction.json"
            # if os.path.exists(destination_path):
            #     with open(destination_path, "r", encoding="utf-8") as f:
            #         data = pd.DataFrame.from_records(json.load(f))

            data = json.loads(request.body.decode('utf-8')) 
            # print("Received JSON data:", json.dumps(data, indent=4))    
            # print("Received word:", data.get("word"))

            # # Store raw JSON data before any transformation
            # destination_path = "ai_model/model/raw_prediction.json"
            # with open(destination_path, "w", encoding="utf-8") as f:
            #     json.dump(data, f, indent=4)

            with torch.no_grad():
                processed_data = process(data)
                # print("data : ", data)
                # print("model : ", model)
                # print("processed_data : ", processed_data)
                for images, labels in processed_data:
                    # print("images before : ",images)
                    # print("labels before : ",labels)
                    images, labels = images.to(device), labels.to(device)
                    # print("images : ",images)
                    # print("labels : ",labels)
                    output = model(images)
                    print("output : ",output)
                    predicted_class = word_class_mapping[torch.argmax(output, dim=1).item()][0]
                    # print("prediction done")
                return JsonResponse({
                    "predicted_class": predicted_class
                })
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)