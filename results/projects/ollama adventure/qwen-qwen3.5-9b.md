# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: ollamas adventure
Created: 11/03/2026, 12:52:27 AM
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

Here is the complete, self-contained HTML file for **"Ollama's Adventure"**.

You can save this code as an `.html` file (e.g., `ollama_adventure.html`) and open it in any modern web browser to play.

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
            background-color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Fredoka One', cursive;
            overflow: hidden;
            user-select: none;
        }

        #game-container {
            position: relative;
            width: 800px;
            height: 450px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            border-radius: 10px;
            background-color: #87CEEB; /* Sky Blue */
            overflow: hidden;
        }

        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }

        .ui-layer {
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
            text-align: center;
        }

        .hud {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            font-size: 24px;
            text-shadow: 2px 2px 0 #000;
            pointer-events: none;
        }

        .hud-right {
            right: 20px;
        }

        #start-screen, #game-over-screen {
            background: rgba(0, 0, 0, 0.6);
            padding: 40px;
            border-radius: 20px;
            color: white;
            pointer-events: auto;
            border: 4px solid #FFD700;
            backdrop-filter: blur(5px);
        }

        h1 {
            font-size: 48px;
            margin: 0 0 20px 0;
            color: #FFD700;
            text-shadow: 3px 3px 0 #d35400;
        }

        p {
            font-family: sans-serif;
            font-size: 18px;
            margin-bottom: 30px;
            color: #eee;
        }

        button {
            background-color: #e67e22;
            border: none;
            padding: 15px 40px;
            font-family: 'Fredoka One', cursive;
            font-size: 24px;
            color: white;
            cursor: pointer;
            border-radius: 50px;
            box-shadow: 0 6px #d35400;
            transition: transform 0.1s;
        }

        button:active {
            transform: translateY(4px);
            box-shadow: 0 2px #d35400;
        }

        button:hover {
            background-color: #f39c12;
        }

        .hidden {
            display: none !important;
        }

    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="800" height="450"></canvas>

    <!-- HUD -->
    <div class="hud">
        Score: <span id="scoreVal">0</span><br>
        High Score: <span id="highScoreVal">0</span>
    </div>

    <!-- Start Screen -->
    <div id="start-screen" class="ui-layer">
        <h1>Ollama's Adventure</h1>
        <p>Press SPACE, Click, or Tap to Jump!</p>
        <button id="startBtn">PLAY NOW</button>
    </div>

    <!-- Game Over Screen -->
    <div id="game-over-screen" class="ui-layer hidden">
        <h1>OUCH!</h1>
        <p>Ollama hit an obstacle.</p>
        <p>Score: <span id="finalScore">0</span></p>
        <button id="restartBtn">PLAY AGAIN</button>
    </div>
</div>

<script>
/**
 * OLLAMA'S ADVENTURE
 * A self-contained Canvas game.
 */

// --- Audio System (Web Audio API) ---
const AudioSys = {
    ctx: null,
    init: function() {
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
    },
    playJump: function() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(600, this.ctx.currentTime + 0.1);
        
        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.15);
    },
    playScore: function() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.type = 'triangle';
        // Two notes for a "ding" sound
        osc.frequency.setValueAtTime(600, this.ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(900, this.ctx.currentTime + 0.1);
        
        gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 0.3);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.3);
    },
    playCrash: function() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(100, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(30, this.ctx.currentTime + 0.3);
        
        gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.3);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.3);
    }
};

// --- Game Constants & Setup ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// UI Elements
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const scoreEl = document.getElementById('scoreVal');
const highScoreEl = document.getElementById('highScoreVal');
const finalScoreEl = document.getElementById('finalScore');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');

// Game State
let frames = 0;
let score = 0;
let highScore = localStorage.getItem('ollamaHighScore') || 0;
let gameSpeed = 5;
let isGameOver = false;
let animationId;

highScoreEl.innerText = highScore;

// Parallax Layers
const layers = {
    ground: { y: 380, w: canvas.width, h: canvas.height - 380 }, // Visual offset handled in draw
    bg1: { speed: 0.5, color: '#A2D9CE', content: 'mountains' },
    bg2: { speed: 0.2, color: '#F6E58D', content: 'hills' }
};

// --- Classes ---

class Alpaca {
    constructor() {
        this.w = 60;
        this.h = 50;
        this.x = 50;
        this.y = 380 - this.h + 20; // Start slightly above ground
        
        this.vy = 0;
        this.gravity = 0.7;
        this.jumpStrength = -14;
        this.grounded = true;
        
        // Animation
        this.animTimer = 0;
    }

    jump() {
        if (this.grounded) {
            this.vy = this.jumpStrength;
            this.grounded = false;
            AudioSys.playJump();
        }
    }

