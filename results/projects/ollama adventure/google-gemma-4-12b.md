# Gemma 4 12B
Model: google/gemma-4-12b
Test: ollamas adventure
Created: 11/03/2026, 12:59:11 AM
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

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama's Adventure</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #f0e6ff;
            font-family: 'Fredoka+One', cursive;
        }

        #game-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(to bottom, #a1c4fd 0%, #c2e9fb 100%);
        }

        canvas {
            display: block;
            background: #87CEEB;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            max-width: 100%;
            max-height: 100%;
        }

        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }

        .menu {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 30px;
            border: 5px solid #6c5ce7;
            pointer-events: auto;
        }

        h1 { color: #6c5ce7; font-size: 3rem; margin-bottom: 10px; }
        p { color: #444; font-size: 1.2rem; }

        button {
            padding: 15px 40px;
            font-size: 1.5rem;
            background-color: #6c5ce7;
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, background-color 0.2s;
        }

        button:hover {
            background-color: #a29bfe;
            transform: scale(1.1);
        }

        #score-hud {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 2rem;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        #game-over-screen { display: none; }
    </style>
</head>
<body>>

<div id="game-container">
    <canvas id="gameCanvas"></canvas>
    <div id="ui-layer">
        <div id="score-hud">Score: 0</div>
        
        <!-- Start Menu -->
        <div id="start-menu" class="menu">
            <h1>Ollama's Adventure</h1>
            <p>Help the alpaca jump over cacti!</p>
            <p style="font-size: 1rem;">Space or Click to Jump</p>
            <button onclick="startGame()">START GAME</button>
        </div>

        <!-- Game Over Menu -->
        <div id="game-over-screen" class="menu">
            <h1>Oh No!</h1>
            <p>Final Score: <span id="final-score">0</span></p>
            <p>High Score: <span id="high-score">0</span></p>
            <button onclick="startGame()">TRY AGAIN</button>
        </div>
    </div>
</div>

<script>
/** 
 * GAME CONFIGURATION & STATE
 */
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score-hud');
const startMenu = document.getElementById('start-menu');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreElement = document.getElementById('final-score');
const highscoreElement = document.getElementById('high-score');

// Resize canvas to fit window
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = Math.min(window.innerHeight, 600);
}
window.addEventListener('resize', resize);
resize();

let gameActive = false;
let score = 0;
let highscore = localStorage.getItem('alpaca_highscore') || 0;
let gameSpeed = 5;
let frameCount = 0;

// Game Objects
const player = {
    x: 100,
    y: 0,
    width: 80,
    height: 80,
    dy: 0,
    jumpForce: -15,
    gravity: 0.6,
    grounded: false,
    draw() {
        // Draw Alpaca (simplified cartoon style)
        ctx.save();
        ctx.translate(this.x, this.y);
        
        // Body/Neck
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.ellipse(40, 40, 35, 45, Math.PI / 10, 0, Math.PI * 2);
        ctx.fill();
        
        // Head
        ctx.beginPath();
        ctx.arc(65, 15, 20, 0, Math.PI * 2);
        ctx.fill();

        // Ear
        ctx.fillStyle = '#f9f9f9';
        ctx.beginPath();
        ctx.ellipse(60, 0, 8, 15, -0.3, 0, Math.PI*2);
        ctx.fill();

        // Eye
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(72, 12, 3, 0, Math.PI * 2);
        ctx.fill();

        // Muzzle (the "fluff")
        ctx.fillStyle = '#eee';
        ctx.beginPath();
        ctx.ellipse(80, 25, 10, 12, 0, 0, Math.PI * 2);
        ctx.fill();

        // Mane (the woolly hair)
        ctx.strokeStyle = '#f3e5fc';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(40, 10);
        ctx.quadraticCurveTo(20, 30, 30, 60);
        ctx.stroke();

        ctx.restore();
    }
};

let obstacles = [];
const backgrounds = [
    { x: 0, speed: 0.5, color: '#87CEEB' }, // Clouds/Sky layer (Simulated with colors)
    { x: 0, speed: 2, color: '#90EE90' }     // Grass layer
];

/**
 * AUDIO ENGINE (Web Audio API)
 */
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function playTone(freq, type, duration) {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
}

function playJump() { playTone(400, 'square', 0.1); }
function playScore() { playTone(800, 'sine', 0.1); }
function playHit() { playTone(150, 'sawtooth', 0.3); }

/**
 * GAME LOGIC
 */
function startGame() {
    gameActive = true;
    score = 0;
    gameSpeed = 6;
    obstacles = [];
    player.y = canvas.height - 150;
    player.dy = 0;
    startMenu.style.display = 'none';
    gameOverScreen.style.display = 'none';
    requestAnimationFrame(gameLoop);
}

function update() {
    frameCount++;
    score += 0.1;
    scoreElement.innerText = `Score: ${Math.floor(score)}`;
    
    // Speed up gradually
    gameSpeed += 0.001;

    // Physics
    player.dy += player.gravity;
    player.y += player.dy;

    const groundY = canvas.height - 120;
    if (player.y > groundY) {
        player.y = groundY;
        player.dy = 0;
        player.grounded = true;
    } else {
        player.grounded = false;
    }

    // Obstacles
    if (frameCount % Math.floor(120 / (gameSpeed/5)) === 0) {
        obstacles.push({ x: canvas.width, y: groundY + 20 - 40, w: 40, h: 40 });
    }

    obstacles.forEach((obs, i) => {
        obs.x -= gameSpeed;
        // Collision detection
        if (
            player.x < obs.x + obs.w &&
            player.x + player.width > obs.x &&
            player.y < obs.y + obs.h &&
            player.y + player.height > obs.y
        ) {
            gameOver();
        }
        // Remove off-screen
        if (obs.x < -100) obstacles.splice(i, 1);
    });

    // Parallax Backgrounds
    backgrounds.forEach((bg, i) => {
        bg.x -= bg.speed;
        if (bg.x <= -canvas.width) bg.x = 0;
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Background Layers
    backgrounds.forEach((bg, i) => {
        ctx.fillStyle = (i === 1) ? '#7cfc00' : '#98fb98'; // Grass vs Distant Hills
        ctx.fillRect(bg.x, canvas.height - 120, canvas.width, 120);
        ctx.fillRect(bg.x + canvas.width, canvas.height - 120, canvas.width, 120);
    });

    // Draw Ground Line
    ctx.fillStyle = '#5d4037';
    ctx.fillRect(0, canvas.height - 50, canvas.width, 50);

    // Draw Obstacles (Cacti)
    obstacles.forEach(obs => {
        ctx.fillStyle = '#2e7d32';
        ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
        // Add some "cactus" spikes
        ctx.strokeStyle = '#1b5e20';
        ctx.lineWidth = 2;
        ctx.strokeRect(obs.x, obs.y, obs.w, obs.h);
    });

    player.draw();
}

function gameLoop() {
    if (!gameActive) return;
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

function gameOver() {
    gameActive = false;
    playHit();
    
    if (score > highscore) {
        highscore = Math.floor(score);
        localStorage.setItem('alpaca_highscore', highscore);
    }
    
    finalScoreElement.innerText = Math.floor(score);
    highscoreElement.innerText = highscore;
    gameOverScreen.style.display = 'block';
}

/**
 * INPUTS
 */
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        if (player.grounded && gameActive) {
            player.dy = player.jumpForce;
            playJump();
        }
    }
});

window.addEventListener('touchstart', () => {
    if (player.grounded && gameActive) {
        player.dy = player.jumpForce;
        playJump();
    }
}, {passive: false});

// Simple loop for "score point" sound occasionally
setInterval(() => {
    if (gameActive && Math.random() > 0.8) playScore();
}, 3000);

</script>
</body>
</html>
```

78 t/s, 3125 tokens, 40s
