from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
import gridfs
import torch
import os
from io import BytesIO

# MongoDB connection
MONGO_URI = "mongodb+srv://rabanquentin:Yl9svhJSF3F0Fodp@mongo.yrj08.mongodb.net/?retryWrites=true&w=majority&appName=mongo"
client = MongoClient(MONGO_URI)
db = client["mydatabase"]
fs = gridfs.GridFS(db)

app = Flask(__name__)

# ------------------------ 1. UPLOAD MODEL ------------------------

@app.route("/upload_model", methods=["POST"])
def upload_model():
    """Uploads a PyTorch model file to MongoDB GridFS."""
    if "model" not in request.files:
        return jsonify({"error": "No model file provided"}), 400
    
    model_file = request.files["model"]
    
    # Delete old model if exists
    existing_file = fs.find_one({"filename": model_file.filename})
    if existing_file:
        fs.delete(existing_file._id)

    model_id = fs.put(model_file, filename=model_file.filename)
    
    return jsonify({"message": "Model uploaded successfully!", "model_id": str(model_id)}), 200

# ------------------------ 2. UPLOAD WORD LIST ------------------------

@app.route("/upload_words", methods=["POST"])
def upload_words():
    """Uploads a word-class mapping to MongoDB."""
    words = request.json.get("words", [])
    
    if not words:
        return jsonify({"error": "Word list is empty"}), 400

    db.word_mapping.delete_many({})  # Clear old data
    db.word_mapping.insert_many(words)

    return jsonify({"message": "Word mapping uploaded successfully!"}), 200

# ------------------------ 3. DOWNLOAD MODEL ------------------------

@app.route("/download_model", methods=["GET"])
def download_model():
    """Fetches the PyTorch model file from MongoDB GridFS."""
    file = fs.find_one({"filename": "deepest_model64_23labels.pth"})
    if not file:
        return jsonify({"error": "Model not found"}), 404

    model_data = file.read()
    buffer = BytesIO(model_data)

    return send_file(buffer, mimetype="application/octet-stream", as_attachment=True, download_name="model.pth")

# ------------------------ 4. GET WORD LIST ------------------------

@app.route("/get_words", methods=["GET"])
def get_words():
    """Fetches the word-class mapping from MongoDB."""
    word_mapping = list(db.word_mapping.find({}, {"_id": 0}))  # Exclude "_id"
    
    if not word_mapping:
        return jsonify({"error": "No word mapping found"}), 404
    
    return jsonify({"word_mapping": word_mapping}), 200

# ------------------------ RUN SERVER ------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
