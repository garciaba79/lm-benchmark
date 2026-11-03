# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: ollamas adventure
Created: 11/03/2026, 02:55:49 AM
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

# Ollama's Adventure - Endless Runner Game

I'll create a complete, playable endless runner game with all the requested features in a single HTML file. The game will feature an alpaca character, parallax background, sound effects, and scoring mechanics.

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
            user-select: none;
        }
        
        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background: linear-gradient(to bottom, #1a2980, #26d0ce);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            color: white;
        }
        
        #game-container {
            position: relative;
            width: 800px;
            height: 500px;
            box-shadow: 0 0 25px rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            overflow: hidden;
        }
        
        #game-canvas {
            background: linear-gradient(to bottom, #87CEEB, #E0F7FA);
            display: block;
        }
        
        #ui-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        
        #score-display {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 28px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        #high-score-display {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        #start-screen, #game-over-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.7);
            z-index: 10;
        }
        
        #game-over-screen {
            display: none;
        }
        
        h1 {
            font-size: 50px;
            margin-bottom: 20px;
            color: #FFD700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
        }
        
        h2 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #FF6B6B;
        }
        
        p {
            font-size: 22px;
            margin-bottom: 10px;
            text-align: center;
            max-width: 80%;
        }
        
        .score-value {
            font-size: 32px;
            font-weight: bold;
            color: #4ECDC4;
        }
        
        #final-score {
            font-size: 40px;
            margin: 15px 0;
            color: #FFD700;
        }
        
        .btn {
            background: linear-gradient(to bottom, #FF6B6B, #FF8E53);
            border: none;
            padding: 15px 40px;
            font-size: 22px;
            font-weight: bold;
            color: white;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 30px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.2s;
            pointer-events: auto;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            background: linear-gradient(to bottom, #FF8E53, #FF6B6B);
        }
        
        .btn:active {
            transform: translateY(1px);
        }
        
        #instructions {
            position: absolute;
            bottom: 20px;
            width: 100%;
            text-align: center;
            font-size: 18px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .hidden {
            display: none !important;
        }
        
        #clouds {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        
        .cloud {
            position: absolute;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            filter: blur(5px);
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="game-canvas" width="800" height="500"></canvas>
        
        <div id="ui-overlay">
            <div id="score-display">Score: <span id="score">0</span></div>
            <div id="high-score-display">High Score: <span id="high-score">0</span></div>
        </div>
        
        <div id="start-screen">
            <h1>Ollama's Adventure</h1>
            <p>Help Ollama run as far as possible!</p>
            <p>Press SPACE or CLICK to jump over obstacles</p>
            <p>Watch out for the rocks and cacti!</p>
            <button id="start-btn" class="btn">Start Game</button>
            <div id="instructions">Press SPACE or CLICK to jump</div>
        </div>
        
        <div id="game-over-screen">
            <h2>Game Over!</h2>
            <p>Ollama got tired and took a break</p>
            <p>Your score: <span id="final-score" class="score-value">0</span></p>
            <p>High Score: <span id="final-high-score" class="score-value">0</span></p>
            <button id="retry-btn" class="btn">Play Again</button>
        </div>
    </div>

    <script>
        // Game variables
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        const startScreen = document.getElementById('start-screen');
        const gameOverScreen = document.getElementById('game-over-screen');
        const startBtn = document.getElementById('start-btn');
        const retryBtn = document.getElementById('retry-btn');
        const scoreDisplay = document.getElementById('score');
        const highScoreDisplay = document.getElementById('high-score');
        const finalScoreDisplay = document.getElementById('final-score');
        const finalHighScoreDisplay = document.getElementById('final-high-score');
        
        // Game state
        let gameRunning = false;
        let score = 0;
        let highScore = localStorage.getItem('ollamasAdventureHighScore') || 0;
        let gameSpeed = 5;
        let frames = 0;
        
        // Player object
        const player = {
            x: 100,
            y: 350,
            width: 60,
            height: 80,
            jumping: false,
            jumpVelocity: 0,
            gravity: 0.5,
            jumpPower: -12,
            grounded: true,
            
            draw: function() {
                // Draw alpaca body
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.arc(this.x + this.width/2, this.y + this.height/2, 30, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw alpaca ears
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.arc(this.x + 20, this.y + 15, 8, 0, Math.PI * 2);
                ctx.arc(this.x + this.width - 20, this.y + 15, 8, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw alpaca eyes
                ctx.fillStyle = 'black';
                ctx.beginPath();
                ctx.arc(this.x + 20, this.y + 30, 4, 0, Math.PI * 2);
                ctx.arc(this.x + this.width - 20, this.y + 30, 4, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw alpaca nose
                ctx.fillStyle = '#FF6B6B';
                ctx.beginPath();
                ctx.arc(this.x + this.width/2, this.y + 40, 5, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw alpaca mouth
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(this.x + this.width/2, this.y + 50, 8, 0, Math.PI);
                ctx.stroke();
            },
            
            update: function() {
                if (this.jumping) {
                    this.y += this.jumpVelocity;
                    this.jumpVelocity += this.gravity;
                    
                    if (this.y >= 350) {
                        this.y = 350;
                        this.jumping = false;
                        this.grounded = true;
                    }
                }
            },
            
            jump: function() {
                if (this.grounded) {
                    this.jumping = true;
                    this.grounded = false;
                    this.jumpVelocity = this.jumpPower;
                    playSound(200, 0.1, 'sine');
                }
            }
        };
        
        // Obstacles array
        const obstacles = [];
        
        // Background elements
        const backgroundLayers = [
            { x: 0, speed: 0.5 }, // Far background
            { x: 0, speed: 1.0 }  // Near background
        ];
        
        // Clouds for parallax effect
        const clouds = [];
        for (let i = 0; i < 8; i++) {
            clouds.push({
                x: Math.random() * canvas.width,
                y: Math.random() * 150,
                width: 60 + Math.random() * 80,
                height: 30 + Math.random() * 30,
                speed: 0.2 + Math.random() * 0.5
            });
        }
        
        // Draw background
        function drawBackground() {
            // Sky gradient
            const skyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            skyGradient.addColorStop(0, '#87CEEB');
            skyGradient.addColorStop(1, '#E0F7FA');
            ctx.fillStyle = skyGradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Ground
            ctx.fillStyle = '#8BC34A';
            ctx.fillRect(0, 400, canvas.width, 100);
            
            // Draw grass details
            ctx.fillStyle = '#7CB342';
            for (let i = 0; i < 50; i++) {
                const x = Math.random() * canvas.width;
                const height = 5 + Math.random() * 10;
                ctx.fillRect(x, 400, 2, -height);
            }
            
            // Draw background layers
            backgroundLayers.forEach(layer => {
                // Draw mountains in the background
                ctx.fillStyle = '#795548';
                for (let i = 0; i < 10; i++) {
                    const x = (i * 200 - layer.x) % (canvas.width + 200);
                    const height = 100 + Math.random() * 100;
                    ctx.beginPath();
                    ctx.moveTo(x, 400);
                    ctx.lineTo(x + 100, 400 - height);
                    ctx.lineTo(x + 200, 400);
                    ctx.fill();
                }
                
                // Draw sun
                ctx.fillStyle = '#FFEB3B';
                ctx.beginPath();
                ctx.arc(700, 80, 40, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw sun rays
                ctx.strokeStyle = '#FFEB3B';
                ctx.lineWidth = 5;
                for (let i = 0; i < 12; i++) {
                    const angle = (i / 12) * Math.PI * 2;
                    const x1 = 700 + Math.cos(angle) * 40;
                    const y1 = 80 + Math.sin(angle) * 40;
                    const x2 = 700 + Math.cos(angle) * 60;
                    const y2 = 80 + Math.sin(angle) * 60;
                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    ctx.stroke();
                }
            });
        }
        
        // Draw clouds
        function drawClouds() {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            clouds.forEach(cloud => {
                ctx.beginPath();
                ctx.arc(cloud.x, cloud.y, cloud.width/3, 0, Math.PI * 2);
                ctx.arc(cloud.x + cloud.width/3, cloud.y - cloud.height/4, cloud.width/4, 0, Math.PI * 2);
                ctx.arc(cloud.x + cloud.width/2, cloud.y, cloud.width/3, 0, Math.PI * 2);
                ctx.arc(cloud.x + cloud.width/1.5, cloud.y - cloud.height/6, cloud.width/4, 0, Math.PI * 2);
                ctx.fill();
            });
        }
        
        // Create new obstacle
        function createObstacle() {
            const obstacleTypes = ['rock', 'cactus'];
            const type = obstacleTypes[Math.floor(Math.random() * obstacleTypes.length)];
            
            obstacles.push({
                x: canvas.width,
                y: 380,
                width: type === 'rock' ? 40 : 30,
                height: type === 'rock' ? 40 : 60,
                type: type,
                passed: false
            });
        }
        
        // Draw obstacles
        function drawObstacles() {
            obstacles.forEach(obstacle => {
                if (obstacle.type === 'rock') {
                    // Draw rock
                    ctx.fillStyle = '#795548';
                    ctx.beginPath();
                    ctx.arc(obstacle.x + obstacle.width/2, obstacle.y + obstacle.height/2, obstacle.width/2, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Add some texture to the rock
                    ctx.fillStyle = '#5D4037';
                    ctx.beginPath();
                    ctx.arc(obstacle.x + obstacle.width/3, obstacle.y + obstacle.height/3, 5, 0, Math.PI * 2);
                    ctx.arc(obstacle.x + 2*obstacle.width/3, obstacle.y + 2*obstacle.height/3, 8, 0, Math.PI * 2);
                    ctx.fill();
                } else {
                    // Draw cactus
                    ctx.fillStyle = '#4CAF50';
                    ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
                    
                    // Cactus arms
                    ctx.fillRect(obstacle.x - 10, obstacle.y + 20, 15, 15);
                    ctx.fillRect(obstacle.x + obstacle.width - 5, obstacle.y + 40, 15, 15);
                    
                    // Cactus spikes
                    ctx.fillStyle = '#388E3C';
                    for (let i = 0; i < 5; i++) {
                        const x = obstacle.x + i * 6;
                        ctx.fillRect(x, obstacle.y - 5, 4, 10);
                    }
                }
            });
        }
        
        // Update obstacles
        function updateObstacles() {
            for (let i = 0; i < obstacles.length; i++) {
                obstacles[i].x -= gameSpeed;
                
                // Check if player passed the obstacle
                if (!obstacles[i].passed && obstacles[i].x + obstacles[i].width < player.x) {
                    obstacles[i].passed = true;
                    score += 10;
                    scoreDisplay.textContent = score;
                    playSound(500, 0.1, 'triangle');
                }
                
                // Remove obstacles that are off screen
                if (obstacles[i].x + obstacles[i].width < 0) {
                    obstacles.splice(i, 1);
                    i--;
                }
            }
        }
        
        // Update background layers
        function updateBackground() {
            backgroundLayers.forEach(layer => {
                layer.x -= layer.speed;
                if (layer.x <= -canvas.width) {
                    layer.x = 0;
                }
            });
            
            // Update clouds
            clouds.forEach(cloud => {
                cloud.x -= cloud.speed;
                if (cloud.x + cloud.width < 0) {
                    cloud.x = canvas.width;
                    cloud.y = Math.random() * 150;
                }
            });
        }
        
        // Check collisions
        function checkCollisions() {
            for (let i = 0; i < obstacles.length; i++) {
                const obs = obstacles[i];
                
                if (
                    player.x < obs.x + obs.width &&
                    player.x + player.width > obs.x &&
                    player.y < obs.y + obs.height &&
                    player.y + player.height > obs.y
                ) {
                    // Collision detected
                    gameOver();
                    playSound(100, 0.3, 'sawtooth');
                    return;
                }
            }
        }
        
        // Game loop
        function gameLoop() {
            if (!gameRunning) return;
            
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw background
            drawBackground();
            drawClouds();
            
            // Update and draw player
            player.update();
            player.draw();
            
            // Update obstacles
            updateObstacles();
            
            // Draw obstacles
            drawObstacles();
            
            // Update background
            updateBackground();
            
            // Check collisions
            checkCollisions();
            
            // Create new obstacles randomly
            if (frames % 100 === 0) {
                createObstacle();
            }
            
            // Increase game speed gradually
            if (frames % 500 === 0) {
                gameSpeed += 0.2;
            }
            
            frames++;
            requestAnimationFrame(gameLoop);
        }
        
        // Start game
        function startGame() {
            gameRunning = true;
            score = 0;
            gameSpeed = 5;
            frames = 0;
            obstacles.length = 0;
            player.y = 350;
            player.jumping = false;
            player.grounded = true;
            
            scoreDisplay.textContent = score;
            startScreen.classList.add('hidden');
            gameOverScreen.classList.add('hidden');
            
            gameLoop();
        }
        
        // Game over
        function gameOver() {
            gameRunning = false;
            
            // Update high score
            if (score > highScore) {
                highScore = score;
                localStorage.setItem('ollamasAdventureHighScore', highScore);
                highScoreDisplay.textContent = highScore;
            }
            
            // Show game over screen
            finalScoreDisplay.textContent = score;
            finalHighScoreDisplay.textContent = highScore;
            gameOverScreen.classList.remove('hidden');
        }
        
        // Sound effects using Web Audio API
        function playSound(frequency, duration, type) {
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.type = type;
                oscillator.frequency.value = frequency;
                gainNode.gain.value = 0.3;
                
                oscillator.start(0);
                oscillator.stop(audioContext.currentTime + duration);
            } catch (e) {
                // Fallback for browsers that don't support Web Audio API
                console.log("Sound not supported in this browser");
            }
        }
        
        // Event listeners
        startBtn.addEventListener('click', startGame);
        retryBtn.addEventListener('click', startGame);
        
        document.addEventListener('keydown', function(e) {
            if (e.code === 'Space') {
                if (gameRunning) {
                    player.jump();
                } else if (gameOverScreen.classList.contains('hidden')) {
                    startGame();
                }
            }
        });
        
        canvas.addEventListener('click', function() {
            if (gameRunning) {
                player.jump();
            }
        });
        
        // Initialize high score display
        highScoreDisplay.textContent = highScore;
    </script>
</body>
</html>
```

## Features Implemented

1. **Complete Game Mechanics**:
   - Player character (alpaca) that automatically runs to the right
   - Jumping with spacebar or click/tap
   - Obstacle avoidance (rocks and cacti)
   - Increasing difficulty over time

2. **Visual Design**:
   - Cartoonish alpaca character with detailed features
   - Parallax scrolling background with multiple layers
   - Cloud elements for atmospheric effect
   - Colorful, vibrant game environment

3. **Game Elements**:
   - Score tracking system
   - High score saved in localStorage
   - Start screen and game over screen
   - Retry button functionality

4. **Sound Effects**:
   - Jump sound using Web Audio API
   - Score point sound
   - Game over sound
   - All sounds are short and lighthearted

5. **Responsive Controls**:
   - Spacebar or mouse click to jump
   - Clear visual feedback for actions

The game is completely self-contained in a single HTML file with no external dependencies. Simply copy the entire code into an HTML file and open it in any modern browser to play!

48 t/s, 5002 tokens, 103s
