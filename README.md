# BigData
School Project - Borget Flavien, JACQUET Clément, LAVAL Corentin, RABAN Quentin

# Subject

The aim of this project is to create an interactive Pictionary application where users draw objects and a machine learning model tries to guess what they are drawing. This application was developed by Google in their project
“Quick, Draw” project.

Several objectives emerge in this project:
## Machine Learning:
- Develop an image classification model capable of recognizing freehand drawings. Use a dataset of drawings to train the model.
- Implement supervised and unsupervised learning techniques to improve model performance.
## Front-End:
- Design an intuitive user interface where users can draw using a digital canvas. The interface should display the drawing in real time and show attempts to recognize the model.
- Integrate features such as a stopwatch, user scores (i.e. how long it takes the algorithm to guess the drawing) and categories of words to draw.
## Back-End:
- Set up a system to store user drawings and game results. This system must also store the machine learning models.
- Use a database to manage users, drawings and scores

## Further Informations :

### Pictionary data

#### STEP 1 - Designing the words to be drawn :
You need to define a set of words or objects for users to draw (at least 10 words). Each word should be associated with a category (e.g. animals, objects, food) to facilitate selection during the game. You are encouraged to write a script to automatically retrieve sets of words from online sources.

#### STEP 2 - Game results:
You should also be able to store the results of the game for each participant, such as the time taken to draw and find each word and the number of attempts needed to guess the word correctly. These results can be analyzed afterwards to determine, for example, which word was the most difficult for the machine to guess.

### Training the image recognition model

In this part, we'll develop, train and implement a machine learning model to recognize drawings made by users.

#### STEP 1 - Download drawing datasets:
Use datasets available online, such as the Quick, Draw! Dataset, which contains millions of drawings of various objects. This data can be used to train your recognition model. See also: Sketchy Database, Doodle Dataset.
#### STEP 2 - Implementing the model :
In this step, you'll need to propose and implement a machine learning model to recognize user drawings. You can start by using pre-trained models, then you'll need to develop your own model to classify drawings in real time. You are free to set the complexity of the approach. For similar results, we'll give preference to the least complex models.
#### STEP 3 - Continuous improvement of the model :
Finally, you'll need to develop an intelligent approach to improving your image recognition model as users draw. For example, you could offer a “feedback” option where users can confirm whether the guessed word is correct, and use this information to refine the model over time.

### Application

Design and implementation of an application for :
- Retrieve user information (login system)
- selection of words to draw stored in the Cloud
- Run the game with recognition of the drawings via the model (the model is also stored in the cloud, inference is done online)
- Communication of results to the user (drawing time, number of attempts).

The application doesn't need to store anything locally. All elements (words to be drawn, model, users, results) are stored in the cloud, in a technical solution that you can choose.

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

Then, please run this command to install the docker (in BigData\NewApp) (can take time and downloads)
```bash
docker-compose up -d
```
After that , you can go on http://localhost:8000/ to use the app
