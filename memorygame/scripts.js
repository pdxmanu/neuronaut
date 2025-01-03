// Game Variables
let cards = [];
let flippedCards = [];
let matchedCards = [];
let score = 0;
let startTime;
let gameCompleted = false;

// Initialize Game
const gameBoard = document.getElementById("game-board");
const scoreDisplay = document.getElementById("score");
const timeDisplay = document.getElementById("time");
const popupMessage = document.getElementById("popup-message");

function initializeGame() {
    cards = [];
    flippedCards = [];
    matchedCards = [];
    score = 0;
    startTime = Date.now();
    gameCompleted = false;

    // Create 4x4 grid of cards
    const cardValues = [1, 2, 3, 4, 5, 6, 7, 8];
    shuffleArray(cardValues);

    gameBoard.innerHTML = ""; // Clear previous cards

    for (let i = 0; i < 16; i++) {
        const card = document.createElement("div");
        card.classList.add("card");
        card.dataset.value = cardValues[i];
        card.dataset.index = i;

        card.addEventListener("click", flipCard);
        gameBoard.appendChild(card);
    }
    updateScore();
    updateTime();
}

function flipCard(event) {
    if (gameCompleted || flippedCards.length >= 2 || event.target.classList.contains("flipped")) return;

    const card = event.target;
    card.classList.add("flipped");
    card.innerText = card.dataset.value;
    flippedCards.push(card);

    if (flippedCards.length === 2) {
        checkMatch();
    }
}

function checkMatch() {
    const [card1, card2] = flippedCards;
    if (card1.dataset.value === card2.dataset.value) {
        card1.classList.add("matched");
        card2.classList.add("matched");
        matchedCards.push(card1, card2);
        score++;
        if (matchedCards.length === 16) {
            gameCompleted = true;
            showPopup("You Win! Press R to Replay | Q to Quit");
        }
    } else {
        setTimeout(() => {
            card1.classList.remove("flipped");
            card2.classList.remove("flipped");
        }, 1000);
    }
    flippedCards = [];
    updateScore();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Swap elements
    }
}

function updateScore() {
    scoreDisplay.textContent = `Score: ${score}`;
}

function updateTime() {
    if (!gameCompleted) {
        const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        timeDisplay.textContent = `Time: ${elapsedTime}s`;
        requestAnimationFrame(updateTime);
    }
}

function showPopup(message) {
    popupMessage.querySelector("p").innerText = message;
    popupMessage.style.display = "block";
}

// Event listeners for replay and quit
document.addEventListener("keydown", (event) => {
    if (gameCompleted) {
        if (event.key === "r" || event.key === "R") {
            popupMessage.style.display = "none";
            initializeGame();
        } else if (event.key === "q" || event.key === "Q") {
            window.location.reload();
        }
    }
});

// Start the game
initializeGame();
