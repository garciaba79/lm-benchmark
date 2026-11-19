# DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic
Model: deepseek-v4-pro-qwen3.5-9b-uncensored-heretic
Test: ollamas adventure
Created: 11/18/2026, 11:44:26 PM
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

Here is a complete, self-contained HTML file containing "Ollama's Adventure". It includes all CSS, JavaScript, and Canvas rendering logic required to play the game. No external libraries or assets are used.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama's Adventure</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #2c3e50;
            overflow: hidden;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        #game-container {
            position: relative;
            width: 800px;
            height: 450px;
            background-color: #87CEEB; /* Sky blue */
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            overflow: hidden;
        }

        canvas {
            display: block;
            width: 100%;
            height: 100%;
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
            justify-content: space-between;
            padding: 20px;
        }

        .hud {
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-weight: bold;
            font-size: 24px;
       

        #start-screen, #game-over-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            pointer-events: auto;
        }

        #start-screen h1 { font-size: 48px; margin-bottom: 20px; color: #FFD700; text-shadow: 3px 3px 0 #d35400; }
        #game-over-screen h1 { font-size: 42px; margin-bottom: 10px; color: #e74c3c; }

        .btn {
            background: linear-gradient(to bottom, #f1c40f, #d35400);
            border: none;
            padding: 15px 40px;
            font-size: 24px;
            color: white;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.1s, box-shadow 0.1s;
            margin-top: 20px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn:hover { transform: scale(1.05); box-shadow: 0 6px 12px rgba(0,0,0,0.3); }
        .btn:active { transform: scale(0.95); }

        #high-score-display {
            font-size: 18px;
            color: #f1c40f;
            margin-top: 10px;
        }

        /* Mobile controls hint */
        .mobile-hint {
            position: absolute;
            bottom: 20px;
            width: 100%;
            text-align: center;
            color: rgba(255,255,255,0.7);
            font-size: 14px;
        }

    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="800" height="450"></canvas>
    
    <div id="ui-layer">
        <div class="hud">Score: <span id="scoreVal">0</span></div>
        <div class="mobile-hint">Press SPACE or TAP to jump</div>
    </div>

    <div id="start-screen">
        <h1>Ollama's Adventure</h1>
        <p style="font-size: 20px; margin-bottom: 30px;">Help Ollama run forever!</p>
        <button class="btn" onclick="startGame()">Start Running</button>
    </div>

    <div id="game-over-screen" style="display: none;">
        <h1>Ouch! You hit an obstacle.</h1>
        <p style="font-size: 24px; margin-bottom: 5px;">Final Score: <span id="finalScore">0</span></p>
        <p id="high-score-display" style="font-size: 16px; color: #f1c40f;">High Score: <span id="hsVal">0</span></p>
        <button class="btn" onclick="startGame()">Play Again</button>
    </div>
</div>

<script>
/**
 * Ollama's Adventure - Game Logic
 */

// --- Audio System (Web Audio API) ---
const AudioSys = {
    ctx: new (window.AudioContext || window.webkitAudioContext)(),
    
    playJump() {
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        // A quick "boing" sound
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(300, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(600, this.ctx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.1);
    },

    playScore() {
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        // A pleasant "ding" sound
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, this.ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.15);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.15);
    },

    playCrash() {
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        
        // A low "thud" sound
        osc.type = 'square';
        osc.frequency.setValueAtTime(150, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(50, this.ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.6, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
        
        osc.start();
        osc.stop(this.ctx.currentTime + 0.2);
    }
};

// --- Game Constants & State ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('scoreVal');
const finalScoreEl = document.getElementById('finalScore');
const hsDisplay = document.getElementById('hsVal');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');

// Physics constants
const GRAVITY = 0.6;
const JUMP_FORCE = -12;
const GROUND_Y = 380; // The y-coordinate of the ground line

let gameState = {
    running: false,
    score: 0,
    highScore: parseInt(localStorage.getItem('ollamaHighScore')) || 0,
    speed: 5,
    frameCount: 0
};

// --- Entities ---

const alpaca = {
    x: 100,
    y: GROUND_Y - 60,
    width: 80,
    height: 60,
    vy: 0,
    grounded: true,
    
    draw() {
        ctx.save();
        
        // Body (White fluffy)
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.ellipse(this.x + this.width/2, this.y + this.height/2, 35, 40, 0, 0, Math.PI * 2);
        ctx.fill();

        // Head (White)
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(this.x + this.width/2 - 10, this.y - 20, 35, 0, Math.PI * 2);
        ctx.fill();

        // Ears (Pinkish inside)
        ctx.fillStyle = '#FFB6C1';
        ctx.beginPath();
        ctx.arc(this.x + this.width/2 - 10, this.y - 45, 8, 0, Math.PI * 2);
        ctx.fill();

        // Face (Pinkish)
        ctx.fillStyle = '#FFDAB9';
        ctx.fillRect(this.x + this.width/2 - 10, this.y - 30, 20, 40);

        // Eyes (Black)
        ctx.fillStyle = '#000000';
        ctx.beginPath();
        ctx.arc(this.x + this.width/2 - 5, this.y - 25, 6, 0, Math.PI * 2);
        ctx.fill();
        
        // Legs (Brown)
        ctx.fillStyle = '#8B4513';
        if (this.grounded) {
            // Standing legs
            ctx.fillRect(this.x + 20, this.y + 60, 10, 20);
            ctx.fillRect(this.x + 50, this.y + 60, 10, 20);
        } else {
            // Jumping legs (slightly bent)
            ctx.fillRect(this.x + 20, this.y + 60, 10, 18);
            ctx.fillRect(this.x + 50, this.y + 60, 10, 18);
        }

        // Tail (Brown)
        ctx.fillStyle = '#8B4513';
        ctx.beginPath();
        ctx.moveTo(this.x - 20, this.y + 30);
        ctx.quadraticCurveTo(this.x - 30, this.y + 20, this.x - 20, this.y + 10);
        ctx.fill();

        ctx.restore();
    },

    update() {
        // Apply gravity
        if (!this.grounded) {
            this.vy += GRAVITY;
            this.y += this.vy;
            
            // Check ground collision
            if (this.y + this.height >= GROUND_Y) {
                this.y = GROUND_Y - this.height;
                this.vy = 0;
                this.grounded = true;
            }
        } else {
            // When on ground, velocity is reset to 0
            this.vy = 0;
        }
    },

    jump() {
        if (this.grounded) {
            this.vy = JUMP_FORCE;
            this.grounded = false;
            AudioSys.playJump();
        }
    }
};

// --- Obstacles ---
let obstacles = [];

class Obstacle {
    constructor(x, type) {
        this.x = x;
        this.type = type; // 'rock' or 'cactus'
        this.width = 40 + Math.random() * 20;
        this.height = 30 + Math.random() * 15;
        
        if (this.type === 'rock') {
            this.color = '#7f8c8d'; // Grey
        } else {
            this.color = '#2ecc71'; // Green
        }
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        
        if (this.type === 'rock') {
            // Draw a bumpy rock shape
            const points = 5;
            for (let i = 0; i <= points; i++) {
                const angle = (i / points) * Math.PI * 2;
                const r = this.width/2 + Math.sin(angle * 3) * 10;
                const px = this.x + Math.cos(angle) * r;
                const py = GROUND_Y - this.height + Math.sin(angle * 4) * 5;
                if (i === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            }
            ctx.closePath();
        } else {
            // Draw a cactus shape
            const cx = this.x + this.width/2;
            const cy = GROUND_Y - this.height/2;
            
            ctx.moveTo(cx, cy + 10);
            for (let i = 0; i < 4; i++) {
                const angle = Math.PI / 2 + (i * Math.PI / 2) - Math.sin(i)*5;
                const r = this.height/2 + Math.cos(angle) * 10;
                ctx.lineTo(cx + Math.cos(angle) * r, cy + Math.sin(angle) * r);
            }
            ctx.closePath();
        }

        ctx.fill();
        
        // Highlight
        ctx.strokeStyle = 'rgba(255,255,255,0.3)';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    update() {
        this.x -= gameState.speed;
    }
}

// --- Background Layers (Parallax) ---
const layers = [
    { speed: 0.2, color: '#1a252f', height: 40 }, // Distant mountains
    { speed: 0.5, color: '#3d5a80', height: 60 }, // Mid clouds/mountains
    { speed: 0.8, color: '#ffffff', height: 10 }  // Foreground grass tufts
];

let bgOffsets = [0, 0, 0];

function drawBackground() {
    layers.forEach((layer, index) => {
        const offset = bgOffsets[index] % canvas.width;
        
        ctx.fillStyle = layer.color;
        
        if (index === 2) {
            // Draw grass tufts
            for (let x = -offset; x < canvas.width + this.width; x += 100) {
                const y = GROUND_Y - layer.height;
                ctx.fillRect(x, y, 60, layer.height);
                
                // Add some random bumps to grass
                ctx.fillStyle = '#2ecc71';
                for(let i=0; i<3; i++) {
                    ctx.fillRect(x + Math.random()*50, y - Math.random()*20, 10, 10);
                }
            }
        } else if (index === 1) {
            // Draw mid-layer mountains/clouds
            for (let x = -offset; x < canvas.width + this.width; x += 300) {
                const y = GROUND_Y - layer.height - Math.sin(x * 0.02) * 50;
                ctx.beginPath();
                ctx.moveTo(x, y);
                for (let i = 1; i <= 4; i++) {
                    const angle = Math.PI / 2 + (i * Math.PI / 2) - Math.sin(i)*5;
                    const r = layer.height/2 + Math.cos(angle) * 30;
                    ctx.lineTo(x + Math.cos(angle) * r, y + Math.sin(angle) * r);
                }
                ctx.closePath();
                ctx.fill();
            }
        } else {
            // Draw distant mountains (index 0)
            for (let x = -offset; x < canvas.width + this.width; x += 500) {
                const y = GROUND_Y - layer.height - Math.sin(x * 0.01) * 80;
                ctx.beginPath();
                ctx.moveTo(x, y);
                for (let i = 1; i <= 6; i++) {
                    const angle = Math.PI / 3 + (i * Math.PI / 3) - Math.sin(i)*5;
                    const r = layer.height/2 + Math.cos(angle) * 40;
                    ctx.lineTo(x + Math.cos(angle) * r, y + Math.sin(angle) * r);
                }
                ctx.closePath();
                ctx.fill();
            }
        }
    });
}

// --- Game Loop & Logic ---

function spawnObstacle() {
    // Determine gap size based on current speed (faster = wider gaps)
    const minGap = 300;
    const maxGap = 600;
    const gap = Math.floor(Math.random() * (maxGap - minGap + 1) + minGap);
    
    // Determine obstacle type based on randomness
    const isRock = Math.random() < 0.4;
    
    obstacles.push(new Obstacle(canvas.width, isRock ? 'rock' : 'cactus'));
}

function checkCollisions() {
    for (let obs of obstacles) {
        // Simple AABB collision detection
        if (alpaca.x + alpaca.width > obs.x && 
            alpaca.x < obs.x + obs.width &&
            alpaca.y + alpaca.height > GROUND_Y - obs.height &&
            alpaca.y < GROUND_Y) {
            
            AudioSys.playCrash();
            gameOver();
        }
    }
}

function update() {
    if (!gameState.running) return;

    // Update Score
    gameState.score += 0.1; // Score based on distance/time survived
    scoreEl.innerText = Math.floor(gameState.score);

    // Spawn obstacles
    spawnObstacle();

    // Move obstacles
    obstacles.forEach(obs => obs.update());
    
    // Remove off-screen obstacles
    if (obstacles.length > 0 && obstacles[0].x + obstacles[0].width < -50) {
        obstacles.shift();
    }

    // Update alpaca
    alpaca.update();

    // Check collisions
    checkCollisions();

    // Increase speed gradually
    gameState.speed += 0.02;

    requestAnimationFrame(loop);
}

function loop() {
    if (!gameState.running) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update background offsets based on game speed
    layers.forEach((layer, index) => {
        bgOffsets[index] += gameState.speed * layer.speed;
    });

    drawBackground();

    // Draw obstacles (behind alpaca)
    obstacles.forEach(obs => obs.draw());

    // Draw alpaca
    alpaca.draw();

    requestAnimationFrame(loop);
}

function startGame() {
    // Reset state
    gameState.score = 0;
    gameState.speed = 5;
    obstacles = [];
    alpaca.y = GROUND_Y - alpaca.height;
    alpaca.vy = 0;
    
    document.getElementById('scoreVal').innerText = '0';
    
    startScreen.style.display = 'none';
    gameOverScreen.style.display = 'none';
    
    gameState.running = true;
    
    // Ensure audio context is ready
    if (AudioSys.ctx.state === 'suspended') {
        AudioSys.ctx.resume();
    }

    loop();
}

function gameOver() {
    gameState.running = false;
    
    // Save high score
    const newHighScore = Math.max(gameState.score, gameState.highScore);
    localStorage.setItem('ollamaHighScore', newHighScore);
    gameState.highScore = newHighScore;
    
    finalScoreEl.innerText = Math.floor(gameState.score);
    hsDisplay.innerText = Math.floor(newHighScore);
    
    gameOverScreen.style.display = 'flex';
}

// --- Input Handling ---

function handleInput(e) {
    if (e.type === 'keydown' && e.code !== 'Space') return;
    if (e.type === 'touchstart' || e.type === 'mousedown') return; // Let clicks/taps pass through
    
    if (gameState.running) {
        alpaca.jump();
    } else if (!gameState.running && startScreen.style.display !== 'none') {
        // If game hasn't started, spacebar could also start it, but we have a button.
    }
}

window.addEventListener('keydown', handleInput);
canvas.addEventListener('mousedown', () => {
    if (gameState.running) alpaca.jump();
});
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Prevent scrolling
    if (gameState.running) alpaca.jump();
}, {passive: false});

// Initial render to show something before starting
alpaca.draw();
drawBackground();

</script>
</body>
</html>
```

158 t/s, 5093 tokens, 32s
