# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: ollamas adventure
Created: 11/22/2026, 02:53:34 AM
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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        #game-container {
            position: relative;
            width: 800px;
            height: 450px;
            background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 50%, #90EE90 100%);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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
            right: 0;
            bottom: 0;
            pointer-events: none;
        }

        .hud {
            position: absolute;
            top: 20px;
            left: 30px;
            color: #fff;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        .hud span {
            margin-right: 30px;
        }

        #start-screen, #game-over-screen {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            pointer-events: auto;
        }

        #game-over-screen {
            display: none;
        }

        h1 {
            color: #FFD700;
            font-size: 48px;
            margin-bottom: 20px;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
        }

        h2 {
            color: #FF6B6B;
            font-size: 36px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        p {
            color: #fff;
            font-size: 18px;
            margin-bottom: 30px;
            text-align: center;
            max-width: 600px;
            line-height: 1.6;
        }

        .btn {
            padding: 15px 40px;
            font-size: 24px;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            border: none;
            border-radius: 50px;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 8px 20px rgba(255, 165, 0, 0.4);
            transition: all 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 12px 30px rgba(255, 165, 0, 0.6);
        }

        .btn:active {
            transform: translateY(1px) scale(0.98);
        }

        #controls-hint {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            text-align: center;
        }

        .key {
            display: inline-block;
            padding: 5px 12px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            margin: 0 5px;
        }

        .floating-score {
            position: absolute;
            color: #FFD700;
            font-size: 32px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            animation: floatUp 1s ease-out forwards;
        }

        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0) scale(1); }
            100% { opacity: 0; transform: translateY(-50px) scale(1.2); }
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="450"></canvas>
        
        <div id="ui-layer">
            <div class="hud">
                <span>Score: <strong id="score-display">0</strong></span>
                <span>High Score: <strong id="high-score-display">0</strong></span>
            </div>

            <div id="start-screen">
                <h1>Ollama's Adventure 🦙</h1>
                <p>Welcome, brave alpaca! Run as far as you can and avoid the obstacles. The faster you go, the higher your score!</p>
                <button class="btn" onclick="startGame()">Start Running!</button>
            </div>

            <div id="game-over-screen">
                <h2>Oh no! You crashed! 💥</h2>
                <p>Your final score: <strong id="final-score">0</strong></p>
                <button class="btn" onclick="resetGame()">Play Again</button>
            </div>

            <div id="controls-hint">
                Press <span class="key">SPACE</span> or <span class="key">↑</span> to jump • Click/Tap anywhere to jump
            </div>
        </div>
    </div>

    <script>
        // Game Constants
        const CANVAS_WIDTH = 800;
        const CANVAS_HEIGHT = 450;
        const GRAVITY = 1.2;
        const JUMP_FORCE = -18;
        const GROUND_Y = 380;
        const INITIAL_SPEED = 6;
        const MAX_SPEED = 15;
        const SPEED_INCREMENT = 0.003;

        // Game State
        let gameState = {
            isRunning: false,
            score: 0,
            highScore: parseInt(localStorage.getItem('ollamaHighScore')) || 0,
            speed: INITIAL_SPEED,
            frameCount: 0,
            obstacles: [],
            particles: [],
            floatingTexts: []
        };

        // Alpaca Object
        const alpaca = {
            x: 150,
            y: GROUND_Y - 80,
            width: 70,
            height: 60,
            vy: 0,
            isJumping: false,
            rotation: 0,
            
            jump() {
                if (!this.isJumping) {
                    this.vy = JUMP_FORCE;
                    this.isJumping = true;
                    createParticles(this.x + this.width / 2, this.y + this.height, '#FFFFFF', 8);
                    playSound('jump');
                }
            },

            update() {
                // Apply gravity
                this.vy += GRAVITY;
                
                // Update position
                this.y += this.vy;

                // Ground collision
                if (this.y >= GROUND_Y - this.height) {
                    this.y = GROUND_Y - this.height;
                    this.vy = 0;
                    this.isJumping = false;
                    
                    // Add a little bounce effect when landing
                    createParticles(this.x + this.width / 2, this.y + this.height, '#8B4513', 5);
                }

                // Calculate rotation based on jump state
                if (this.isJumping) {
                    this.rotation = Math.min(Math.max(this.vy * 0.05, -0.3), 0.3);
                } else {
                    this.rotation *= 0.9;
                }
            },

            draw(ctx) {
                ctx.save();
                ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
                ctx.rotate(this.rotation);

                // Body (cream colored)
                ctx.fillStyle = '#F5DEB3';
                ctx.beginPath();
                ctx.ellipse(0, 10, 35, 40, 0, 0, Math.PI * 2);
                ctx.fill();

                // Head (slightly larger cream)
                ctx.fillStyle = '#FFEBCD';
                ctx.beginPath();
                ctx.arc(0, -25, 28, 0, Math.PI * 2);
                ctx.fill();

                // Ears (two triangular ears on top of head)
                ctx.fillStyle = '#F5DEB3';
                ctx.beginPath();
                ctx.moveTo(-18, -45);
                ctx.lineTo(-25, -60);
                ctx.lineTo(-10, -50);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(18, -45);
                ctx.lineTo(25, -60);
                ctx.lineTo(10, -50);
                ctx.fill();

                // Face (dark brown)
                ctx.fillStyle = '#6B4423';
                
                // Eyes
                ctx.beginPath();
                ctx.arc(-8, -28, 4, 0, Math.PI * 2);
                ctx.arc(8, -28, 4, 0, Math.PI * 2);
                ctx.fill();

                // Eye whites (white circles)
                ctx.fillStyle = '#FFFFFF';
                ctx.beginPath();
                ctx.arc(-9, -28, 3, 0, Math.PI * 2);
                ctx.arc(9, -28, 3, 0, Math.PI * 2);
                ctx.fill();

                // Nose and mouth area
                ctx.beginPath();
                ctx.ellipse(0, -15, 6, 4, 0, 0, Math.PI * 2);
                ctx.fill();

                // Whiskers (light brown)
                ctx.strokeStyle = '#D2B48C';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(-5, -13);
                ctx.lineTo(-15, -10);
                ctx.moveTo(5, -13);
                ctx.lineTo(15, -10);
                ctx.stroke();

                // Legs (brown)
                ctx.fillStyle = '#8B4513';
                
                // Back legs
                ctx.beginPath();
                ctx.ellipse(-20, 25, 6, 12, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.ellipse(20, 25, 6, 12, 0, 0, Math.PI * 2);
                ctx.fill();

                // Front legs (slightly bent when jumping)
                if (this.isJumping) {
                    ctx.beginPath();
                    ctx.ellipse(-15, 30, 5, 8, -0.2, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.beginPath();
                    ctx.ellipse(15, 30, 5, 8, 0.2, 0, Math.PI * 2);
                    ctx.fill();
                } else {
                    ctx.beginPath();
                    ctx.ellipse(-18, 28, 6, 14, -0.1, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.beginPath();
                    ctx.ellipse(18, 28, 6, 14, 0.1, 0, Math.PI * 2);
                    ctx.fill();
                }

                // Mane (fluffy hair on neck)
                ctx.fillStyle = '#DEB887';
                ctx.beginPath();
                ctx.moveTo(-25, -5);
                ctx.quadraticCurveTo(0, -15, 25, -5);
                ctx.lineTo(20, 5);
                ctx.quadraticCurveTo(0, 10, -20, 5);
                ctx.fill();

                // Tail (small fluffy tail)
                ctx.fillStyle = '#F5DEB3';
                ctx.beginPath();
                ctx.ellipse(-40, 5, 8, 6, Math.PI / 4, 0, Math.PI * 2);
                ctx.fill();

                ctx.restore();
            }
        };

        // Background Layers for Parallax Effect
        const backgroundLayers = [
            {
                name: 'farMountains',
                speedRatio: 0.15,
                color: '#87CEEB',
                elements: [],
                yBase: -50
            },
            {
                name: 'nearHills',
                speedRatio: 0.3,
                color: '#90EE90',
                elements: [],
                yBase: 100
            }
        ];

        // Initialize background elements
        function initBackground() {
            for (let i = 0; i < 8; i++) {
                backgroundLayers[0].elements.push({
                    x: Math.random() * CANVAS_WIDTH,
                    y: -50 + Math.random() * 150,
                    width: 60 + Math.random() * 120,
                    height: 80 + Math.random() * 100
                });
            }

            for (let i = 0; i < 12; i++) {
                backgroundLayers[1].elements.push({
                    x: Math.random() * CANVAS_WIDTH,
                    y: -50 + Math.random() * 80,
                    width: 40 + Math.random() * 90,
                    height: 60 + Math.random() * 70
                });
            }
        }

        // Obstacle Class
        class Obstacle {
            constructor() {
                this.x = CANVAS_WIDTH;
                this.y = GROUND_Y - 80;
                this.width = 50 + Math.random() * 30;
                this.height = 60 + Math.random() * 20;
                this.type = Math.random() > 0.7 ? 'rock' : 'cactus';
                this.passed = false;
            }

            update(speed) {
                this.x -= speed;
            }

            draw(ctx) {
                if (this.type === 'cactus') {
                    // Draw cactus
                    ctx.fillStyle = '#2E8B57';
                    
                    // Main stem
                    ctx.beginPath();
                    ctx.ellipse(this.x + this.width / 2, this.y + this.height / 2, 
                               this.width / 3, this.height / 1.5, 0, 0, Math.PI * 2);
                    ctx.fill();

                    // Arms (left)
                    if (Math.random() > 0.5 || this.frameCount % 60 < 30) {
                        ctx.beginPath();
                        ctx.ellipse(this.x + 10, this.y + this.height / 2 - 10, 
                                   8, 14, -0.3, 0, Math.PI * 2);
                        ctx.fill();
                    }

                    // Arms (right)
                    if (Math.random() > 0.5 || this.frameCount % 60 >= 30) {
                        ctx.beginPath();
                        ctx.ellipse(this.x + this.width - 10, this.y + this.height / 2 - 10, 
                                   8, 14, 0.3, 0, Math.PI * 2);
                        ctx.fill();
                    }

                } else {
                    // Draw rock
                    ctx.fillStyle = '#696969';
                    
                    // Main rock body
                    ctx.beginPath();
                    ctx.moveTo(this.x + this.width / 3, this.y + this.height);
                    ctx.lineTo(this.x + this.width * 0.7, this.y + this.height);
                    ctx.quadraticCurveTo(this.x + this.width, this.y + this.height / 2, 
                                        this.x + this.width * 0.85, this.y);
                    ctx.quadraticCurveTo(this.x + this.width / 3, this.y - 10, 
                                        this.x, this.y + this.height / 2);
                    ctx.fill();

                    // Rock texture details
                    ctx.fillStyle = '#707070';
                    ctx.beginPath();
                    ctx.arc(this.x + this.width * 0.3, this.y + this.height * 0.4, 
                            8, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.beginPath();
                    ctx.arc(this.x + this.width * 0.7, this.y + this.height * 0.6, 
                            5, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            checkCollision(alpaca) {
                // Simple AABB collision with slight padding for fairness
                const padding = 8;
                return (alpaca.x + alpaca.width - padding > this.x + padding &&
                        alpaca.x < this.x + this.width - padding &&
                        alpaca.y + alpaca.height - padding > this.y + padding);
            }

            isOffScreen() {
                return this.x + this.width < 0;
            }
        }

        // Particle System for visual effects
        class Particle {
            constructor(x, y, color, velocity) {
                this.x = x;
                this.y = y;
                this.color = color;
                this.vx = (Math.random() - 0.5) * 4 + velocity[0];
                this.vy = (Math.random() - 0.5) * 4 + velocity[1];
                this.life = 1.0;
                this.decay = 0.02 + Math.random() * 0.03;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.vy += 0.15; // gravity for particles
                this.life -= this.decay;
            }

            draw(ctx) {
                ctx.globalAlpha = Math.max(0, this.life);
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, 4 * this.life, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1.0;
            }
        }

        // Floating Text for score display
        class FloatingText {
            constructor(x, y, text) {
                this.x = x;
                this.y = y;
                this.text = text;
                this.life = 1.0;
                this.vy = -2;
            }

            update() {
                this.y += this.vy;
                this.life -= 0.02;
            }

            draw(ctx) {
                ctx.globalAlpha = Math.max(0, this.life);
                ctx.fillStyle = '#FFD700';
                ctx.font = 'bold 36px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(this.text, this.x, this.y);
                ctx.globalAlpha = 1.0;
            }
        }

        // Sound System using Web Audio API
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function playSound(type) {
            if (!audioCtx || audioCtx.state === 'suspended') {
                audioCtx.resume().then(() => {});
            }

            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            switch (type) {
                case 'jump':
                    oscillator.type = 'sine';
                    oscillator.frequency.setValueAtTime(300, audioCtx.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(500, audioCtx.currentTime + 0.1);
                    gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                    oscillator.start(audioCtx.currentTime);
                    oscillator.stop(audioCtx.currentTime + 0.1);
                    break;

                case 'score':
                    oscillator.type = 'triangle';
                    oscillator.frequency.setValueAtTime(600, audioCtx.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(900, audioCtx.currentTime + 0.15);
                    gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                    oscillator.start(audioCtx.currentTime);
                    oscillator.stop(audioCtx.currentTime + 0.15);
                    break;

                case 'crash':
                    oscillator.type = 'sawtooth';
                    oscillator.frequency.setValueAtTime(200, audioCtx.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.3);
                    gainNode.gain.setValueAtTime(0.4, audioCtx.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                    oscillator.start(audioCtx.currentTime);
                    oscillator.stop(audioCtx.currentTime + 0.3);
                    break;

                case 'background':
                    // Subtle ambient sound
                    if (Math.random() > 0.95) {
                        oscillator.type = 'sine';
                        oscillator.frequency.setValueAtTime(100 + Math.random() * 50, audioCtx.currentTime);
                        gainNode.gain.setValueAtTime(0.02, audioCtx.currentTime);
                        oscillator.start(audioCtx.currentTime);
                        oscillator.stop(audioCtx.currentTime + 0.2);
                    }
            }
        }

        // Particle creation helper
        function createParticles(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                gameState.particles.push(new Particle(
                    x, y, color, [Math.random() * 2 - 1, Math.random() * 2 - 1]
                ));
            }
        }

        // Create floating score text
        function showFloatingScore(x, y) {
            gameState.floatingTexts.push(new FloatingText(x, y, '+10'));
        }

        // Game Control Functions
        function startGame() {
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('game-over-screen').style.display = 'none';
            
            if (!audioCtx || audioCtx.state === 'suspended') {
                audioCtx.resume().then(() => {});
            }

            resetGameVariables();
            gameState.isRunning = true;
            gameLoop();
        }

        function resetGame() {
            document.getElementById('game-over-screen').style.display = 'none';
            
            if (!audioCtx || audioCtx.state === 'suspended') {
                audioCtx.resume().then(() => {});
            }

            resetGameVariables();
            gameState.isRunning = true;
        }

        function resetGameVariables() {
            gameState.score = 0;
            gameState.speed = INITIAL_SPEED;
            gameState.frameCount = 0;
            gameState.obstacles = [];
            gameState.particles = [];
            gameState.floatingTexts = [];
            
            alpaca.y = GROUND_Y - alpaca.height;
            alpaca.vy = 0;
            alpaca.isJumping = false;

            updateScoreDisplay();
        }

        function gameOver() {
            gameState.isRunning = false;
            
            // Save high score
            if (gameState.score > gameState.highScore) {
                gameState.highScore = Math.floor(gameState.score);
                localStorage.setItem('ollamaHighScore', gameState.highScore);
            }

            document.getElementById('final-score').textContent = Math.floor(gameState.score);
            document.getElementById('game-over-screen').style.display = 'flex';
            
            playSound('crash');
        }

        function updateScoreDisplay() {
            document.getElementById('score-display').textContent = Math.floor(gameState.score);
            document.getElementById('high-score-display').textContent = gameState.highScore;
        }

        // Main Game Loop
        let lastTime = 0;
        function gameLoop(timestamp) {
            if (!gameState.isRunning || !lastTime) {
                lastTime = timestamp;
                requestAnimationFrame(gameLoop);
                return;
            }

            const deltaTime = timestamp - lastTime;
            lastTime = timestamp;

            // Clear canvas
            const ctx = document.getElementById('gameCanvas').getContext('2d');
            ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            // Update and draw background layers (parallax)
            backgroundLayers.forEach(layer => {
                layer.elements.forEach(el => {
                    el.x -= gameState.speed * layer.speedRatio;
                    
                    if (el.x + el.width < 0) {
                        el.x = CANVAS_WIDTH + Math.random() * 200;
                        el.y = -50 + Math.random() * 100;
                    }

                    ctx.fillStyle = layer.color;
                    ctx.beginPath();
                    
                    if (layer.name === 'farMountains') {
                        // Draw mountain shape
                        ctx.moveTo(el.x, el.y + el.height);
                        ctx.lineTo(el.x + el.width / 2, el.y);
                        ctx.lineTo(el.x + el.width, el.y + el.height);
                    } else {
                        // Draw hill shape
                        ctx.ellipse(
                            el.x + el.width / 2, 
                            el.y + el.height / 2, 
                            el.width / 2, 
                            el.height / 2, 
                            0, 0, Math.PI * 2
                        );
                    }
                    
                    ctx.fill();
                });
            });

            // Draw ground
            ctx.fillStyle = '#8B4513';
            ctx.fillRect(0, GROUND_Y + alpaca.height, CANVAS_WIDTH, CANVAS_HEIGHT - (GROUND_Y + alpaca.height));
            
            // Ground grass detail
            ctx.fillStyle = '#228B22';
            for (let i = 0; i < CANVAS_WIDTH; i += 40) {
                const offset = Math.sin(i * 0.1 + gameState.frameCount * 0.05) * 10;
                ctx.beginPath();
                ctx.moveTo(i - offset, GROUND_Y + alpaca.height);
                ctx.lineTo(i - offset + 20, GROUND_Y + alpaca.height);
                ctx.lineTo(i - offset + 30, GROUND_Y + alpaca.height);
                ctx.fill();
            }

            // Spawn obstacles
            if (gameState.frameCount % Math.floor(150 / gameState.speed) === 0 && 
                gameState.obstacles.length < 3) {
                gameState.obstacles.push(new Obstacle());
            }

            // Update and draw obstacles
            for (let i = gameState.obstacles.length - 1; i >= 0; i--) {
                const obs = gameState.obstacles[i];
                obs.update(gameState.speed);
                obs.draw(ctx);

                if (obs.checkCollision(alpaca)) {
                    gameOver();
                }

                if (obs.isOffScreen()) {
                    gameState.obstacles.splice(i, 1);
                }
            }

            // Update and draw particles
            for (let i = gameState.particles.length - 1; i >= 0; i--) {
                const p = gameState.particles[i];
                p.update();
                p.draw(ctx);
                
                if (p.life <= 0) {
                    gameState.particles.splice(i, 1);
                }
            }

            // Update and draw floating texts
            for (let i = gameState.floatingTexts.length - 1; i >= 0; i--) {
                const ft = gameState.floatingTexts[i];
                ft.update();
                ft.draw(ctx);
                
                if (ft.life <= 0) {
                    gameState.floatingTexts.splice(i, 1);
                }
            }

            // Update and draw alpaca
            alpaca.frameCount = gameState.frameCount;
            alpaca.update();
            alpaca.draw(ctx);

            // Update game state
            gameState.frameCount++;
            
            // Increase score based on distance traveled
            const distanceTraveled = CANVAS_WIDTH - alpaca.x;
            if (distanceTraveled > 0 && Math.floor(gameState.score) % 1 === 0) {
                gameState.score += distanceTraveled * 0.0005;
                
                // Show floating score occasionally
                if (Math.random() < 0.02) {
                    showFloatingScore(alpaca.x + alpaca.width / 2, alpaca.y - 40);
                }
            }

            // Increase speed gradually
            gameState.speed = Math.min(MAX_SPEED, INITIAL_SPEED + gameState.frameCount * SPEED_INCREMENT);

            updateScoreDisplay();

            requestAnimationFrame(gameLoop);
        }

        // Input Handling
        function handleJump() {
            if (gameState.isRunning) {
                alpaca.jump();
            }
        }

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' || e.code === 'ArrowUp') {
                e.preventDefault();
                handleJump();
            }
        });

        document.getElementById('game-container').addEventListener('mousedown', () => {
            handleJump();
        });

        document.getElementById('game-container').addEventListener('touchstart', (e) => {
            e.preventDefault();
            handleJump();
        });

        // Initialize background
        initBackground();

        // Initial high score display
        updateScoreDisplay();
    </script>
</body>
</html>
```

105 t/s, 7222 tokens, 69s, 46%
