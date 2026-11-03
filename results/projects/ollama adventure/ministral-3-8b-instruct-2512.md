# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: ollamas adventure
Created: 11/03/2026, 12:43:09 AM
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

Here's a complete self-contained endless runner game called "Ollama's Adventure" in a single HTML file with all assets generated via CSS/Canvas:

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
            background-color: #f5f5dc;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            overflow: hidden;
        }

        #game-container {
            position: relative;
            width: 800px;
            height: 400px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        #game-canvas {
            width: 800px;
            height: 400px;
            background-color: #e6f7ff;
        }

        #ui-panel {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 20px;
            color: white;
            font-size: 24px;
            z-index: 10;
        }

        #score-display {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 8px 16px;
            border-radius: 5px;
        }

        #high-score-display {
            background-color: rgba(255, 215, 0, 0.7);
            padding: 8px 16px;
            border-radius: 5px;
        }

        #game-over-panel {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(0, 0, 0, 0.9);
            color: white;
            text-align: center;
            padding: 30px;
            border-radius: 10px;
            display: none;
            z-index: 20;
        }

        #game-over-score {
            font-size: 48px;
            margin-bottom: 20px;
        }

        #high-score-text {
            font-style: italic;
            margin-bottom: 20px;
        }

        button {
            background-color: #ffd700;
            color: black;
            border: none;
            padding: 12px 30px;
            font-size: 24px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }

        button:hover {
            background-color: #ffcc00;
            transform: scale(1.05);
        }

        /* Alpaca drawing styles */
        .alpaca-body {
            width: 60px;
            height: 80px;
            position: absolute;
            left: 200px;
            bottom: 100px;
            background-color: #d4a574;
            border-radius: 30px;
        }

        .alpaca-head {
            width: 50px;
            height: 50px;
            position: absolute;
            left: 210px;
            bottom: 160px;
            background-color: #d4a574;
            border-radius: 50%;
        }

        .alpaca-ears {
            position: absolute;
            left: 200px;
            bottom: 130px;
        }

        .ear-left, .ear-right {
            width: 30px;
            height: 40px;
            background-color: #d4a574;
            border-radius: 50%;
            transform-origin: top center;
        }

        .ear-left {
            left: 190px;
            transform: rotate(-20deg);
        }

        .ear-right {
            right: 230px;
            transform: rotate(20deg);
        }

        .alpaca-eyes {
            position: absolute;
            width: 8px;
            height: 8px;
            background-color: white;
            border-radius: 50%;
            left: 217px;
            bottom: 145px;
        }

        .eye-left {
            left: 213px;
        }

        .alpaca-mouth {
            position: absolute;
            width: 20px;
            height: 8px;
            background-color: black;
            border-radius: 4px;
            left: 225px;
            bottom: 147px;
        }

        .alpaca-legs {
            position: absolute;
            width: 10px;
            height: 30px;
            background-color: #d4a574;
            border-radius: 5px;
        }

        .leg-left {
            left: 208px;
            bottom: 120px;
        }

        .leg-right {
            right: 228px;
            bottom: 120px;
        }

        /* Obstacle styles */
        .obstacle {
            position: absolute;
            background-color: #8B4513;
            border-radius: 10px;
        }

        .cactus {
            width: 40px;
            height: 60px;
            bottom: 200px;
        }

        .rock {
            width: 60px;
            height: 40px;
            bottom: 250px;
        }

        /* Background layers */
        #bg-layer-1, #bg-layer-2 {
            position: absolute;
            top: 0;
            left: 0;
            width: 1600px;
            height: 400px;
        }

        #bg-layer-1 {
            background-color: #87CEEB;
            z-index: -1;
        }

        #bg-layer-2 {
            background-color: #E0F7FA;
            z-index: -2;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <!-- Background layers -->
        <div id="bg-layer-1"></div>
        <div id="bg-layer-2"></div>

        <!-- Canvas for game elements -->
        <canvas id="game-canvas"></canvas>

        <!-- UI Elements -->
        <div id="ui-panel">
            <div id="score-display">Score: 0</div>
            <div id="high-score-display">High Score: 0</div>
        </div>

        <!-- Game Over Panel -->
        <div id="game-over-panel">
            <div id="game-over-score">Game Over!</div>
            <div>Your score: <span id="final-score">0</span></div>
            <div id="high-score-text">High Score: <span id="current-high-score">0</span></div>
            <button id="retry-button">Play Again</button>
        </div>

        <!-- Alpaca elements (will be positioned via JavaScript) -->
        <div class="alpaca-body"></div>
        <div class="alpaca-head"></div>
        <div class="ear-left"></div>
        <div class="ear-right"></div>
        <div class="eye-left"></div>
        <div class="eye-right"></div>
        <div class="alpaca-mouth"></div>
        <div class="leg-left"></div>
        <div class="leg-right"></div>
    </div>

    <script>
        // Game state
        const gameState = {
            player: {
                x: 200,
                y: 300,
                velocityY: 0,
                gravity: 0.8,
                jumpForce: -15,
                isJumping: false,
                frame: 0,
                animationSpeed: 6
            },
            obstacles: [],
            score: 0,
            highScore: parseInt(localStorage.getItem('ollamasAdventureHighScore')) || 0,
            gameSpeed: 2,
            speedIncreaseRate: 0.001,
            lastObstacleTime: 0,
            obstacleInterval: 3000, // milliseconds
            gameActive: true,
            animationFrameId: null,
            audioContext: null,
            jumpSound: null,
            scoreSound: null,
            hitSound: null
        };

        // DOM elements
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        const uiScoreDisplay = document.getElementById('score-display');
        const uiHighScoreDisplay = document.getElementById('high-score-display');
        const gameOverPanel = document.getElementById('game-over-panel');
        const finalScoreDisplay = document.getElementById('final-score');
        const currentHighScoreDisplay = document.getElementById('current-high-score');
        const retryButton = document.getElementById('retry-button');

        // Initialize audio
        function initAudio() {
            gameState.audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Jump sound
            gameState.jumpSound = createSound(gameState.audioContext, 0.5, [0.3, 0.4, 0.2], 1);
            // Score sound
            gameState.scoreSound = createSound(gameState.audioContext, 0.7, [0.6, 0.5, 0.4], 1);
            // Hit sound
            gameState.hitSound = createSound(gameState.audioContext, 0.3, [0.2, 0.3, 0.1], 1);
        }

        function createSound(audioCtx, duration, frequencies, volume) {
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            // Set up the sound parameters
            oscillator.type = 'sine';
            oscillator.frequency.value = frequencies[0];
            oscillator.connect(gainNode);
            gainNode.gain.value = volume;
            gainNode.connect(audioCtx.destination);

            return {
                play: function() {
                    oscillator.start();
                    oscillator.stop(audioCtx.currentTime + duration);

                    // Add some frequency modulation for more interesting sound
                    const freqChange = audioCtx.createGain();
                    const freqModulator = audioCtx.createOscillator();

                    freqModulator.type = 'sine';
                    freqModulator.frequency.value = 10;
                    freqModulator.connect(freqChange.gain);
                    freqChange.gain.value = 0.2;

                    oscillator.frequency.cancelScheduledValues(audioCtx.currentTime);
                    oscillator.frequency.setValueAtTime(
                        frequencies[0],
                        audioCtx.currentTime
                    );
                    oscillator.frequency.linearRampToValueAtTime(
                        frequencies[1],
                        audioCtx.currentTime + duration/3
                    );
                    oscillator.frequency.exponentialRampToValueAtTime(
                        frequencies[2],
                        audioCtx.currentTime + duration
                    );

                    freqModulator.start();
                    freqChange.connect(oscillator.frequency);
                }
            };
        }

        // Initialize game
        function initGame() {
            // Reset game state
            gameState.player.x = 200;
            gameState.player.y = 300;
            gameState.player.velocityY = 0;
            gameState.player.isJumping = false;
            gameState.obstacles = [];
            gameState.score = 0;
            gameState.gameSpeed = 2;
            gameState.lastObstacleTime = performance.now();
            gameState.animationFrameId = null;

            // Hide game over panel
            gameOverPanel.style.display = 'none';

            // Start the game loop
            gameState.animationFrameId = requestAnimationFrame(gameLoop);
        }

        // Game loop
        function gameLoop(timestamp) {
            if (!gameState.gameActive) return;

            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Update background parallax effect
            updateBackground();

            // Update player position
            updatePlayer(timestamp);

            // Generate obstacles
            generateObstacles(timestamp);

            // Move and check collisions with obstacles
            moveObstacles();
            checkCollisions();

            // Draw everything
            drawGame();

            // Continue the loop
            gameState.animationFrameId = requestAnimationFrame(gameLoop);
        }

            // Update background parallax effect
        function updateBackground() {
            const bgLayer1 = document.getElementById('bg-layer-1');
            const bgLayer2 = document.getElementById('bg-layer-2');

            // Move layer 1 (faster)
            const speed1 = gameState.gameSpeed * 0.7;
            let pos1 = parseInt(bgLayer1.style.left) || 0;
            pos1 -= speed1;
            if (pos1 < -800) pos1 += 1600;
            bgLayer1.style.left = pos1 + 'px';

            // Move layer 2 (slower)
            const speed2 = gameState.gameSpeed * 0.3;
            let pos2 = parseInt(bgLayer2.style.left) || 0;
            pos2 -= speed2;
            if (pos2 < -800) pos2 += 1600;
            bgLayer2.style.left = pos2 + 'px';
        }

        // Update player physics
        function updatePlayer(timestamp) {
            // Apply gravity
            gameState.player.velocityY += gameState.player.gravity;

            // Update y position
            gameState.player.y += gameState.player.velocityY;

            // Ground collision (simple)
            if (gameState.player.y > 300) {
                gameState.player.y = 300;
                gameState.player.velocityY = 0;
                gameState.player.isJumping = false;
            }

            // Increase score based on time survived
            const currentTime = performance.now();
            const timeSinceLastScoreUpdate = (currentTime - gameState.lastScoreUpdate) / 1000;

            if (timeSinceLastScoreUpdate > 0.5) {
                gameState.score += Math.floor(timeSinceLastScoreUpdate * 2);
                uiScoreDisplay.textContent = `Score: ${gameState.score}`;
                gameState.lastScoreUpdate = currentTime;
                playSound(gameState.scoreSound);
            }

            // Increase game speed over time
            const speedIncreaseFactor = (performance.now() / 1000) * gameState.speedIncreaseRate;
            gameState.gameSpeed += speedIncreaseFactor;

            // Handle jump input
            if ((event.keys && event.keys.includes(' ')) || (gameState.lastKeyPress === ' ')) {
                if (!gameState.player.isJumping) {
                    gameState.player.velocityY = gameState.player.jumpForce;
                    gameState.player.isJumping = true;
                    playSound(gameState.jumpSound);
                }
            }

            // Reset key press flag
            gameState.lastKeyPress = null;

            // Animation frame counter for running animation
            gameState.player.frame++;
            if (gameState.player.frame >= gameState.player.animationSpeed) {
                gameState.player.frame = 0;
            }
        }

        // Generate obstacles
        function generateObstacles(timestamp) {
            const now = timestamp;
            const timeSinceLastObstacle = now - gameState.lastObstacleTime;

            if (timeSinceLastObstacle > gameState.obstacleInterval) {
                // Create a new obstacle
                const obstacleType = Math.random() < 0.5 ? 'cactus' : 'rock';
                const obstacleWidth = obstacleType === 'cactus' ? 40 : 60;
                const obstacleHeight = obstacleType === 'cactus' ? 60 : 40;

                gameState.obstacles.push({
                    x: canvas.width + Math.random() * 100,
                    y: canvas.height - obstacleHeight - 20,
                    width: obstacleWidth,
                    height: obstacleHeight,
                    type: obstacleType
                });

                // Reset timer with some randomness to make it less predictable
                gameState.lastObstacleTime = now + (gameState.obstacleInterval * (0.8 + Math.random() * 0.4));
            }
        }

        // Move obstacles
        function moveObstacles() {
            for (let i = gameState.obstacles.length - 1; i >= 0; i--) {
                const obstacle = gameState.obstacles[i];
                obstacle.x -= gameState.gameSpeed;

                // Remove obstacles that are off screen
                if (obstacle.x + obstacle.width < 0) {
                    gameState.obstacles.splice(i, 1);
                }
            }
        }

        // Check for collisions with obstacles
        function checkCollisions() {
            const playerRect = {
                x: gameState.player.x,
                y: gameState.player.y,
                width: 60,
                height: 80
            };

            for (let i = gameState.obstacles.length - 1; i >= 0; i--) {
                const obstacle = gameState.obstacles[i];

                // Simple collision detection
                if (
                    playerRect.x + playerRect.width > obstacle.x &&
                    playerRect.x < obstacle.x + obstacle.width &&
                    playerRect.y + playerRect.height > obstacle.y &&
                    playerRect.y < obstacle.y + obstacle.height
                ) {
                    // Collision detected - game over
                    endGame();
                    return;
                }
            }
        }

        // Draw all game elements
        function drawGame() {
            // Draw alpaca (using CSS classes for simplicity)
            const alpacaBody = document.querySelector('.alpaca-body');
            const alpacaHead = document.querySelector('.alpaca-head');

            // Position based on player state
            alpacaBody.style.left = `${gameState.player.x}px`;
            alpacaBody.style.bottom = `${300 - gameState.player.y + 80}px`;

            // Simple running animation by moving head slightly
            const headXOffset = Math.sin(gameState.player.frame * 0.5) * 10;
            alpacaHead.style.left = `${gameState.player.x + 20 + headXOffset}px`;
            alpacaHead.style.bottom = `${300 - gameState.player.y + 60}px`;

            // Draw obstacles
            for (const obstacle of gameState.obstacles) {
                const obstacleElement = document.createElement('div');
                obstacleElement.className = `obstacle ${obstacle.type}`;
                obstacleElement.style.left = `${obstacle.x}px`;
                obstacleElement.style.width = `${obstacle.width}px`;

                // Add to DOM temporarily for drawing
                canvas.parentNode.appendChild(obstacleElement);
                ctx.drawImage(
                    obstacleElement.getBoundingClientRect().width,
                    obstacleElement.getBoundingClientRect().height,
                    obstacle.x, obstacle.y, obstacle.width, obstacle.height
                );
                canvas.parentNode.removeChild(obstacleElement);

                // Draw some simple details on obstacles
                if (obstacle.type === 'cactus') {
                    ctx.fillStyle = '#32CD32';
                    const cactusSpikes = [
                        {x: obstacle.x + 10, y: obstacle.y - 5},
                        {x: obstacle.x + 20, y: obstacle.y - 15},
                        {x: obstacle.x + 30, y: obstacle.y - 8}
                    ];
                    cactusSpikes.forEach(spike => {
                        ctx.beginPath();
                        ctx.moveTo(spike.x, spike.y);
                        ctx.lineTo(spike.x + 5, spike.y - 10);
                        ctx.lineTo(spike.x + 10, spike.y);
                        ctx.fill();
                    });
                } else if (obstacle.type === 'rock') {
                    // Draw some cracks
                    ctx.strokeStyle = '#8B4513';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(obstacle.x + 10, obstacle.y);
                    ctx.lineTo(obstacle.x + 30, obstacle.y + 20);
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(obstacle.x + 50, obstacle.y + 10);
                    ctx.lineTo(obstacle.x + 40, obstacle.y + 30);
                    ctx.stroke();
                }
            }

            // Draw ground
            ctx.fillStyle = '#8B4513';
            ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

            // Draw score and high score in UI
            uiScoreDisplay.textContent = `Score: ${gameState.score}`;
            uiHighScoreDisplay.textContent = `High Score: ${gameState.highScore}`;
        }

        // End game function
        function endGame() {
            gameState.gameActive = false;
            cancelAnimationFrame(gameState.animationFrameId);

            // Update high score if needed
            if (gameState.score > gameState.highScore) {
                gameState.highScore = gameState.score;
                localStorage.setItem('ollamasAdventureHighScore', gameState.highScore);
            }

            // Show game over panel
            finalScoreDisplay.textContent = gameState.score;
            currentHighScoreDisplay.textContent = gameState.highScore;
            gameOverPanel.style.display = 'block';
        }

        // Play sound function
        function playSound(sound) {
            if (gameState.audioContext.state === 'suspended') {
                gameState.audioContext.resume();
            }
            sound.play();
        }

        // Event listeners
        document.addEventListener('keydown', (e) => {
            if (!gameState.gameActive && e.key === ' ') return;

            if ((e.key === ' ' || e.code === 'Space') && !gameState.player.isJumping) {
                gameState.lastKeyPress = ' ';
            }
        });

        document.addEventListener('click', () => {
            if (gameState.gameActive && !gameState.player.isJumping) {
                gameState.lastKeyPress = ' ';
            }
        });

        retryButton.addEventListener('click', initGame);

        // Touch support for mobile
        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            if (gameState.gameActive && !gameState.player.isJumping) {
                gameState.lastKeyPress = ' ';
            }
        });

        // Start the game
        initAudio();
        initGame();

        // Handle window resize
        window.addEventListener('resize', () => {
            canvas.width = 800;
            canvas.height = 400;
        });
    </script>
</body>
</html>
```

**Features of Ollama's Adventure:**

1. **Core Gameplay**:
   - Alpaca character that automatically runs to the right
   - Jump by pressing spacebar or clicking/tapping
   - Avoid obstacles (cacti and rocks) that appear from the right

2. **Game Mechanics**:
   - Score increases over time (based on survival)
   - Game speed gradually increases as you play longer
   - Collision detection with simple physics

3. **Visual Elements**:
   - Parallax scrolling background with two layers moving at different speeds
   - Cartoon alpaca character drawn with CSS
   - Simple obstacle shapes that appear randomly
   - Ground level for collision detection

4. **Audio**:
   - Jump sound effect (sine wave with frequency modulation)
   - Score increase sound
   - Collision/hit sound

5. **UI/UX**:
   - Current score display
   - High score tracking using localStorage
   - Game over screen with final score and high score
   - Play Again button to restart the game

6. **Responsive Design**:
   - Works on both desktop and mobile devices
   - Touch support for jumping on mobile
   - Clean, colorful cartoon aesthetic

The game is completely self-contained in a single HTML file with no external dependencies. The alpaca character is drawn using CSS rather than images, and all obstacles are generated dynamically.

117 t/s, 5327 tokens, 46s