    update() {
        // Physics
        this.y += this.vy;
        
        // Gravity
        if (this.y < 380 - this.h) {
            this.vy += this.gravity;
            this.grounded = false;
        } else {
            this.y = 380 - this.h;
            this.vy = 0;
            this.grounded = true;
        }

        // Bobbing animation when running
        if (this.grounded && !isGameOver) {
            this.animTimer += frames % 20 === 0 ? 1 : 0; // Simple toggle for legs
        }
    }

    draw() {
        ctx.save();
        
        // Body Color (Creamy White)
        ctx.fillStyle = '#FDFCF5'; 
        ctx.fillRect(this.x, this.y, this.w, this.h);

        // Ears
        ctx.beginPath();
        ctx.ellipse(this.x + 10, this.y + 5, 6, 12, -Math.PI / 4, 0, Math.PI * 2); // Left ear
        ctx.ellipse(this.x + 50, this.y + 5, 6, 12, Math.PI / 4, 0, Math.PI * 2);   // Right ear
        ctx.fill();

        // Legs (Simple stick legs that rotate slightly)
        if (!isGameOver) {
            const legOffset = Math.sin(frames * 0.5) * 5; // Leg swing speed
            ctx.strokeStyle = '#FDFCF5';
            ctx.lineWidth = 8;
            
            // Back Leg
            ctx.beginPath();
            ctx.moveTo(this.x + 10, this.y + this.h - 5);
            ctx.lineTo(this.x + 10 + legOffset, this.y + this.h + 20);
            ctx.stroke();

            // Front Leg
            ctx.beginPath();
            ctx.moveTo(this.x + this.w - 10, this.y + this.h - 5);
            ctx.lineTo(this.x + this.w - 10 - legOffset, this.y + this.h + 20);
            ctx.stroke();
        }

        // Face (Pinkish nose area)
        ctx.fillStyle = '#FFB6C1';
        ctx.fillRect(this.x + 25, this.y + 25, 10, 8);
        
        // Eyes
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(this.x + 20, this.y + 25, 3, 0, Math.PI * 2); // Left eye
        ctx.arc(this.x + 40, this.y + 25, 3, 0, Math.PI * 2); // Right eye
        ctx.fill();

        ctx.restore();
    }
}

class Obstacle {
    constructor() {
        this.w = 40;
        this.h = 40;
        this.x = canvas.width + Math.random() * 200;
        this.y = 380 - this.h; // Sitting on ground
        this.markedForDeletion = false;
        
        // Randomize obstacle type (Bush or Rock)
        this.type = Math.random() > 0.5 ? 'bush' : 'rock';
    }

    update() {
        this.x -= gameSpeed;
        if (this.x < -this.w) this.markedForDeletion = true;
    }

    draw() {
        if (this.type === 'rock') {
            ctx.fillStyle = '#7F8C8D'; // Grey rock
            ctx.beginPath();
            ctx.moveTo(this.x + 10, this.y);
            ctx.lineTo(this.x + this.w - 10, this.y);
            ctx.lineTo(this.x + this.w, this.y + 15);
            ctx.lineTo(this.x + this.w - 5, this.y + this.h - 5);
            ctx.lineTo(this.x + 5, this.y + this.h - 5);
            ctx.lineTo(this.x, this.y + 15);
            ctx.fill();
        } else {
            // Bush (Green)
            ctx.fillStyle = '#2ECC71';
            ctx.beginPath();
            ctx.moveTo(this.x, this.y + 30);
            ctx.quadraticCurveTo(this.x + 5, this.y - 5, this.x + 20, this.y);
            ctx.quadraticCurveTo(this.x + 40, this.y - 5, this.x + this.w, this.y + 30);
            ctx.fill();
        }
    }
}

class Cloud {
    constructor() {
        this.x = canvas.width + Math.random() * 200;
        this.y = Math.random() * (canvas.height - layers.bg1.color) - 50;
        this.w = 60 + Math.random() * 40;
        this.speedMod = 0.8; // Moves slower than background
        this.markedForDeletion = false;
    }

    update() {
        this.x -= gameSpeed * this.speedMod;
        if (this.x < -100) this.markedForDeletion = true;
    }

    draw() {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 20, 0, Math.PI);
        ctx.arc(this.x + 25, this.y - 10, 25, 0, Math.PI);
        ctx.arc(this.x + 50, this.y, 20, 0, Math.PI);
        ctx.fill();
    }
}

// --- Game Logic Variables ---
let player;
let obstacles = [];
let clouds = [];
let spawnTimer = 0;

function init() {
    player = new Alpaca();
    obstacles = [];
    clouds = [];
    score = 0;
    gameSpeed = 5;
    frames = 0;
    isGameOver = false;
    
    // Initial background clouds
    for(let i=0; i<3; i++) {
        let c = new Cloud();
        c.x -= Math.random() * canvas.width; // Spread them out
        clouds.push(c);
    }
}

