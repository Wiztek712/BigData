const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
// const list = ['apple','banana','bicycle', 'car', 'cat', 'dog', 'guitar', 'house', 'star', 'sword', 'tent', 'tree']
const list = ['apple','banana', 'bench', 'bicycle', 'car', 'cat', 'dog', 'elbow', 'fish', 'guitar', 'hammer', 'house', 'ice cream', 'moon', 'pencil', 'sailboat', 'star', 'sword', 't-shirt', 'tent', 'tree', 'umbrella', 'wine bottle']

let saveDrawings = [];
let drawing = false;
let drawingData = []; // Stocke le trait en cours
let previousDrawingData = []; // Stocke tous les traits précédents
let currentStroke = null; // Trait courant
let firstStrokeStartTime = null; // Temps de départ global pour tous les traits
let sendDataInterval = null;
let timeLeft = 60; // Game duration in seconds
let score = 0;
let currentWord = "";
let wordGuessed = "";
const SEND_INTERVAL = 200; // Send every 200 milliseconds
randomWord();
startTimer();

function startTimer() {
    const timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            document.getElementById('time-left').textContent = timeLeft;
        } else {
            clearInterval(timerInterval);
            endGame();
        }
    }, 1000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function endGame() {
    const saveData = {
        word: currentWord,
        recognized: false,
        time: Date.now() - firstStrokeStartTime,
        drawing: drawingData.map(stroke => [
            stroke.x.map(Math.floor), // Troncature des X
            stroke.y.map(Math.floor), // Troncature des Y
            stroke.t
        ])
    };
    saveDrawings.push(saveData)
    // console.log(saveDrawings)

    // Get the CSRF token from the cookie
    const csrfToken = getCookie('csrftoken');

    // Send the saveDrawings to the server using Fetch API
    fetch('/save_game_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // Add CSRF token here
        },
        body: JSON.stringify({
            saveDrawings: saveDrawings, // Send drawing data
            score: score // Send score within the body
        }),
    })
        .then(response => response.json())
        .then(data => {
            // console.log('Data saved:', data);
            // After saving, redirect to the final results page
            alert(`Time's up! Your score is ${score} words.`);
            window.location.href = `/final-results/`;
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('There was an error saving the game data.');
        });
}

// Function to start auto-sending if it's not already running
function startAutoSend() {
    // console.log("start")
    if (!sendDataInterval) {
        sendDataInterval = setInterval(() => {
            if (drawingData.length > 0) {
                requestIdleCallback(getDrawingData, { timeout: 300 }); // Use idle time to prevent lag
            }
        }, SEND_INTERVAL);
    }
}

// Function to stop sending data when drawing stops
function stopAutoSend() {
    // console.log("stop")
    clearInterval(sendDataInterval);
    sendDataInterval = null;
}

// Fonction pour démarrer le dessin
function startDrawing(e) {
    drawing = true;

    // Initialiser le trait courant
    currentStroke = {
        x: [],
        y: [],
        t: []
    };

    // Initialiser le temps global si ce n'est pas déjà fait
    if (firstStrokeStartTime === null) {
        firstStrokeStartTime = Date.now();
    }

    draw(e); // Dessiner immédiatement
    startAutoSend();
}

// Fonction pour arrêter le dessin
function stopDrawing() {
    if (drawing && currentStroke) {
        previousDrawingData.push(currentStroke); // Ajouter le trait terminé à la liste principale
        drawingData = previousDrawingData;
        currentStroke = null; // Réinitialiser le trait courant
    }
    drawing = false;
    ctx.beginPath(); // Terminer le chemin courant
    // getDrawingData();
    stopAutoSend();
}

// Fonction pour dessiner
function draw(e) {
    if (!drawing) return;

    // Position de la souris ou du doigt
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor(e.clientX - rect.left); // Troncature de X
    const y = Math.floor(e.clientY - rect.top);  // Troncature de Y
    const t = Date.now() - firstStrokeStartTime; // Temps écoulé depuis le premier point du premier trait

    // Ajouter les coordonnées et le temps au trait courant
    currentStroke.x.push(x);
    currentStroke.y.push(y);
    currentStroke.t.push(t);

    drawingData = [];
    drawingData = drawingData.concat(previousDrawingData, currentStroke);

    // Dessiner sur le canvas
    ctx.lineWidth = 2;
    ctx.lineCap = 'round'; // Terminaisons arrondies
    ctx.strokeStyle = 'black'; // Couleur du trait

    ctx.lineTo(x, y);
    ctx.stroke(); // Dessiner la ligne
    ctx.beginPath();
    ctx.moveTo(x, y); // Déplacer le point de départ
}

// Fonction pour effacer le canvas
function clearCanvas() {
    drawing = false;
    ctx.beginPath();
    stopAutoSend();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawingData = []; // Réinitialiser les traits
    previousDrawingData = [];
    currentStroke = null;
    document.getElementById('prediction-result').textContent =  "";
}

// Fonction pour récupérer les données du dessin au format JSON
async function getDrawingData() {
    // console.log(drawingData)
    const exportData = {
        word: 0, // Exemple, tu peux le modifier
        countrycode: "FR",
        timestamp: new Date().toISOString(),
        recognized: false,
        key_id: "0", // Exemple, tu peux le générer ou le modifier
        drawing: drawingData.map(stroke => [
            stroke.x.map(Math.floor), // Troncature des X
            stroke.y.map(Math.floor), // Troncature des Y
            stroke.t // Temps inchangé
        ]) // Structurer les traits
    };
    object = JSON.stringify([exportData])

    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: object

        });

        const result = await response.json();
        wordGuessed = result.predicted_class;
        if (wordGuessed) {
            // Add this div to your HTML body for displaying results
            document.getElementById('prediction-result').textContent =
                `Predicted class: ${wordGuessed}`;
            document.body.offsetHeight;
            guessed();
        } else {
            alert('Error: Could not get prediction');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error sending data to server');
    }
}

function ChangeWord(found=false){
    const randomItem = list[Math.floor(Math.random() * list.length)];
    if( randomItem != currentWord){

        const saveData = {
            word: currentWord,
            recognized: found,
            time: Date.now() - firstStrokeStartTime,
            key_id: new Date().toISOString(),
            drawing: drawingData.map(stroke => [
                stroke.x.map(Math.floor), // Troncature des X
                stroke.y.map(Math.floor), // Troncature des Y
                stroke.t
            ])
        };
        saveDrawings.push(saveData)
        firstStrokeStartTime = null; // Réinitialiser le temps global
        currentWord = randomItem;
        document.getElementById('word-to-draw').textContent =
            `AI must guess : ${randomItem}`;

        clearCanvas();
    }
    else{
        ChangeWord(found);
    }
}

function randomWord(){
    currentWord = list[Math.floor(Math.random() * list.length)];
    document.getElementById('word-to-draw').textContent =
        `AI must guess : ${currentWord}`;
}

function guessed(){
    document.getElementById('prediction-result').textContent
    if (currentWord == wordGuessed){
        ChangeWord(true);
        score++;
        clearCanvas();
    }
}

// Ajouter les écouteurs d'événements
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);

// Support tactile
canvas.addEventListener('touchstart', (e) => startDrawing(e.touches[0]));
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('touchmove', (e) => draw(e.touches[0]));
