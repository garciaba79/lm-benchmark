# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: ollamas adventure
Created: 11/22/2026, 12:40:01 PM
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

Here is the complete, single-file source code for **Ollama's Adventure**.

Save the code below as an `.html` file (e.g., `ollama-adventure.html`) and open it in any modern web browser.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Ollama's Adventure</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #333;
            font-family: 'Fredoka One', cursive;
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
            display: block;
            background-color: #87CEEB; /* Sky Blue */
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
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
            text-align: center;
        }

        .score-board {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 24px;
            color: white;
            text-shadow: 2px 2px 0 #000;
            pointer-events: none;
        }

        .high-score {
            font-size: 18px;
            color: #FFD700;
            margin-top: 5px;
        }

        #menu {
            background: rgba(0, 0, 0, 0.6);
            padding: 40px;
            border-radius: 20px;
            pointer-events: auto;
            border: 4px solid white;
            display: none; /* Hidden by default */
        }

        h1 {
            color: #fff;
            margin: 0 0 20px 0;
            font-size: 48px;
            text-shadow: 3px 3px 0 #333;
            color: #FFB6C1; /* Alpaca Pink */
        }

        p {
            color: #eee;
            font-size: 20px;
            margin-bottom: 30px;
        }

        button {
            background: #FF69B4;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 24px;
            font-family: 'Fredoka One', cursive;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 6px 0 #C71585;
            transition: transform 0.1s, box-shadow 0.1s;
        }

        button:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 #C71585;
        }

        button:hover {
            background: #FF1493;
        }

        /* Mobile instructions */
        .mobile-hint {
            display: none;
            margin-top: 10px;
            font-size: 14px;
            opacity: 0.8;
        }
        
        @media (hover: none) {
            .mobile-hint { display: block; }
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas"></canvas>
        
        <div id="ui-layer">
            <div class="score-board">
                <div id="scoreDisplay">Score: 0</div>
                <div id="highScoreDisplay" class="high-score">Best: 0</div>
            </div>

            <div id="menu">
                <h1 id="menuTitle">Ollama's Adventure</h1>
                <p id="menuText">Press Space or Tap to Jump!</p>
                <button id="actionBtn">Play</button>
                <div class="mobile-hint">(Tap screen to jump)</div>
            </div>
        </div>
    </div>

<script>
/**
 * OLLAMA'S ADVENTURE
 * A self-contained endless runner.
 */

// --- Configuration ---
const CONFIG = {
    gravity: 0.6,
    jumpStrength: -12,
    groundHeight: 100,
    baseSpeed: 5,
    maxSpeed: 12,
    speedIncrement: 0.001,
    colors: {
        sky: '#87CEEB',
        ground: '#4CAF50',
        groundDark: '#388E3C',
        alpaca: '#FFFFFF',
        alpacaShadow: '#E0E0E0',
        alpacaFace: '#FFB6C1',
        obstacle: '#8B4513'
    }
};

// --- Audio System (Web Audio API) ---
const AudioSys = {
    ctx: null,
    init: function() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    },
    playJump: function() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(600, this.ctx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.1);
    },
    playScore: function() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(1200, this.ctx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.1);
    },
    playCrash: function() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(100, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(10, this.ctx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.3);
    }
};

// --- Game State ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const uiMenu = document.getElementById('menu');
const uiTitle = document.getElementById('menuTitle');
const uiText = document.getElementById('menuText');
const btnAction = document.getElementById('actionBtn');
const scoreEl = document.getElementById('scoreDisplay');
const highScoreEl = document.getElementById('highScoreDisplay');

let gameState = 'START'; // START, PLAYING, GAMEOVER
let score = 0;
let highScore = localStorage.getItem('ollamaHighScore') || 0;
let gameSpeed = CONFIG.baseSpeed;
let frameCount = 0;
let animationId;

// Resize handling
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();
highScoreEl.innerText = `Best: ${Math.floor(highScore)}`;

