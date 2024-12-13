const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
const PORT = 3000;

// Configuration MongoDB
const MONGO_URL = 'mongodb://mongo:27017'; // Adresse du service MongoDB
let db;

// Middleware pour parser le JSON dans les requêtes
app.use(express.json());

// Connexion à MongoDB
MongoClient.connect(MONGO_URL, { useUnifiedTopology: true })
    .then((client) => {
        db = client.db('quickdraw');
        console.log('Connected to MongoDB');

        // Création des indexes
        db.collection('drawings').createIndex({ user: 1 }) // Index sur "user"
            .then(() => console.log('Index created on user field'))
            .catch((err) => console.error('Error creating user index:', err));

        db.collection('drawings').createIndex({ word: 1 }) // Index sur "word"
            .then(() => console.log('Index created on word field'))
            .catch((err) => console.error('Error creating word index:', err));
    })
    .catch((err) => console.error('Error connecting to MongoDB:', err));

// Routes

// 1. Ajouter un dessin
app.post('/drawings', async (req, res) => {
    try {
        const { word, drawing, user, recognitionTime, recognized } = req.body;
        if (!word || !drawing || !user || recognitionTime === undefined) {
            return res.status(400).send({ error: 'Invalid data format. Missing required fields.' });
        }

        const newDrawing = {
            word,
            drawing,
            user,
            recognitionTime,
            recognized: recognized || false, // Défaut à `false` si non fourni
            timestamp: new Date(),
        };

        await db.collection('drawings').insertOne(newDrawing);
        res.status(201).send({ message: 'Drawing added successfully', drawing: newDrawing });
    } catch (err) {
        res.status(500).send({ error: 'Failed to add drawing' });
    }
});

// 2. Obtenir tous les dessins
app.get('/drawings', async (req, res) => {
    try {
        const drawings = await db.collection('drawings').find().toArray();
        res.json(drawings);
    } catch (err) {
        res.status(500).send({ error: 'Failed to fetch drawings' });
    }
});

// 3. Obtenir tous les dessins d'un même nom
app.get('/drawings/word/:word', async (req, res) => {
    const { word } = req.params;
    try {
        const drawings = await db.collection('drawings').find({ word }).toArray();
        if (drawings.length === 0) {
            return res.status(404).send({ error: `No drawings found for word: ${word}` });
        }
        res.json(drawings);
    } catch (err) {
        res.status(500).send({ error: 'Failed to fetch drawings by word' });
    }
});

// 4. Lister tous les utilisateurs
app.get('/users', async (req, res) => {
    try {
        const users = await db.collection('drawings').distinct('user');
        res.json(users);
    } catch (err) {
        res.status(500).send({ error: 'Failed to fetch users' });
    }
});

// 5. Obtenir tous les dessins d'un utilisateur
app.get('/drawings/user/:user', async (req, res) => {
    const { user } = req.params;
    try {
        const drawings = await db.collection('drawings').find({ user }).toArray();
        if (drawings.length === 0) {
            return res.status(404).send({ error: `No drawings found for user: ${user}` });
        }
        res.json(drawings);
    } catch (err) {
        res.status(500).send({ error: 'Failed to fetch drawings by user' });
    }
});

// Démarrer le serveur
app.listen(PORT, () => console.log(`API running on http://localhost:${PORT}`));
