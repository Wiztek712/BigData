# BigData - Interactive Pictionary AI
**School Project - Borget Flavien, Jacquet Clément, Laval Corentin, Raban Quentin**

## **Project Overview**
This project aims to create an interactive **Pictionary-style** web application where users draw objects, and a machine learning model attempts to recognize them in real time. This concept was inspired by **Google's "Quick, Draw!"** project.

###  **Main Objectives**
#### **1️⃣ Machine Learning**
- Develop an **image classification model** capable of recognizing freehand drawings.
- Use an **annotated dataset** to train the model.
- Implement **supervised and unsupervised learning** techniques to optimize recognition.

#### **2️⃣ Front-End**
- Design an intuitive UI with a **digital canvas** for users to draw on.
- Display real-time recognition attempts.
- Include **features** such as:
    - A **timer**
    - User **scores**
    - Word **categories** (e.g., animals, objects, food).

#### **3️⃣ Back-End**
- Store **user drawings and game results**.
- Manage machine learning **models and their improvements**.
- Use a **MongoDB database** for handling users, drawings, and scores.
- **Future migration:** **Host the full application (Docker) on AWS** for centralized access via a **public IP**.

---

##  **Game Mechanics**
###  **Pictionary Data**
#### **Step 1 - Defining Words to Draw**
- Create a set of **at least 10 words** per category.
- Automate **word retrieval** from online sources (e.g., APIs).

#### **Step 2 - Game Results Storage**
- Store **drawing time, recognition attempts**, and other stats.
- Analyze data to determine which words are the hardest to guess.

---

##  **Machine Learning Model**
### **Step 1 - Dataset Selection**
- Use public datasets such as:
    - **Quick, Draw! Dataset**
    - **Sketchy Database**
    - **Doodle Dataset**.

### **Step 2 - Model Implementation**
- Start with **pre-trained models** (e.g., CNN, ResNet).
- Develop a **custom model** to classify drawings in real-time.

### **Step 3 - Continuous Learning**
- Implement **feedback-based learning**:
    - Allow users to **confirm/reject** predictions.
    - Use **collected feedback** to fine-tune the model.

---

##  **Web Application**
### **Features**
-  **User Authentication** (login system).
-  **Word selection** stored in the Cloud.
-  **Real-time drawing recognition** using the trained ML model.
-  **Game results** displayed at the end.

Everything (words, models, users, and results) is stored **in the cloud**.

---

## 🛠 **Technologies Used**
| Component    | Technology |
|-------------|-----------|
| Front-End   | **HTML, CSS, JavaScript (Canvas API)** |
| Back-End    | **Django, Flask, FastAPI** |
| Database    | **MongoDB Atlas** |
| ML Model    | **TensorFlow, PyTorch, OpenCV** |
| Deployment  | **Docker, Docker Compose (AWS planned)** |

---

##  **Project Setup**
### **Installation**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_repo.git
   cd your_repo
   ```
2. **Create and activate a virtual environment**:
    ```bash
    # Linux / macOS
    python -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.	**Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.	**Run the database & server**:

    ```bash
    docker-compose up -d
    python manage.py migrate
    python manage.py runserver
    ```

5.	**Access the app**:

    Open http://localhost:8000/ in your browser.

---

## Deployment (Cloud)

Current Deployment
* The application is currently using **MongoDB Atlas** for storing:	
  - User data 
  - Drawings 
  - Game results 
  - ML models

**Future Plans: Full Deployment on AWS**

*   Move Dockerized Application to AWS (e.g., EC2 / ECS).
*	Use a single public IP for centralized access.
*	Improve scalability & reduce latency for ML inference.