// --- Classes ---

class Alpaca {
    constructor() {
        this.width = 60;
        this.height = 70;
        this.x = 50;
        this.y = canvas.height - CONFIG.groundHeight - this.height;
        this.dy = 0;
        this.grounded = true;
        this.legAngle = 0;
    }

    jump() {
        if (this.grounded) {
            this.dy = CONFIG.jumpStrength;
            this.grounded = false;
            AudioSys.playJump();
        }
    }

    update() {
        // Physics
        this.y += this.dy;
        
        if (this.y + this.height < canvas.height - CONFIG.groundHeight) {
            this.dy += CONFIG.gravity;
            this.grounded = false;
        } else {
            this.dy = 0;
            this.grounded = true;
            this.y = canvas.height - CONFIG.groundHeight - this.height;
        }

        // Animation logic
        if (this.grounded) {
            this.legAngle += 0.2 + (gameSpeed * 0.01);
        } else {
            this.legAngle = Math.PI / 4; // Legs tucked
        }
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        // Draw Legs
        ctx.fillStyle = '#F0F0F0';
        const legWidth = 10;
        const legHeight = 25;
        
        // Back Leg
        ctx.save();
        ctx.translate(10, 50);
        ctx.rotate(Math.sin(this.legAngle) * 0.5);
        ctx.fillRect(0, 0, legWidth, legHeight);
        ctx.restore();

        // Front Leg
        ctx.save();
        ctx.translate(35, 50);
        ctx.rotate(Math.sin(this.legAngle + Math.PI) * 0.5);
        ctx.fillRect(0, 0, legWidth, legHeight);
        ctx.restore();

        // Body (Fluffy Cloud shape)
        ctx.fillStyle = CONFIG.colors.alpaca;
        ctx.beginPath();
        ctx.ellipse(30, 40, 30, 25, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Fluff details
        ctx.fillStyle = '#FFF';
        ctx.beginPath();
        ctx.arc(20, 35, 10, 0, Math.PI*2);
        ctx.arc(40, 35, 12, 0, Math.PI*2);
        ctx.arc(30, 25, 10, 0, Math.PI*2);
        ctx.fill();

        // Head
        ctx.fillStyle = CONFIG.colors.alpaca;
        ctx.beginPath();
        ctx.arc(55, 15, 18, 0, Math.PI * 2);
        ctx.fill();

        // Ears
        ctx.beginPath();
        ctx.ellipse(45, 0, 4, 8, -0.5, 0, Math.PI * 2);
        ctx.ellipse(65, 0, 4, 8, 0.5, 0, Math.PI * 2);
        ctx.fill();

        // Face
        ctx.fillStyle = '#333';
        ctx.beginPath();
        ctx.arc(62, 12, 2, 0, Math.PI * 2); // Eye
        ctx.fill();
        
        // Snout
        ctx.fillStyle = CONFIG.colors.alpacaFace;
        ctx.beginPath();
        ctx.ellipse(65, 20, 6, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        // Tail
        ctx.beginPath();
        ctx.arc(0, 40, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }
}

class Obstacle {
    constructor() {
        this.width = 40;
        this.height = 40 + Math.random() * 20;
        this.x = canvas.width;
        this.y = canvas.height - CONFIG.groundHeight - this.height;
        this.markedForDeletion = false;
        this.type = Math.random() > 0.5 ? 'rock' : 'cactus';
    }

    update() {
        this.x -= gameSpeed;
        if (this.x + this.width < 0) this.markedForDeletion = true;
    }

    draw() {
        ctx.fillStyle = this.type === 'rock' ? '#888' : '#2E8B57';
        
        if (this.type === 'rock') {
            // Draw Rock
            ctx.beginPath();
            ctx.moveTo(this.x, this.y + this.height);
            ctx.lineTo(this.x + 10, this.y);
            ctx.lineTo(this.x + 30, this.y + 10);
            ctx.lineTo(this.x + this.width, this.y + this.height);
            ctx.fill();
            // Highlight
            ctx.strokeStyle = '#A9A9A9';
            ctx.lineWidth = 2;
            ctx.stroke();
        } else {
            // Draw Cactus/Pine
            ctx.fillRect(this.x + 10, this.y, 20, this.height);
            ctx.fillRect(this.x, this.y + 15, 10, 20); // Arm L
            ctx.fillRect(this.x + 30, this.y + 10, 10, 15); // Arm R
        }
    }
}

class Cloud {
    constructor(speedMod) {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * (canvas.height / 2);
        this.speed = gameSpeed * speedMod * 0.5;
        this.scale = 0.5 + Math.random() * 0.5;
        this.markedForDeletion = false;
    }
    
    update() {
        this.x -= this.speed;
        if (this.x + 100 < 0) this.markedForDeletion = true;
    }

    draw() {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.scale(this.scale, this.scale);
        ctx.beginPath();
        ctx.arc(0, 0, 30, 0, Math.PI * 2);
        ctx.arc(25, -10, 35, 0, Math.PI * 2);
        ctx.arc(50, 0, 30, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

// --- Game Objects ---
let player;
let obstacles = [];
let clouds = [];
let spawnTimer = 0;
let spawnInterval = 100; // Frames

function initGame() {
    player = new Alpaca();
    obstacles = [];
    clouds = [];
    score = 0;
    gameSpeed = CONFIG.baseSpeed;
    spawnTimer = 0;
    
    // Initial Clouds
    for(let i=0; i<5; i++) {
        let c = new Cloud(0.5);
        c.x = Math.random() * canvas.width;
        clouds.push(c);
    }
    
    scoreEl.innerText = `Score: 0`;
}

// --- Game Loop ---
function loop() {
    if (gameState !== 'PLAYING') return;

    animationId = requestAnimationFrame(loop);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Update Logic
    
    // Speed up
    if (gameSpeed < CONFIG.maxSpeed) {
        gameSpeed += CONFIG.speedIncrement;
    }

    // Score
    score += 0.1;
    if (Math.floor(score) % 100 === 0 && Math.floor(score) > 0 && frameCount % 60 === 0) {
         AudioSys.playScore();
    }
    scoreEl.innerText = `Score: ${Math.floor(score)}`;

    // Spawn Clouds
    if (Math.random() < 0.01) {
        clouds.push(new Cloud(0.5)); // Far layer
    }
    if (Math.random() < 0.02) {
        clouds.push(new Cloud(1.2)); // Near layer
    }

    // Spawn Obstacles
    spawnTimer++;
    if (spawnTimer > spawnInterval) {
        obstacles.push(new Obstacle());
        // Randomize next spawn based on speed
        spawnInterval = 60 + Math.random() * 100 - (gameSpeed * 2);
        if (spawnInterval < 40) spawnInterval = 40;
        spawnTimer = 0;
    }

    // 2. Draw Background (Parallax)
    
    // Sky
    ctx.fillStyle = CONFIG.colors.sky;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Sun
    ctx.fillStyle = '#FFD700';
    ctx.beginPath();
    ctx.arc(canvas.width - 80, 80, 40, 0, Math.PI*2);
    ctx.fill();

    // Clouds (Layer 1 - Back)
    clouds.forEach(c => {
        if(c.scale < 1) c.update();
        if(!c.markedForDeletion) c.draw();
    });

    // Mountains (Procedural Background)
    ctx.fillStyle = '#A9CCE3';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height - CONFIG.groundHeight);
    for(let i=0; i<=canvas.width; i+=100) {
        ctx.lineTo(i, canvas.height - CONFIG.groundHeight - 100 - (Math.sin(i*0.01 + frameCount*0.002)*50));
    }
    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.fill();

    // Ground
    ctx.fillStyle = CONFIG.colors.ground;
    ctx.fillRect(0, canvas.height - CONFIG.groundHeight, canvas.width, CONFIG.groundHeight);
    // Ground Detail (stripes to show movement)
    ctx.fillStyle = CONFIG.colors.groundDark;
    let stripeOffset = -(score * 20) % 100;
    for (let i = stripeOffset; i < canvas.width; i += 100) {
        ctx.beginPath();
        ctx.moveTo(i, canvas.height - CONFIG.groundHeight);
        ctx.lineTo(i + 50, canvas.height);
        ctx.lineTo(i + 20, canvas.height);
        ctx.lineTo(i - 30, canvas.height - CONFIG.groundHeight);
        ctx.fill();
    }

    // 3. Update & Draw Entities
    
    // Clouds (Layer 2 - Front)
    clouds.forEach(c => {
        if(c.scale >= 1) c.update();
        if(!c.markedForDeletion) c.draw();
    });

    // Player
    player.update();
    player.draw();

    // Obstacles
    obstacles.forEach(obs => {
        obs.update();
        obs.draw();
        
        // Collision Detection (AABB)
        // Shrink hitbox slightly for fairness
        const hitboxX = player.x + 15;
        const hitboxY = player.y + 15;
        const hitboxW = player.width - 30;
        const hitboxH = player.height - 30;

        if (
            hitboxX < obs.x + obs.width &&
            hitboxX + hitboxW > obs.x &&
            hitboxY < obs.y + obs.height &&
            hitboxY + hitboxH > obs.y
        ) {
            gameOver();
        }
    });

    // Cleanup
    obstacles = obstacles.filter(o => !o.markedForDeletion);
    clouds = clouds.filter(c => !c.markedForDeletion);

    frameCount++;
}

// --- Input Handling ---
function handleInput(e) {
    if (e.type === 'keydown' && e.code !== 'Space') return;
    if (e.type === 'keydown') e.preventDefault(); // Stop scrolling

    if (gameState === 'START' || gameState === 'GAMEOVER') {
        // Handled by button click usually, but spacebar works too
        if (uiMenu.style.display !== 'none') return; 
    }
    
    if (gameState === 'PLAYING') {
        player.jump();
    }
}

window.addEventListener('keydown', handleInput);
window.addEventListener('touchstart', (e) => {
    if(gameState === 'PLAYING') player.jump();
}, {passive: false});
window.addEventListener('mousedown', (e) => {
    if(gameState === 'PLAYING') player.jump();
});

// --- Game Flow Control ---

function startGame() {
    AudioSys.init();
    gameState = 'PLAYING';
    uiMenu.style.display = 'none';
    initGame();
    loop();
}

function gameOver() {
    gameState = 'GAMEOVER';
    cancelAnimationFrame(animationId);
    AudioSys.playCrash();
    
    // Update High Score
    if (score > highScore) {
        highScore = score;
        localStorage.setItem('ollamaHighScore', highScore);
        highScoreEl.innerText = `Best: ${Math.floor(highScore)}`;
    }

    // Show Menu
    uiTitle.innerText = "Oh no!";
    uiText.innerText = `Score: ${Math.floor(score)}`;
    btnAction.innerText = "Play Again";
    uiMenu.style.display = 'block';
}

// Button Listener
btnAction.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent jump trigger
    startGame();
});

// Initial Render
initGame();
// Draw one frame so background isn't empty
ctx.fillStyle = CONFIG.colors.sky;
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = CONFIG.colors.ground;
ctx.fillRect(0, canvas.height - CONFIG.groundHeight, canvas.width, CONFIG.groundHeight);
player.draw();

// Show Menu initially
uiMenu.style.display = 'block';
uiTitle.innerText = "Ollama's Adventure";
uiText.innerText = "Help Ollama jump over obstacles!";
btnAction.innerText = "Play";

</script>
</body>
</html>
```

44 t/s, 5470 tokens, 126s, 35%
