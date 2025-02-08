from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

TARGET_SERVER_URL = "http://localhost:8000/model/"
FILE_PATH = "deepest_model64.pth"
SEND_INTERVAL = 60


def send_file_periodically():
    while True:
        try:
            files = {'file': open(FILE_PATH, 'rb')}
            response = requests.post(TARGET_SERVER_URL, files=files)
            print(f"File sent, response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error sending file: {e}")
        finally:
            time.sleep(SEND_INTERVAL)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask file sender running"})


if __name__ == '__main__':
    # Start background thread
    threading.Thread(target=send_file_periodically, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)