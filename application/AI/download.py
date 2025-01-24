import urllib.request
import urllib.parse


import ndjson
import pandas as pd
from google.cloud import storage

def download_file(url, destination_path):
    try:
        urllib.request.urlretrieve(url, destination_path)
        print(f"File downloaded successfully to {destination_path}")
        return destination_path
    except Exception as e:
        print(f"Failed to download file. Error: {e}")


def download_data_and_parse_it(bucket_name, blob_name):
    """
    Télécharge un fichier NDJSON depuis un bucket public et le parse.

    Args:
        bucket_name (str): Nom du bucket Google Cloud Storage.
        blob_name (str): Chemin du fichier NDJSON dans le bucket.

    Returns:
        pd.DataFrame: Les données converties en DataFrame.

    Raises:
        FileNotFoundError: Si le fichier est introuvable.
    """
    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    if not blob.exists():
        raise FileNotFoundError(f"Le fichier '{blob_name}' est introuvable dans le bucket '{bucket_name}'.")

    try:
        # Utilisation d'un client anonyme pour accéder au bucket public
        client = storage.Client.create_anonymous_client()

        bucket = client.bucket(bucket_name)

        blob = bucket.blob(file_path)

        # Vérifie si le fichier existe
        if not blob.exists():
            raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable dans le bucket '{bucket_name}'.")

        # Télécharge le contenu du fichier
        content = blob.download_as_text()  # Contenu brut en tant que texte
        print(f"Données brutes du fichier {file_path} (500 premiers caractères) :\n{content[:500]}")

        # Parse les données brutes en liste de dictionnaires
        data = ndjson.loads(content)
        print(f"Nombre d'enregistrements chargés : {len(data)}")

        # Convertit en DataFrame si les données sont valides
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            print(f"Fichier chargé avec succès. Aperçu des données :\n{df.head()}")
        else:
            print("Le fichier est vide ou ne contient pas de données valides.")
    except FileNotFoundError as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")



# def download_data_and_parse_it(destination_path):
#     if os.path.exists(destination_path):
#         print("The file exists.")
#         return parse_ndjson_pandas(destination_path)
#     else:
#         print("The file does not exist.")
#         # Get the file name without extension
#         file_name = os.path.splitext(os.path.basename(destination_path))[0]

#         # URL encode the file name to handle special characters
#         encoded_file_name = urllib.parse.quote(file_name)

#         # Construct the URL using the encoded file name
#         url = f"https://storage.googleapis.com/quickdraw_dataset/full/simplified/{encoded_file_name}.ndjson"

#         # Now you can call the download and parse function
#         file_path = download_file(url, destination_path)
#         return parse_ndjson_pandas(file_path)

if __name__ == "__main__":
    bucket_name = "quickdraw_dataset"
    dataset_names = [
        "star", "sword", "tent", "apple", "banana", "cat",
        "dog", "car", "house", "tree", "rocket", "guitar", "bicycle"
    ]

    datasets = {}
    for name in dataset_names:
        file_path = f"full/simplified/{name}.ndjson"
        datasets[name] = download_data_and_parse_it(file_path, name)
