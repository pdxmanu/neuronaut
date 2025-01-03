let cards = [];
let flippedCards = [];
let score = 0;
let startTime = null;
let gameInterval = null;

// Initialize the card values and shuffle them
function initializeCards() {
    const cardValues = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8];
    shuffle(cardValues);
    cards = cardValues.map((value, index) => ({
        value,
        id: index,
        flipped: false,
        matched: false
    }));
}

// Shuffle an array using Fisher-Yates shuffle algorithm
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Create the card elements in the DOM
function createCardElements() {
    const gameGrid = document.getElementById('game-grid');
    gameGrid.innerHTML = ''; // Clear the grid

    cards.forEach(card => {
        const cardElement = document.createElement('div');
        cardElement.classList.add('card');
        cardElement.setAttribute('data-id', card.id);
        cardElement.addEventListener('click', flipCard);
        gameGrid.appendChild(cardElement);
    });
}

// Flip the card and check for matches
function flipCard() {
    if (flippedCards.length === 2) return;

    const cardElement = this;
    const cardId = cardElement.getAttribute('data-id');
    const card = cards[cardId];

    if (card.flipped || card.matched) return;

    card.flipped = true;
    cardElement.classList.add('flipped');
    cardElement.textContent = card.value;
    flippedCards.push(card);

    if (flippedCards.length === 2) {
        checkForMatch();
    }
}

// Check if the flipped cards match
function checkForMatch() {
    const [card1, card2] = flippedCards;
    const cardElements = document.querySelectorAll('.card');

    if (card1.value === card2.value) {
        card1.matched = true;
        card2.matched = true;
        updateScore();
    } else {
        setTimeout(() => {
            card1.flipped = false;
            card2.flipped = false;
            cardElements[card1.id].classList.remove('flipped');
            cardElements[card2.id].classList.remove('flipped');
            cardElements[card1.id].textContent = '';
            cardElements[card2.id].textContent = '';
        }, 1000);
    }

    flippedCards = [];

    if (cards.every(card => card.matched)) {
        endGame();
    }
}

// Update the score
function updateScore() {
    score += 1;
    document.getElementById('score').textContent = score;
}

// Start the game
function startGame() {
    score = 0;
    document.getElementById('score').textContent = score;
    startTime = new Date();
    initializeCards();
    createCardElements();

    if (gameInterval) clearInterval(gameInterval);
    gameInterval = setInterval(updateTime, 1000);
}

// Update the game time
function updateTime() {
    const timeElapsed = Math.floor((new Date() - startTime) / 1000);
    document.getElementById('time').textContent = timeElapsed;
}

// End the game
function endGame() {
    clearInterval(gameInterval);
    alert(`Game Over! Your score: ${score}`);
}

// Initialize the game
document.getElementById('start-button').addEventListener('click', startGame);
