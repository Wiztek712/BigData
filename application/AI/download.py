import urllib.request
import urllib.parse
import pandas as pd
import ujson as json
import os

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
        return df
    except Exception as e:
         print(f"Failed to parse file. Error: {e}")

def download_data_and_parse_it(destination_path):
    if os.path.exists(destination_path):
        print("The file exists.")
        return parse_ndjson_pandas(destination_path)
    else:
        print("The file does not exist.")
        # Get the file name without extension
        file_name = os.path.splitext(os.path.basename(destination_path))[0]
        
        # URL encode the file name to handle special characters
        encoded_file_name = urllib.parse.quote(file_name)
        
        # Construct the URL using the encoded file name
        url = f"https://storage.googleapis.com/quickdraw_dataset/full/simplified/{encoded_file_name}.ndjson"

        # Now you can call the download and parse function
        file_path = download_file(url, destination_path)
        return parse_ndjson_pandas(file_path)

if __name__ == "__main__":
    file_path = "star.ndjson"
    df = download_data_and_parse_it(file_path)
    file_path = "sword.ndjson"
    df1 = download_data_and_parse_it(file_path)
    file_path = "tent.ndjson"
    df2 = download_data_and_parse_it(file_path)