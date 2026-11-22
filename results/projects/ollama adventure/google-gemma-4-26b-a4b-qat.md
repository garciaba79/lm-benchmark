# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: ollamas adventure
Created: 11/22/2026, 03:05:00 AM
Exported from: LM Studio (via test script)
Context 16K

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

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama's Adventure</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #222;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
            user-select: none;
        }
        #game-container {
            position: relative;
            width: 800px;
            height: 400px;
            box-shadow: 0 0 50px rgba(0,0,0,0.5);
            border: 4px solid #444;
            background: #87CEEB; /* Sky color */
        }
        canvas {
            display: block;
        }
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        #hud {
            position: absolute;
            top: 10px;
            width: 100%;
            display: flex;
            justify-content: space-around;
            font-size: 24px;
            font-weight: bold;
            pointer-events: none;
        }
        #menu {
            background: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            pointer-events: auto;
            display: block;
        }
        h1 { margin: 0 0 10px 0; color: #ffeb3b; font-size: 42px; }
        p { margin: 5px 0 20px 0; font-size: 18px; }
        button {
            padding: 12px 30px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50px;
            transition: transform 0.1s, background 0.2s;
        }
        button:hover { background-color: #45a049; transform: scale(1.1); }
        button:active { transform: scale(0.95); }
        .hidden { display: none !important; }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="800" height="400"></canvas>
    <div id="hud">
        <div id="score-display">Score: 0</div>
        <div id="highscore-display">High Score: 0</div>
    </div>
    <div id="ui-layer">
        <div id="menu">
            <h1 id="menu-title">Ollama's Adventure</h1>
            <p id="menu-subtext">Avoid the cacti!</p>
            <div id="final-score" style="margin-bottom: 15px; font-size: 24px;"></div>
            <button id="start-btn">PLAY</button>
        </div>
    </div>
</div>

<script>
/** 
 * AUDIO ENGINE (Web Audio API)
 */
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(freq, type, duration, volume) {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + duration);
    gain.gain.setValueAtTime(volume, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
}

const sounds = {
    jump: () => playSound(400, 'triangle', 0.3, 0.2),
    point: () => playSound(800, 'sine', 0.2, 0.1),
    hit: () => playSound(150, 'sawtooth', 0.5, 0.3)
};

/**
 * GAME LOGIC
 */
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const menu = document.getElementById('menu');
const menuTitle = document.getElementById('menu-title');
const menuSubtext = document.getElementById('menu-subtext');
const finalScoreDisplay = document.getElementById('final-score');
const scoreDisplay = document.getElementById('score-display');
const highscoreDisplay = document.getElementById('highscore-display');

// Game State
let gameState = 'START'; // START, PLAYING, GAMEOVER
let score = 0;
let highscore = localStorage.getItem('ollama_highscore') || 0;
let gameSpeed = 4;
let frameCount = 0;

highscoreDisplay.innerText = `High Score: ${highscore}`;

// Player Object
const alpaca = {
    x: 100,
    y: 300,
    width: 50,
    height: 50,
    dy: 0,
    jumpForce: 13,
    gravity: 0.6,
    grounded: false,
    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        
        // Body (Fluffy white shape)
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.ellipse(25, 25, 25, 20, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Neck/Head
        ctx.fillStyle = '#F0F0F0';
        ctx.fillRect(35, 5, 15, 25);
        ctx.beginPath();
        ctx.ellipse(45, 10, 12, 15, 0, 0, Math.PI * 2);
        ctx.fill();

        // Eyes
        ctx.fillStyle = '#000';
        ctx.fillRect(48, 5, 3, 3);
        
        // Ears
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.ellipse(40, 0, 5, 10, -0.5, 0, Math.PI * 2);
        ctx.ellipse(50, 0, 5, 10, 0.5, 0, Math.PI * 2);
        ctx.fill();

        // Legs (simple rectangles)
        ctx.fillStyle = '#DDD';
        ctx.fillRect(15, 40, 8, 12);
        ctx.fillRect(30, 40, 8, 12);

        ctx.restore();
    }
};

// Obstacles
let obstacles = [];
function spawnObstacle() {
    const height = 30 + Math.random() * 30;
    obstacles.push({
        x: canvas.width + 50,
        y: 350 - height,
        width: 30,
        height: height,
        color: '#2E7D32'
    });
}

// Background Layers
const clouds = [];
const mountains = [];
function initBackground() {
    for(let i=0; i<5; i++) {
        clouds.push({ x: Math.random()*canvas.width, y: 50 + Math.random()*100, w: 60 + Math.random()*40, speed: 0.5 });
        mountains.push({ x: Math.random()*canvas.width, w: 150 + Math.random()*100, h: 100 + Math.random()*100, speed: 1 });
    }
}
initBackground();

function drawBackground() {
    // Sky
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Distant Mountains (Parallax 1)
    ctx.fillStyle = '#A5D6A7';
    mountains.forEach(m => {
        ctx.beginPath();
        ctx.moveTo(m.x - m.w/2, 350);
        ctx.lineTo(m.x, 350 - m.h);
        ctx.lineTo(m.x + m.w/2, 350);
        ctx.fill();
        m.x -= m.speed * (gameSpeed * 0.2);
        if(m.x < -100) m.x = canvas.width + 100;
    });

    // Clouds (Parallax 2)
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    clouds.forEach(c => {
        ctx.beginPath();
        ctx.arc(c.x, c.y, c.w/2, 0, Math.PI*2);
        ctx.arc(c.x + c.w/3, c.y - 10, c.w/2.5, 0, Math.PI*2);
        ctx.arc(c.x + c.w/1.5, c.y, c.w/2.2, 0, Math.PI*2);
        ctx.fill();
        c.x -= c.speed * (gameSpeed * 0.5);
        if(c.x < -100) c.x = canvas.width + 100;
    });

    // Ground
    ctx.fillStyle = '#795548'; // Dirt
    ctx.fillRect(0, 350, canvas.width, 50);
    ctx.fillStyle = '#4CAF50'; // Grass top
    ctx.fillRect(0, 350, canvas.width, 10);
}

function update() {
    if (gameState !== 'PLAYING') return;

    frameCount++;
    gameSpeed += 0.0005; // Gradually increase speed

    // Alpaca Physics
    alpaca.dy += alpaca.gravity;
    alpaca.y += alpaca.dy;

    if (alpaca.y + alpaca.height > 350) {
        alpaca.y = 350 - alpaca.height;
        alpaca.dy = 0;
        alpaca.grounded = true;
    } else {
        alpaca.grounded = false;
    }

    // Obstacles logic
    if (frameCount % Math.max(40, Math.floor(120 / (gameSpeed/4))) === 0) {
        spawnObstacle();
    }

    for (let i = obstacles.length - 1; i >= 0; i--) {
        let o = obstacles[i];
        o.x -= gameSpeed;

        // Collision Detection (AABB)
        if (
            alpaca.x < o.x + o.width &&
            alpaca.x + alpaca.width * 0.7 > o.x && // Hitbox slightly smaller for fairness
            alpaca.y < o.y + o.height &&
            alpaca.y + alpaca.height > o.y
        ) {
            gameOver();
        }

        // Score increment (distance)
        if (!o.passed && o.x + o.width < alpaca.x) {
            o.passed = true;
            score += 10;
            scoreDisplay.innerText = `Score: ${score}`;
            sounds.point();
        }

        if (o.x + o.width < 0) obstacles.splice(i, 1);
    }

    // Update Score display based on time for "endless" feel
    if(frameCount % 60 === 0) score++; 
    scoreDisplay.innerText = `Score: ${score}`;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBackground();

    // Draw Obstacles (Cactus-ish)
    obstacles.forEach(o => {
        ctx.fillStyle = o.color;
        // Main stem
        ctx.fillRect(o.x, o.y, o.width, o.height);
        // Little cactus arms
        ctx.fillRect(o.x - 10, o.y + 10, 10, 5);
        ctx.fillRect(o.x + o.width, o.y + 15, 10, 5);
        ctx.fillRect(o.x - 10, o.y + 20, 5, 10);
    });

    alpaca.draw();
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

function jump() {
    if (alpaca.grounded && gameState === 'PLAYING') {
        alpaca.dy = -alpaca.jumpForce;
        alpaca.grounded = false;
        sounds.jump();
    }
}

function gameOver() {
    gameState = 'GAMEOVER';
    sounds.hit();
    
    if (score > highscore) {
        highscore = score;
        localStorage.setItem('ollama_highscore', highscore);
        highscoreDisplay.innerText = `High Score: ${highscore}`;
    }

    menuTitle.innerText = "Game Over!";
    menuSubtext.innerText = `You traveled ${score} meters!`;
    finalScoreDisplay.innerText = `Score: ${score}`;
    startBtn.innerText = "RETRY";
    menu.classList.remove('hidden');
}

function resetGame() {
    score = 0;
    gameSpeed = 4;
    obstacles = [];
    alpaca.y = 300;
    alpaca.dy = 0;
    frameCount = 0;
    scoreDisplay.innerText = "Score: 0";
    gameState = 'PLAYING';
    menu.classList.add('hidden');
    
    // Audio Context needs interaction to resume
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
}

// Input Listeners
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.code === 'ArrowUp') {
        e.preventDefault();
        if (gameState === 'PLAYING') jump();
        else if (gameState !== 'PLAYING') resetGame();
    }
});

canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    if (gameState === 'PLAYING') jump();
});

canvas.addEventListener('mousedown', () => {
    if (gameState === 'PLAYING') jump();
});

startBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent clicking button from triggering jump
    resetGame();
});

// Start the loop
gameLoop();

</script>
</body>
</html>
```

51 t/s, 3796 tokens, 75s, 25%
