import os
import urllib.request
import urllib.parse
import ndjson
import pandas as pd
from google.cloud import storage


def download_file(url, destination_path):
    """
    Télécharge un fichier depuis une URL et l'enregistre localement.

    Args:
        url (str): URL du fichier à télécharger.
        destination_path (str): Chemin où enregistrer le fichier localement.

    Returns:
        str: Chemin vers le fichier téléchargé.
    """
    try:
        urllib.request.urlretrieve(url, destination_path)
        print(f"Fichier téléchargé avec succès vers : {destination_path}")
        return destination_path
    except Exception as e:
        print(f"Échec du téléchargement. Erreur : {e}")
        raise


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
    # Création d'un client anonyme pour les buckets publics
    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Vérification si le fichier existe dans le bucket
    if not blob.exists():
        raise FileNotFoundError(f"Le fichier '{blob_name}' est introuvable dans le bucket '{bucket_name}'.")

    try:
        # Téléchargement du contenu du fichier
        content = blob.download_as_text()  # Contenu brut sous forme de texte
        print(f"Données brutes du fichier {blob_name} (500 premiers caractères) :\n{content[:500]}")

        # Parsing des données NDJSON
        data = ndjson.loads(content)

        # Validation et conversion en DataFrame
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            print(f"Fichier chargé avec succès. Nombre d'enregistrements : {len(df)}")
            return df
        else:
            raise ValueError("Le fichier est vide ou ne contient pas de données valides.")
    except Exception as e:
        print(f"Erreur inattendue lors du traitement de {blob_name} : {e}")
        raise


if __name__ == "__main__":
    # Configuration du bucket et des datasets
    bucket_name = "quickdraw_dataset"
    dataset_names = [
        "star", "sword", "tent", "apple", "banana", "cat",
        "dog", "car", "house", "tree", "rocket", "guitar", "bicycle"
    ]

    datasets = {}

    # Boucle pour télécharger et parser chaque dataset
    for name in dataset_names:
        try:
            file_path = f"full/simplified/{name}.ndjson"
            print(f"Traitement du fichier : {file_path}")
            df = download_data_and_parse_it(bucket_name, file_path)
            datasets[name] = df
        except FileNotFoundError as e:
            print(f"Erreur : {e}")
        except Exception as e:
            print(f"Erreur inattendue pour {name} : {e}")

    # Exemple : Afficher les premières lignes d'un DataFrame
    if "star" in datasets:
        print(datasets["star"].head())
