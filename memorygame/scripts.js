const CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8];
let shuffledCards = [];
let flippedCards = [];
let score = 0;
let startTime;
let gameData = JSON.parse(localStorage.getItem("gameData")) || [];
let bestTime = localStorage.getItem("bestTime") || '--';

const scoreElement = document.getElementById('score');
const timerElement = document.getElementById('timer');
const bestTimeElement = document.getElementById('bestTime');
const gameGrid = document.getElementById('gameGrid');
const popupMessage = document.getElementById('popupMessage');
const popupText = document.getElementById('popupText');
const replayBtn = document.getElementById('replayBtn');
const quitBtn = document.getElementById('quitBtn');
const showDataBtn = document.getElementById('showDataBtn');
const plotProgressBtn = document.getElementById('plotProgressBtn');

function startGame() {
    shuffledCards = shuffle(CARD_VALUES.slice());
    createGameGrid();
    score = 0;
    flippedCards = [];
    startTime = Date.now();
    updateScore();
    updateTimer();
    popupMessage.classList.add('hidden');
    gameGrid.classList.remove('hidden');
    bestTimeElement.innerText = `Best Time: ${bestTime}`;
}

function shuffle(array) {
    let currentIndex = array.length, randomIndex, tempValue;

    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        tempValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = tempValue;
    }

    return array;
}

function createGameGrid() {
    gameGrid.innerHTML = '';
    shuffledCards.forEach((cardValue, index) => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.value = cardValue;
        card.dataset.index = index;
        card.addEventListener('click', handleCardClick);
        gameGrid.appendChild(card);
    });
}

function handleCardClick(e) {
    const card = e.target;
    if (flippedCards.length === 2 || card.classList.contains('flipped') || card.classList.contains('matched')) {
        return;
    }

    card.classList.add('flipped');
    card.innerText = card.dataset.value;
    flippedCards.push(card);

    if (flippedCards.length === 2) {
        checkForMatch();
    }
}

function checkForMatch() {
    const [card1, card2] = flippedCards;
    if (card1.dataset.value === card2.dataset.value) {
        card1.classList.add('matched');
        card2.classList.add('matched');
        score++;
        updateScore();
        flippedCards = [];
        if (checkGameComplete()) {
            endGame();
        }
    } else {
        setTimeout(() => {
            card1.classList.remove('flipped');
            card2.classList.remove('flipped');
            flippedCards = [];
        }, 1000);
    }
}

function checkGameComplete() {
    return document.querySelectorAll('.matched').length === shuffledCards.length;
}

function updateScore() {
    scoreElement.innerText = `Score: ${score}`;
}

function updateTimer() {
    const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
    timerElement.innerText = `Time: ${elapsedTime}s`;
    setTimeout(updateTimer, 1000);
}

function endGame() {
    const completionTime = Math.floor((Date.now() - startTime) / 1000);
    if (!bestTime || completionTime < bestTime) {
        bestTime = completionTime;
        localStorage.setItem('bestTime', bestTime);
        bestTimeElement.innerText = `Best Time: ${bestTime}`;
    }
    gameData.push({ score, completionTime });
    localStorage.setItem("gameData", JSON.stringify(gameData));
    showPopupMessage(`You Win!\nScore: ${score}\nTime: ${completionTime}s`);
}

function showPopupMessage(message) {
    popupText.innerText = message;
    popupMessage.classList.remove('hidden');
    gameGrid.classList.add('hidden');
}

replayBtn.addEventListener('click', startGame);
quitBtn.addEventListener('click', () => window.close());
showDataBtn.addEventListener('click', displayGameData);
plotProgressBtn.addEventListener('click', plotProgress);

function displayGameData() {
    alert(JSON.stringify(gameData, null, 2));
}

function plotProgress() {
    const times = gameData.map(data => data.completionTime);
    const scores = gameData.map(data => data.score);

    const trace1 = {
        x: times,
        y: scores,
        mode: 'lines+markers',
        type: 'scatter',
        name: 'Scores vs Time'
    };

    const layout = {
        title: 'Game Progress Over Time',
        xaxis: { title: 'Time (s)' },
        yaxis: { title: 'Score' }
    };

    Plotly.newPlot('progressChart', [trace1], layout);
}

document.addEventListener('DOMContentLoaded', startGame);
