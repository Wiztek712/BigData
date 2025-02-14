#!/bin/bash

# Define the URL of the Flask server and the path to the model file
MODEL_URL="http://localhost:5001/upload_model"
WORD_URL="http://localhost:5001/upload_words"
MODEL_FILE="final_model.pth"  # Path to your .pth model file
WORD_FILE="words.json"

# Use curl to send the POST request with the model file as form-data
curl -X POST -F "model=@$MODEL_FILE" $MODEL_URL

curl -X POST -H "Content-Type: application/json" -d @$WORD_FILE $WORD_URL