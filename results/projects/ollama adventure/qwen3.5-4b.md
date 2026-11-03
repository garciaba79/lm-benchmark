# Qwen3.5 4B
Model: qwen3.5-4b
Test: ollamas adventure
Created: 11/03/2026, 12:20:42 AM
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

Here is the complete, self-contained HTML file for **Ollama's Adventure**.

You can save this code as `index.html` and open it in any modern web browser to play. It includes no external dependencies, uses the Web Audio API for sound generation, and features a custom Canvas-based rendering engine.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama's Adventure</title>
    <style>
        :root {
            --primary: #FF9F1C;
            --secondary: #2EC4B6;
            --accent: #E71D36;
            --text: #011627;
        }

        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: var(--secondary);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            touch-action: none; /* Prevent zoom/scroll on mobile */
        }

        #game-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        canvas {
            background: linear-gradient(to bottom, #87CEEB, #E0F7FA);
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }

        /* UI Overlay */
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none; /* Let clicks pass through to canvas/buttons */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .hud {
            padding: 20px;
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            color: var(--text);
            text-shadow: 1px 1px 0px rgba(255,255,255,0.8);
            font-size: 24px;
        }

        .score-box span {
            display: inline-block;
            margin-left: 10px;
        }

        /* Screens (Start / Game Over) */
        .screen {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            pointer-events: auto;
            display: none; /* Hidden by default */
        }

        .screen.active {
            display: block;
        }

        h1 {
            color: var(--accent);
            margin-top: 0;
            font-size: 48px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        p {
            color: #555;
            font-size: 18px;
        }

        button {
            background-color: var(--primary);
            border: none;
            padding: 15px 30px;
            font-size: 24px;
            color: white;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 20px;
            transition: transform 0.1s, background-color 0.2s;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        button:hover {
            background-color: #ffad33;
            transform: scale(1.05);
        }

        button:active {
            transform: scale(0.95);
        }

        .controls-hint {
            margin-top: 20px;
            font-size: 14px;
            color: #888;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas"></canvas>
    
    <div id="ui-layer">
        <div class="hud" style="display:none;" id="hud">
            <div class="score-box">SCORE: <span id="scoreVal">0</span></div>
            <div class="score-box">HIGH SCORE: <span id="highScoreVal">0</span></div>
        </div>

        <!-- Start Screen -->
        <div id="start-screen" class="screen active">
            <h1>Ollama's Adventure</h1>
            <p>Help Ollama the Alpaca avoid obstacles!</p>
            <button id="start-btn">Play Now</button>
            <div class="controls-hint">Press Space or Click to Jump</div>
        </div>

        <!-- Game Over Screen -->
        <div id="game-over-screen" class="screen">
            <h1>Oof!</h1>
            <p>You hit an obstacle.</p>
            <p>Score: <span id="final-score">0</span></p>
            <button id="restart-btn">Try Again</button>
        </div>
    </div>
</div>

<script>
/**
 * GAME CONFIGURATION & STATE
 */
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game State
let gameState = 'START'; // START, PLAYING, GAMEOVER
let framesPerSecond = 60;
let gameSpeed = 5;
let score = 0;
let highScore = localStorage.getItem('ollamaHighScore') || 0;
let frameCount = 0;

// Audio Context (Web Audio API)
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

/**
 * RESIZE HANDLING
 */
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

/**
 * AUDIO SYSTEM (Synthesizer)
 */
function playSound(type) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    
    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    const now = audioCtx.currentTime;

    if (type === 'jump') {
        // Bouncy jump sound
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(600, now + 0.1);
        gainNode.gain.setValueAtTime(0.3, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
    } else if (type === 'score') {
        // High pitch ding
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(800, now);
        gainNode.gain.setValueAtTime(0.1, now);
        gainNode.gain.linearRampToValueAtTime(0, now + 0.5);
        osc.start(now);
        osc.stop(now + 0.5);
    } else if (type === 'crash') {
        // Low thud
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.3);
        gainNode.gain.setValueAtTime(0.5, now);
        gainNode.gain.linearRampToValueAtTime(0, now + 0.5);
        osc.start(now);
        osc.stop(now + 0.5);
    }
}

/**
 * GAME OBJECTS
 */

// The Player (Alpaca)
const player = {
    x: 100,
    y: 0, // Set in update
    width: 60,
    height: 40,
    dy: 0,
    jumpForce: 12,
    gravity: 0.8,
    grounded: false,
    
    draw() {
        ctx.save();
        
        // Body (Cream/White)
        ctx.fillStyle = '#FFFDD0'; 
        ctx.beginPath();
        ctx.roundRect(this.x, this.y + 15, this.width, this.height - 15, 10);
        ctx.fill();

        // Ears (Pinkish)
        ctx.fillStyle = '#FFB7C5';
        ctx.beginPath();
        ctx.moveTo(this.x + 5, this.y + 20);
        ctx.lineTo(this.x + 15, this.y - 5);
        ctx.lineTo(this.x + 30, this.y + 20);
        ctx.fill();

        // Face (Pink)
        ctx.fillStyle = '#FFC0CB';
        ctx.beginPath();
        ctx.arc(this.x + 28, this.y + 18, 15, 0, Math.PI * 2);
        ctx.fill();

        // Eyes
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(this.x + 34, this.y + 16, 2, 0, Math.PI * 2);
        ctx.fill();

        // Blush
        ctx.fillStyle = '#FF9F1C';
        ctx.globalAlpha(0.5);
        ctx.beginPath();
        ctx.arc(this.x + 34, this.y + 20, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha(1.0);

        // Legs (Animated)
        if (this.grounded && gameState === 'PLAYING') {
            // Run animation logic handled in draw loop based on frameCount
            const legOffset = Math.sin(frameCount * 0.2) * 5;
            
            ctx.fillStyle = '#333';
            ctx.beginPath();
            ctx.moveTo(this.x + 10, this.y + 40);
            ctx.lineTo(this.x + 8, this.y + 40 - legOffset); // Left back
            ctx.lineTo(this.x + 25, this.y + 40 - (legOffset * 3)); // Right front
            ctx.lineTo(this.x + 15, this.y + 40);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(this.x + 40, this.y + 40);
            ctx.lineTo(this.x + 42, this.y + 40 - (legOffset * 3)); // Right back
            ctx.lineTo(this.x + 58, this.y + 40 - legOffset); // Left front
            ctx.fill();
        } else {
            // Jump pose
            ctx.fillStyle = '#333';
            ctx.fillRect(this.x + 12, this.y + 35, 6, 10);
            ctx.fillRect(this.x + 42, this.y + 35, 6, 10);
        }

        // Tail
        ctx.fillStyle = '#FFFDD0';
        ctx.beginPath();
        ctx.moveTo(this.x - 5, this.y + 25);
        ctx.lineTo(this.x - 15, this.y + 30);
        ctx.fill();

        ctx.restore();
    },

    update() {
        // Apply Gravity
        if (this.dy > 0) {
            this.dy += this.gravity;
            this.grounded = false;
        } else {
            this.grounded = true;
        }

        this.y += this.dy;

        // Floor Collision
        const floorY = canvas.height - 100;
        if (this.y > floorY) {
            this.y = floorY;
            this.dy = 0;
        }
    },

    jump() {
        if (this.grounded && gameState === 'PLAYING') {
            this.dy = -this.jumpForce;
            playSound('jump');
        }
    }
};

// Obstacles Manager
let obstacles = [];
const obstacleTypes = ['rock', 'cactus']; // Simple shapes

class Obstacle {
    constructor() {
        this.w = 40 + Math.random() * 30;
        this.h = 40 + Math.random() * 40;
        this.x = canvas.width + this.w;
        this.y = canvas.height - 100 - this.h; // Ground level
        this.markedForDeletion = false;
        
        // Randomly choose type (simplified here to just shapes)
        this.type = Math.random() > 0.5 ? 'rock' : 'cactus';
    }

    update() {
        this.x -= gameSpeed;
        if (this.x + this.w < 0) {
            this.markedForDeletion = true;
        }
    }

    draw() {
        ctx.save();
        
        // Shadow
        ctx.fillStyle = 'rgba(0,0,0,0.2)';
        ctx.beginPath();
        ctx.ellipse(this.x + 15, this.y + 35, 20, 8, 0, 0, Math.PI * 2);
        ctx.fill();

        if (this.type === 'rock') {
            // Draw Rock
            ctx.fillStyle = '#7F8C8D';
            ctx.beginPath();
            ctx.moveTo(this.x + 15, this.y + 35);
            ctx.lineTo(this.x + 40, this.y + 20);
            ctx.lineTo(this.x + 10, this.y + 10);
            ctx.fill();
            
            // Detail
            ctx.fillStyle = '#95A5A6';
            ctx.beginPath();
            ctx.arc(this.x + 30, this.y + 25, 8, 0, Math.PI*2);
            ctx.fill();

        } else {
            // Draw Cactus
            ctx.fillStyle = '#27AE60';
            ctx.fillRect(this.x + 10, this.y + 15, 20, 20); // Body
            
            // Arms
            ctx.fillRect(this.x - 5, this.y + 10, 10, 30); // Left arm
            ctx.fillRect(this.x + 35, this.y + 10, 10, 30); // Right arm
            
            // Top hat
            ctx.fillStyle = '#2ECC71';
            ctx.beginPath();
            ctx.moveTo(this.x - 5, this.y + 40);
            ctx.lineTo(this.x + 35, this.y + 40);
            ctx.lineTo(this.x + 20, this.y + 25);
            ctx.fill();
        }

        ctx.restore();
    }
}

// Background Manager (Parallax)
const bgLayers = [
    { speed: 1, color: '#87CEEB', height: canvas.height - 100 }, // Sky is handled by CSS gradient mostly, but we draw clouds
    { speed: 2, type: 'cloud' }
];

function drawBackground() {
    // Draw Mountains (Far)
    ctx.fillStyle = '#A8DADC';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height - 100);
    for(let i=0; i<=canvas.width; i+=50) {
        ctx.lineTo(i + 25, canvas.height - 300 - Math.sin((i/20)*0.01)*50);
        ctx.lineTo(i + 50, canvas.height - 100);
    }
    ctx.fill();

    // Draw Clouds (Mid)
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    let cloudOffset = (frameCount * bgLayers[1].speed) % canvas.width;
    
    function drawCloud(x) {
        ctx.beginPath();
        ctx.arc(x, 100 - Math.sin((x/100)*0.2)*30, 40, 0, Math.PI*2);
        ctx.arc(x + 50, 90 - Math.cos((x/100)*0.2)*30, 50, 0, Math.PI*2);
        ctx.arc(x + 100, 100 - Math.sin((x/100)*0.2)*30, 40, 0, Math.PI*2);
        ctx.fill();
    }

    // Infinite Cloud Loop
    for(let i = -1; i < canvas.width / 60 + 1; i++) {
        drawCloud(i * 80 - cloudOffset);
    }
}

/**
 * GAME LOGIC
 */

function spawnObstacle() {
    // Spawn rate increases as speed increases, but capped for playability
    if (frameCount % Math.floor(1200 / gameSpeed) === 0 || frameCount % 60 === 0) {
        obstacles.push(new Obstacle());
    }
}

function checkCollisions() {
    // AABB Collision Detection
    for (let obs of obstacles) {
        if (
            player.x < obs.x + obs.w - 10 && // Hitbox adjustment
            player.x + player.width > obs.x + 10 &&
            player.y < obs.y + obs.h - 10 &&
            player.y + player.height > obs.y + 5
        ) {
            gameOver();
        }
    }
}

function resetGame() {
    score = 0;
    gameSpeed = 5;
    obstacles = [];
    frameCount = 0;
    player.y = canvas.height - 100 - player.height; // Reset position
    player.dy = 0;
    
    document.getElementById('scoreVal').innerText = score;
    document.getElementById('highScoreVal').innerText = highScore;
}

function gameOver() {
    gameState = 'GAMEOVER';
    playSound('crash');
    
    if (score > highScore) {
        highScore = Math.floor(score);
        localStorage.setItem('ollamaHighScore', highScore);
    }

    document.getElementById('final-score').innerText = Math.floor(score);
    document.getElementById('game-over-screen').classList.add('active');
    document.getElementById('hud').style.display = 'none';
}

function update() {
    if (gameState !== 'PLAYING') return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw Background
    drawBackground();

    // Update & Draw Player
    player.update();
    player.draw();

    // Manage Obstacles
    spawnObstacle();
    
    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.update();
        obs.draw();
        
        if (obs.markedForDeletion) {
            obstacles.splice(i, 1);
        }
    }

    checkCollisions();

    // Update Score & Speed
    score += 0.1; // Score based on distance/time
    document.getElementById('scoreVal').innerText = Math.floor(score);
    
    if (frameCount % 60 === 0) {
        gameSpeed += 0.2; // Gradually increase speed
    }

    frameCount++;
}

function loop() {
    update();
    requestAnimationFrame(loop);
}

/**
 * INPUT HANDLING
 */
function handleInput(e) {
    if (e.type === 'keydown' && e.code !== 'Space') return;
    
    // Prevent default scrolling for spacebar
    if (e.type === 'keydown') e.preventDefault(); 

    switch (gameState) {
        case 'START':
            gameState = 'PLAYING';
            document.getElementById('start-screen').classList.remove('active');
            document.getElementById('hud').style.display = 'flex';
            resetGame();
            break;
        
        case 'PLAYING':
            player.jump();
            break;

        case 'GAMEOVER':
            // Handled by button click, but spacebar could work too if desired
            // For now, we rely on the button.
            break;
    }
}

window.addEventListener('keydown', handleInput);
canvas.addEventListener('mousedown', handleInput);
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Prevent scrolling
    handleInput(e);
}, {passive: false});

document.getElementById('start-btn').addEventListener('click', () => {
    gameState = 'PLAYING';
    document.getElementById('start-screen').classList.remove('active');
    document.getElementById('hud').style.display = 'flex';
    resetGame();
});

document.getElementById('restart-btn').addEventListener('click', () => {
    gameState = 'PLAYING';
    document.getElementById('game-over-screen').classList.remove('active');
    document.getElementById('hud').style.display = 'flex';
    resetGame();
});

// Start Loop
loop();

</script>
</body>
</html>
```

168 t/s, 4963 tokens, 30s
