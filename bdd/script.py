from google.cloud import storage
import ndjson

def load_quickdraw_data(bucket_name, blob_name):
    # Configurer le client Google Cloud
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Télécharger et charger le fichier NDJSON
    content = blob.download_as_text()
    data = ndjson.loads(content)
    return data

# Charger les dessins "apple"
bucket_name = "quickdraw_dataset"
blob_name = "full/simplified/apple.ndjson"
blob_nameStar = "full/simplified/star.ndjson"
blob_nameTent = "full/simplified/tent.ndjson"
blob_nameSword = "full/simplified/sword.ndjson"

data = load_quickdraw_data(bucket_name, blob_name)
dataStar = load_quickdraw_data(bucket_name, blob_nameStar)
dataTent = load_quickdraw_data(bucket_name, blob_nameTent)
dataSword = load_quickdraw_data(bucket_name, blob_nameSword)
print(f"Nombre de dessins chargés : {len(data)}")
print(f"Nombre de dessins Star chargés : {len(dataStar)}")
print(f"Nombre de dessins Tent chargés : {len(dataTent)}")
print(f"Nombre de dessins Sword chargés : {len(dataSword)}")

import matplotlib.pyplot as plt

def visualize_drawing(drawing):
    """
    Affiche un dessin à partir des coordonnées de ses traits.
    :param drawing: Liste des traits (chaque trait est une liste de coordonnées [x, y]).
    """
    plt.figure(figsize=(3, 3))

    # Parcourir les traits et tracer chaque ligne
    for stroke in drawing:
        x, y = stroke
        plt.plot(x, y, marker='o', color='black', linewidth=2)

    # Configuration de l'affichage
    plt.gca().invert_yaxis()  # Inverser l'axe Y pour correspondre à l'orientation du dessin
    plt.axis('off')           # Cacher les axes
    plt.show()

# Visualiser le premier dessin dans la liste
first_drawing = data[1]['drawing']
star = dataStar[1]['drawing']
tent = dataTent[1]['drawing']
sword = dataSword[3]['drawing']

visualize_drawing(first_drawing)
visualize_drawing(star)
visualize_drawing(tent)
visualize_drawing(sword)
