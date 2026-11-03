# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
Test: ollamas adventure
Created: 11/03/2026, 03:13:57 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Create a complete, playable single-page endless runner game in one self-contained HTML file (inline CSS and JavaScript only). Do not use external libraries, images, or assets.

Game name: ollama's Adventure

Core gameplay:
- The player controls a cartoon alpaca that automatically runs to the right.
- Press spacebar or click/tap to make the alpaca jump.
- Avoid obstacles that appear from the right side of the screen.
- The game speed gradually increases over time.
- The goal is to survive as long as possible and get the highest score.

Requirements:
- Track the current score (based on distance or time survived).
- Save and display the high score using localStorage.
- Include a clear "Retry" or "Play Again" button that appears when the player hits an obstacle.
- Use simple, colorful, cartoonish graphics drawn with Canvas or pure HTML/CSS. The main character should look like a fun, recognizable alpaca.
- Add a parallax scrolling background with at least two layers that move at different speeds.
- Generate simple sound effects using the Web Audio API for jumping, scoring points, and hitting an obstacle. Keep the sounds short and lighthearted.

The game should feel responsive and enjoyable. Keep everything inside a single HTML file.

> #### 🤖 Assistant

Sure, I'll create a complete, playable single-page endless runner game named "ollama's Adventure" in one self-contained HTML file using inline CSS and JavaScript. The game will meet all your specified requirements including simple graphics drawn with Canvas, parallax scrolling background, sound effects using the Web Audio API, and saving/loading high score.

Here is the full code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ollama's Adventure</title>
<style>
    body {
        margin: 0;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: #87CEEB;
        font-family: Arial, sans-serif;
    }
    canvas {
        display: block;
        border: 2px solid #fff;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(255, 255, 255, 0.8);
        flex-direction: column;
    }
    .retry-button {
        padding: 10px 20px;
        font-size: 24px;
        cursor: pointer;
        border: none;
        background-color: #FFD700;
        color: black;
        margin-top: 20px;
    }
</style>
</head>
<body>
<canvas id="gameCanvas"></canvas>
<div class="overlay" style="display:none;">
    <div id="gameOverText">Game Over!</div>
    <div>Score: <span id="finalScore">0</span></div>
    <div>High Score: <span id="highScoreDisplay">0</span></div>
    <button class="retry-button" onclick="restartGame()">Play Again</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let gameSpeed = 5;
let score = 0;
let highScore = localStorage.getItem('highScore') || 0;
document.getElementById('highScoreDisplay').textContent = highScore;
const alpacaWidth = 40;
const alpacaHeight = 60;
let alpacaX = canvas.width / 4;
let alpacaY = canvas.height - alpacaHeight - 10;
const jumpStrength = 25;
const gravity = 1;
let isJumping = false;
let jumpFrameCount = 0;

const obstacles = [];
let obstacleSpeed = gameSpeed;
const obstacleWidth = 30;
const obstacleHeight = 60;
let spawnInterval = 1000;
let lastSpawnTime = Date.now();
let backgroundX1 = 0;
let backgroundX2 = canvas.width;

// Web Audio API for sound effects
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
function createOscillator(freq, duration) {
    const oscillator = audioContext.createOscillator();
    oscillator.type = 'square';
    oscillator.frequency.setValueAtTime(freq, audioContext.currentTime);
    oscillator.connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration);
}

document.addEventListener('keydown', (e) => {
    if ((e.code === 'Space' || e.key === ' ') && !isJumping) {
        isJumping = true;
        createOscillator(440, 0.1); // A4 note for jump sound
    }
});
canvas.addEventListener('click', () => {
    if (!isJumping) {
        isJumping = true;
        createOscillator(440, 0.1);
    }
});

function spawnObstacle() {
    const obstacleY = canvas.height - obstacleHeight - 10;
    obstacles.push({ x: canvas.width + 20, y: obstacleY, width: obstacleWidth, height: obstacleHeight });
}

