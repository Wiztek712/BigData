import urllib.request
import pandas as pd
import ujson as json

def download_file(url, destination_path):
    try:
        urllib.request.urlretrieve(url, destination_path)
        print(f"File downloaded successfully to {destination_path}")
        return destination_path
    except Exception as e:
        print(f"Failed to download file. Error: {e}")

def parse_ndjson_pandas(file_path):
    try:
        records = map(json.loads, open(file_path))
        df = pd.DataFrame.from_records(records)
        print(df.tail(10))
    except Exception as e:
         print(f"Failed to parse file. Error: {e}")

if __name__ == "__main__":
    url = "https://storage.googleapis.com/quickdraw_dataset/full/simplified/The%20Eiffel%20Tower.ndjson"
    destination_path = "The_Eiffel_Tower.ndjson"
    file_path = download_file(url, destination_path)
    parse_ndjson_pandas(file_path)
