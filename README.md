# BigData
School Project - Borget Flavien, JACQUET Clément, LAVAL Corentin, RABAN Quentin

# Subject

L'objectif de ce projet est de créer une application interactive de Pictionary où les
utilisateurs dessinent des objets et un modèle de machine learning tente de deviner
ce qu'ils dessinent. Cette application a été développée par Google dans leur projet
“Quick, Draw”

Plusieurs objectifs se dégagent dans ce projet :
## Machine Learning :
- Développer un modèle de classification d'images capable de reconnaître des
dessins à main levée. Utiliser un ensemble de données de dessins pour
entraîner le modèle.
- Implémenter des techniques d'apprentissage supervisé et non supervisé pour
améliorer la performance du modèle.
## Front-End :
- Concevoir une interface utilisateur intuitive où les utilisateurs peuvent
dessiner en utilisant une toile numérique. L'interface doit afficher le dessin en
temps réel et montrer les tentatives de reconnaissance du modèle.
- Intégrer des fonctionnalités telles que le chronomètre, les scores des
utilisateurs (c'est-à-dire le temps nécessaire à l’algorithme pour deviner le
dessin) et les catégories de mots à dessiner.
## Back-End :
- Mettre en place un système pour stocker les dessins des utilisateurs et les
résultats des parties. Ce système doit également stocker les modèles de
machine learning.
- Utiliser une base de données pour gérer les utilisateurs, les dessins et les
scores

## Further Informations :

### Données du Pictionary

####  ETAPE 1 - Conception des mots à dessiner :
Vous devez définir un ensemble de mots ou d'objets que les utilisateurs devront
dessiner (au moins 10 mots). Chaque mot doit être associé à une catégorie (par
exemple, animaux, objets, aliments) pour faciliter la sélection pendant le jeu. Vous
êtes encouragés à écrire un script permettant de récupérer automatiquement des
ensembles de mots à partir de sources en ligne.

####  ETAPE 2 - Résultats du jeu :
Vous devez également être en mesure de stocker les résultats du jeu pour chaque
participant, tels que le temps mis pour dessiner et trouver chaque mot et le nombre
de tentatives nécessaires pour deviner correctement le mot. Ces résultats pourront
être analysés a posteriori pour déterminer, par exemple, quel mot a été le plus difficile
à deviner par la machine.

### Entraînement du modèle de reconnaissance d'images

Dans cette partie, il s'agira d'élaborer, d'entraîner et de mettre en œuvre un modèle
de machine learning pour reconnaître les dessins réalisés par les utilisateurs.

####  ETAPE 1 - Téléchargement des ensembles de données de dessins :
Utilisez des ensembles de données disponibles en ligne, comme le Quick, Draw!
Dataset, qui contient des millions de dessins de divers objets. Ces données peuvent
être utilisées pour entraîner votre modèle de reconnaissance. Voir aussi : Sketchy
Database, Doodle Dataset.
####  ETAPE 2 - Mise en application du modèle :
Dans cette étape, vous devrez proposer et mettre en œuvre un modèle de machine
learning pour reconnaître les dessins des utilisateurs. Vous pouvez commencer par
utiliser des modèles pré-entraînés, puis vous devrez développer votre propre modèle
pour classer les dessins en temps réel. Vous êtes libres de fixer la complexité de
l'approche. À résultat similaire, nous privilégierons les modèles les moins complexes.
####  ETAPE 3 - Amélioration continue du modèle :
Pour terminer, il conviendra de développer une approche intelligente permettant
d’améliorer votre modèle de reconnaissance d'images au fur et à mesure que les
utilisateurs dessinent. Par exemple, vous pouvez proposer une option de "feedback"
où les utilisateurs peuvent confirmer si le mot deviné est correct, et utiliser ces
informations pour affiner le modèle au fil du temps.

### Application

Conception et implémentation d'une application permettant :
- La récupération des informations sur l’utilisateur (système de login)
- La sélection de mots à dessiner stockés dans le Cloud
- Le déroulé du jeu avec reconnaissance des dessins via le modèle (le modèle
est lui aussi stocké dans le cloud, l’inférence est faite en ligne)
- La communication des résultats à l’utilisateur (temps de dessin, nombre de
tentatives).

L’application ne doit absolument rien stocker en local. Tous les éléments (mots à
dessiner, modèle, utilisateurs, résultats) sont stockés dans le cloud, dans une
solution technique qu’il vous appartient de choisir

# Project

## Install

In order to perfrom a clean install, let's begin by deploying a virtual environment.
The following commands assumes that you have python3, python-virtualenv and pip3 already installed.
In root folder : 
```bash
# Linux
python venv .venv
source venv/bin/activate

# Windows
python venv .venv
.venv/Scripts/activate
```

Then, please run this command to install all the requiered libraries
```bash
pip install -r application/requirements.txt
```

## Run the project

### AI

In AI folder, you will find download.py and model.ipynb. The first implements functions to retrieve data from google cloud, the second is a jupyter notebook where we have developped the AI. You can run it through vscode or by running in BigData/application/AI folder : 
```bash
jupyter notebook
```