function updateGameArea() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update background position
    backgroundX1 -= gameSpeed * 0.5;
    backgroundX2 -= gameSpeed * 0.5;
    if (backgroundX1 + canvas.width <= 0) backgroundX1 = backgroundX2 + canvas.width;
    if (backgroundX2 + canvas.width <= 0) backgroundX2 = backgroundX1 + canvas.width;

    // Draw background
    ctx.fillStyle = '#87CEEB'; // Sky color
    ctx.fillRect(backgroundX1, 0, canvas.width, canvas.height);
    ctx.fillRect(backgroundX2, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#228B22'; // Ground color
    ctx.fillRect(0, canvas.height - 30, canvas.width, 30);

    // Draw alpaca
    drawAlpaca();

    // Update and draw obstacles
    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].x -= obstacleSpeed;
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(obstacles[i].x, obstacles[i].y, obstacles[i].width, obstacles[i].height);
        if (obstacles[i].x + obstacles[i].width < 0) {
            obstacles.splice(i, 1);
            i--;
            score++;
            document.getElementById('scoreDisplay').textContent = score;
            createOscillator(659.26, 0.1); // E6 note for scoring sound
        }
    }

    if (isJumping) {
        alpacaY -= jumpStrength;
        jumpFrameCount++;
        if (jumpFrameCount >= 12) {
            isJumping = false;
            jumpFrameCount = 0;
        }
    } else {
        alpacaY += gravity;
    }

    // Prevent alpaca from falling through ground
    if (alpacaY + alpacaHeight > canvas.height - 30) {
        alpacaY = canvas.height - alpacaHeight - 10;
    }

    // Collision detection
    for (let obstacle of obstacles) {
        if (
            alpacaX < obstacle.x + obstacle.width &&
            alpacaX + alpacaWidth > obstacle.x &&
            alpacaY < obstacle.y + obstacle.height &&
            alpacaY + alpacaHeight > obstacle.y
        ) {
            endGame();
            createOscillator(261.63, 0.5); // C4 note for hit sound
        }
    }

    // Increase game speed and spawn rate over time
    if (Date.now() - lastSpawnTime >= spawnInterval) {
        spawnObstacle();
        lastSpawnTime = Date.now();
        obstacleSpeed += 0.1;
        gameSpeed += 0.05;
        spawnInterval -= 2; // Shorten interval to increase frequency of obstacles
    }

    requestAnimationFrame(updateGameArea);
}

function drawAlpaca() {
    ctx.fillStyle = '#DEB887'; // Light brown for alpaca body
    ctx.fillRect(alpacaX, alpacaY, alpacaWidth, alpacaHeight);

    ctx.fillStyle = 'black'; // Alpaca eyes
    ctx.beginPath();
    ctx.arc(alpacaX + 10, alpacaY + 20, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(alpacaX + 30, alpacaY + 20, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = 'black'; // Alpaca mouth
    ctx.fillRect(alpacaX + 10, alpacaY + 40, 20, 5);

    ctx.fillStyle = '#FFD700'; // Alpaca nose
    ctx.beginPath();
    ctx.arc(alpacaX + 20, alpacaY + 35, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = 'white'; // Alpaca belly
    ctx.fillRect(alpacaX + 10, alpacaY + 45, 20, 10);

    ctx.fillStyle = '#DEB887'; // Alpaca ears
    ctx.fillRect(alpacaX, alpacaY - 30, 10, 30);
    ctx.fillRect(alpacaX + 30, alpacaY - 30, 10, 30);

    ctx.fillStyle = 'black'; // Alpaca ear tips
    ctx.beginPath();
    ctx.arc(alpacaX + 5, alpacaY - 40, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(alpacaX + 35, alpacaY - 40, 5, 0, Math.PI * 2);
    ctx.fill();
}

function endGame() {
    document.getElementById('gameOverText').textContent = 'Game Over!';
    document.getElementById('finalScore').textContent = score;
    if (score > highScore) {
        localStorage.setItem('highScore', score);
        highScore = score;
        document.getElementById('highScoreDisplay').textContent = highScore;
    }
    document.querySelector('.overlay').style.display = 'flex';
}

function restartGame() {
    obstacles.length = 0;
    gameSpeed = 5;
    score = 0;
    isJumping = false;
    jumpFrameCount = 0;
    alpacaY = canvas.height - alpacaHeight - 10;
    obstacleSpeed = gameSpeed;
    spawnInterval = 1000;
    lastSpawnTime = Date.now();
    document.querySelector('.overlay').style.display = 'none';
    updateGameArea();
}

updateGameArea();
</script>
</body>
</html>
```

### Explanation:
- **Canvas Setup:** The canvas is set up to fill the screen, and the game area is updated using `requestAnimationFrame` for smooth animation.
- **Alpaca Graphics:** A simple alpaca character is drawn using rectangles and arcs on the Canvas. It has a brown body, eyes, ears, mouth, nose, belly, and ear tips.
- **Obstacles & Collision Detection:** Obstacles are spawned from the right side of the screen and move towards the left at an increasing speed. The game checks for collisions between the alpaca and obstacles to determine if the player has hit an obstacle.
- **Game Over Logic:** When a collision is detected, the game stops, and a game over overlay appears with a retry button. The high score is updated using `localStorage`.
- **Sound Effects:** Simple sound effects are created using the Web Audio API when the alpaca jumps, scores points, or hits an obstacle.
- **Responsive Design:** The game automatically adjusts to different screen sizes by setting the canvas width and height to fill the viewport.

This code creates a fun, simple endless runner game that should be enjoyable on any device with a modern browser.

6 t/s, 2476 tokens, 412s