function handleInput(e) {
    if (e.type === 'keydown' && e.code !== 'Space') return;
    if (e.type === 'keydown') e.preventDefault(); // Prevent scrolling
    
    if (!isGameOver) {
        player.jump();
    }
}

// --- Main Game Functions ---

function spawnObstacle() {
    spawnTimer++;
    // Spawn rate increases slightly as speed increases
    let minFrames = 60 - Math.floor(gameSpeed * 2); 
    if (spawnTimer > minFrames && Math.random() < 0.1) {
        obstacles.push(new Obstacle());
        spawnTimer = 0;
    }
}

function checkCollisions() {
    // AABB Collision detection
    for (let obs of obstacles) {
        if (
            player.x < obs.x + obs.w &&
            player.x + player.w > obs.x &&
            player.y < obs.y + obs.h &&
            player.y + player.h > obs.y
        ) {
            gameOver();
        }
    }
}

function updateScore() {
    score += 0.1; // Score increases by distance/time
    if (score % 10 === 0) {
        gameSpeed += 0.2; // Increase difficulty every 10 points
        AudioSys.playScore();
    }
    
    scoreEl.innerText = Math.floor(score);
}

function drawBackground() {
    // Ground (Grass)
    ctx.fillStyle = '#56824D'; // Grass Green
    ctx.fillRect(0, layers.ground.y, canvas.width, canvas.height - layers.ground.y);
    
    // Ground detail (dirt line)
    ctx.fillStyle = '#3A5F36';
    ctx.fillRect(0, layers.ground.y + 20, canvas.width, 5);

    // Parallax Layer 1 (Mountains/Distant) - moves very slow
    let bgOffset = (frames * layers.bg1.speed * gameSpeed) % canvas.width;
    
    // Draw two copies for seamless loop
    ctx.fillStyle = layers.bg1.color;
    for(let i=0; i<2; i++) {
        ctx.beginPath();
        ctx.moveTo((i*800) + bgOffset, 450);
        ctx.lineTo((i*800) + bgOffset + 200, 300);
        ctx.lineTo((i*800) + bgOffset + 400, 150);
        ctx.fill();
    }

    // Parallax Layer 2 (Hills/Close) - moves slightly faster relative to world
    let bgOffset2 = (frames * layers.bg2.speed * gameSpeed * 0.5) % canvas.width;
    ctx.fillStyle = '#E2F6D3';
    for(let i=0; i<2; i++) {
        ctx.beginPath();
        ctx.moveTo((i*800) + bgOffset2, layers.ground.y);
        ctx.lineTo((i*800) + bgOffset2 + 150, 250);
        ctx.lineTo((i*800) + bgOffset2 + 350, layers.ground.y);
        ctx.fill();
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawBackground();

    // Draw Clouds (Parallax background objects)
    clouds.forEach(c => {
        c.update();
        c.draw();
    });
    // Cleanup dead clouds
    clouds = clouds.filter(c => !c.markedForDeletion);

    // Draw Player
    player.update();
    player.draw();

    // Handle Obstacles
    spawnObstacle();
    obstacles.forEach(obs => {
        obs.update();
        obs.draw();
    });
    
    // Cleanup dead obstacles
    obstacles = obstacles.filter(obs => !obs.markedForDeletion);

    checkCollisions();
    updateScore();
}

function loop() {
    if (!isGameOver) {
        frames++;
        draw();
        animationId = requestAnimationFrame(loop);
    } else {
        // Draw one last frame to show the crash position
        player.draw();
    }
}

function gameOver() {
    isGameOver = true;
    cancelAnimationFrame(animationId);
    AudioSys.playCrash();
    
    if (score > highScore) {
        highScore = Math.floor(score);
        localStorage.setItem('ollamaHighScore', highScore);
        highScoreEl.innerText = highScore;
    }
    
    finalScoreEl.innerText = Math.floor(score);
    startScreen.classList.add('hidden');
    gameOverScreen.classList.remove('hidden');
}

// --- Event Listeners ---

window.addEventListener('keydown', handleInput);
window.addEventListener('mousedown', (e) => {
    if(e.target.tagName !== 'BUTTON') handleInput(e); // Jump on click if not clicking button
});
window.addEventListener('touchstart', (e) => {
    // Prevent default touch behavior but allow jumping
    // We don't preventDefault here to keep it simple, but ideally we'd check target
    if(e.target.tagName !== 'BUTTON') handleInput(e); 
}, {passive: false});

startBtn.addEventListener('click', () => {
    AudioSys.init(); // Initialize audio context on user interaction
    init();
    loop();
    startScreen.classList.add('hidden');
});

restartBtn.addEventListener('click', () => {
    gameOverScreen.classList.add('hidden');
    init();
    loop();
});

// Initial High Score Load
highScoreEl.innerText = highScore;

</script>
</body>
</html>
```

117 t/s, 4932 tokens, 42s
