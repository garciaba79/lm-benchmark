# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: ollamas adventure
Created: 11/03/2026, 12:35:31 AM
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

This is a complete, self-contained, playable endless runner game called "ollama's Adventure" written entirely in one HTML file using inline CSS and JavaScript. It incorporates canvas drawing for graphics, Web Audio API for sound effects, and localStorage for high scores, meeting all specified requirements.

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
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f8ff; /* Light sky background for the body */
            font-family: 'Comic Sans MS', cursive, sans-serif;
            overflow: hidden;
            user-select: none; /* Prevent text selection during gameplay */
        }

        #gameContainer {
            position: relative;
            width: 800px;
            height: 350px;
            border: 4px solid #4a2e1d; /* Brown border for the game area */
            background-color: #bfe6ff; /* Sky color within canvas boundary */
            overflow: hidden;
        }

        #gameCanvas {
            display: block;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }

        #uiOverlay {
            width: 800px;
            margin-top: 20px;
            text-align: center;
            padding: 10px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        #scoreDisplay, #highScoreDisplay {
            font-size: 2em;
            color: #38761d; /* Green for score */
            margin: 5px 0;
        }

        #gameOverScreen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            display: none; /* Hidden by default */
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            z-index: 10;
        }

        #gameOverScreen h2 {
            font-size: 3em;
            margin-bottom: 10px;
            color: #ff6b6b; /* Reddish for game over */
        }

        #finalScoreText {
            font-size: 1.5em;
            margin-bottom: 20px;
        }

        #retryButton {
            padding: 15px 30px;
            font-size: 1.2em;
            cursor: pointer;
            background-color: #4CAF50; /* Green button */
            color: white;
            border: none;
            border-radius: 8px;
            transition: background-color 0.2s;
        }

        #retryButton:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>

    <h1>⛰️ ollama's Adventure 🏞️</h1>

    <div id="gameContainer">
        <canvas id="gameCanvas"></canvas>
        <div id="gameOverScreen">
            <h2>Game Over!</h2>
            <p id="finalScoreText">Your Score: 0 | High Score: 0</p>
            <button id="retryButton">Play Again</button>
        </div>
    </div>

    <div id="uiOverlay">
        <div id="scoreDisplay">Score: 0</div>
        <div id="highScoreDisplay">High Score: 0</div>
    </div>

    <script>
        // --- Game Setup and Constants ---
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const gameContainer = document.getElementById('gameContainer');
        const scoreDisplay = document.getElementById('scoreDisplay');
        const highScoreDisplay = document.getElementById('highScoreDisplay');
        const gameOverScreen = document.getElementById('gameOverScreen');
        const retryButton = document.getElementById('retryButton');

        // Set canvas dimensions to match container size for responsiveness
        canvas.width = 800;
        canvas.height = 350;

        const GRAVITY = 1.0;
        const JUMP_VELOCITY = -20;
        const GROUND_Y = canvas.height - 40; // Altitude where alpaca stands

        let gameLoopId;
        let isGameOver = true;
        let score = 0;
        let highScore = localStorage.getItem('ollamaHighScore') || 0;

        // Player State (The Alpaca)
        const player = {
            x: 50,
            y: GROUND_Y - 20, // Initial ground position + alpaca height offset
            width: 30,
            height: 40,
            velocityY: 0,
            isJumping: false,
            isAlive: true
        };

        // Obstacle State
        let obstacles = [];
        const OBSTACLE_SPEED_MIN = 5;
        const OBSTACLE_GAP_TIME = 1.5; // Seconds between spawns (adjusted by speed)

        // Background & Speed Control
        let gameSpeed = 6; // Initial horizontal scrolling speed
        let scoreTimer = 0;
        let lastSpawnTime = 0;

        // Parallax Background Layers
        const background = {
            layers: [
                { speedFactor: 0.1, height: 50, color: '#90ee90' }, // Far grass/hills (slowest)
                { speedFactor: 0.5, height: 30, color: '#6b8e23' }  // Near ground detail (medium)
            ],
            scrollX: { 1: 0, 2: 0 } // Tracks horizontal offset for seamless looping
        };

        // --- Sound Management (Web Audio API) ---
        let audioContext;

        function initAudio() {
            try {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            } catch(e) {
                console.warn("Web Audio API not supported. Sounds will be disabled.");
                audioContext = null;
            }
        }

        // Simple tone generator for effects
        function playSound(frequency, duration, type = 'sine', volume = 0.5) {
            if (!audioContext) return;

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.type = type;
            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);

            // Envelope shaping for quick clicks/jumps
            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(volume, audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        }

        function playJumpSound() {
            playSound(350, 0.15, 'square', 0.7);
        }

        function playScoreSound() {
            playSound(600, 0.1, 'sine', 0.5);
        }

        function playHitSound() {
            playSound(80, 0.4, 'sawtooth', 1.0);
        }


        // --- Game Logic Functions ---

        function resetGame() {
            player.y = GROUND_Y - player.height;
            player.velocityY = 0;
            player.isJumping = false;
            obstacles = [];
            score = 0;
            gameSpeed = 6;
            lastSpawnTime = performance.now();
            scoreTimer = 0;
            isGameOver = false;
            
            // UI Setup
            gameOverScreen.style.display = 'none';
            updateScoreDisplay();

            if (gameLoopId) {
                cancelAnimationFrame(gameLoopId);
            }
            gameLoopId = requestAnimationFrame(gameUpdate);
        }

        function gameOver() {
            isGameOver = true;
            playHitSound();
            
            // Update High Score
            if (score > highScore) {
                highScore = score;
                localStorage.setItem('ollamaHighScore', highScore);
            }

            document.getElementById('finalScoreText').textContent = 
                `Your Score: ${Math.floor(score)} | High Score: ${Math.floor(highScore)}`;
            document.getElementById('highScoreDisplay').textContent = `High Score: ${Math.floor(highScore)}`;
            
            retryButton.disabled = false;
            gameOverScreen.style.display = 'flex';

            cancelAnimationFrame(gameLoopId);
        }

        function jump() {
            if (player.isJumping || isGameOver) return;
            
            // Jump physics application
            player.velocityY = JUMP_VELOCITY;
            player.isJumping = true;
            playJumpSound();
        }

        function updatePlayer(deltaTime) {
            if (player.isJumping) {
                // Apply gravity and update vertical position
                player.velocityY += GRAVITY * (deltaTime / 16); // Scale gravity effect by delta time approximation
                player.y += player.velocityY;
                
                // Check if landed back on the ground
                if (player.y + player.height > GROUND_Y) {
                    player.y = GROUND_Y - player.height;
                    player.velocityY = 0;
                    player.isJumping = false;
                }
            }
        }

        function spawnObstacle(currentTime) {
            if (currentTime - lastSpawnTime > OBSTACLE_GAP_TIME / (gameSpeed / 6)) { // Adjust interval based on speed scale
                const minHeight = 20;
                const maxHeight = 60;
                const gapSize = 150;

                // Calculate random height for the obstacle pair
                const topHeight = Math.floor(Math.random() * (maxHeight - minHeight) + minHeight);
                const bottomHeight = Math.floor(Math.random() * (maxHeight - minHeight) + minHeight);

                obstacles.push({
                    x: canvas.width,
                    yTop: GROUND_Y - topHeight, // Top part starts from ground up
                    heightTop: topHeight,
                    yBottomStart: GROUND_Y,   // Bottom edge of the obstacle area
                    heightBottom: bottomHeight,
                    passed: false
                });

                lastSpawnTime = currentTime;
            }
        }

        function updateObstacles(deltaTime) {
            const travelDistance = gameSpeed * (deltaTime / 16); // Scale movement by delta time
            
            // Move obstacles
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= travelDistance;

                // Check for passing player (Scoring)
                const playerRight = player.x + player.width;
                if (obstacles[i].x + 5 <= playerRight && !obstacles[i].passed) {
                    score += 10; // Score points for passing
                    playScoreSound();
                    obstacles[i].passed = true;
                    updateScoreDisplay();
                }

                // Remove obstacle if it goes off screen
                if (obstacles[i].x + 5 < 0) {
                    obstacles.splice(i, 1);
                }
            }
        }

        function checkCollision() {
            const playerRight = player.x + player.width;
            const playerBottom = player.y + player.height;

            for (const obs of obstacles) {
                // Simplified AABB collision check against the ground-based obstacle structure
                if (playerRight > obs.x && 
                    player.x < obs.x + 50 && // Collision width range for the obstacle block
                    (playerBottom >= GROUND_Y - Math.min(obs.heightTop, 2) && player.y <= GROUND_Y)) {
                    
                    // Check if collision occurs in the main hazard zone (between top and bottom parts)
                    const collisionHappened = (
                        (playerRight > obs.x + 10 && player.y < GROUND_Y - obs.heightTop) || // Hit the 'ceiling' part of a ground obstacle gap
                        (playerRight > obs.x + 10 && playerBottom > GROUND_Y) // Should not happen if physics is perfect, but included for robustness
                    );

                    if (collisionHappened) {
                        gameOver();
                        return true;
                    }
                }
            }
            return false;
        }


        // --- Drawing Functions ---

        function drawBackground() {
            // 1. Draw Sky/Ground Plane (Base layer drawn by container background, but we redraw the ground line)
            ctx.fillStyle = '#8fbc8f'; // Greenish ground color
            ctx.fillRect(0, GROUND_Y + 20, canvas.width, canvas.height - GROUND_Y);

            // 2. Parallax Scrolling Layers
            const currentSpeedRatio = gameSpeed / 6; // How much faster than the baseline scroll speed

            background.layers.forEach((layer, index) => {
                ctx.fillStyle = layer.color;
                
                // Draw repeating pattern based on offset
                for (let x = -100 * Math.abs(index), i = 0; x < canvas.width + 100; x += 200) {
                    // Use the stored scrollX to determine the base drawing position, looping effect
                    const drawX = (x + background.scrollX[index]) % 200 - 200;
                    ctx.fillRect(drawX, GROUND_Y - layer.height, 200, layer.height);
                }
            });

            // Update scroll position for next frame (seamless loop)
            background.scrollX[1] = (background.scrollX[1] + currentSpeedRatio * 5) % 400;
            background.scrollX[0] = (background.scrollX[0] + currentSpeedRatio * 2) % 400;
        }

        function drawPlayer() {
            // Simple cartoon alpaca drawing using basic shapes and colors
            ctx.save();
            ctx.translate(player.x, player.y);

            // Body (Light Brown/Cream)
            ctx.fillStyle = '#e5d8b3';
            ctx.beginPath();
            ctx.arc(15, 0, 20, Math.PI, 0); // Simple body approximation
            ctx.fill();

            // Head/Face (Slightly darker)
            ctx.fillStyle = '#c4b49a';
            ctx.fillRect(10, -10, 20, 15); // Simplified head box
            
            // Ears (Pinkish interior)
            ctx.fillStyle = '#ffcccb';
            ctx.beginPath();
            ctx.arc(12, -18, 4, 0, Math.PI * 2);
            ctx.fill();

            // Legs/Feet (Visible when on ground)
            if (!player.isJumping && player.y + player.height >= GROUND_Y) {
                 ctx.fillStyle = '#967a58';
                 ctx.fillRect(10, 30, 5, 10);
                 ctx.fillRect(20, 30, 5, 10);
            }


            ctx.restore();
        }

        function drawObstacles() {
            for (const obs of obstacles) {
                // Draw the solid obstacle block structure
                const blockWidth = 40;
                const bottomY = GROUND_Y - 5; // Slightly below ground line for effect

                // Top Hazard Block
                ctx.fillStyle = '#c62828'; // Reddish danger color
                ctx.fillRect(obs.x, obs.yTop, blockWidth, obs.heightTop);
                
                // Bottom Hazard Block (visual gap filler)
                ctx.fillRect(obs.x, bottomY + Math.min(5, 30 - obs.heightBottom), blockWidth, Math.min(5, 30 - obs.heightBottom));

            }
        }

        // --- Main Game Loop and Update Cycle ---

        let lastTime = performance.now();
        function gameUpdate(currentTime) {
            if (isGameOver) return;

            const deltaTime = currentTime - lastTime;
            lastTime = currentTime;

            // 1. Clear Canvas & Draw Background
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawBackground();

            // 2. Update Game State (Physics and Movement)
            updatePlayer(deltaTime);
            spawnObstacle(currentTime);
            updateObstacles(deltaTime);
            checkCollision();

            // 3. Draw Entities
            drawObstacles();
            drawPlayer();

            // 4. Score and Speed Progression
            scoreTimer += (deltaTime / 1000); // Time in seconds
            
            // Increase score based on time survived
            if (Math.floor(scoreTimer) > Math.floor((score - 100) / 10)) { // Smoother scoring increase
                 score = Math.floor(scoreTimer * 2);
                 updateScoreDisplay();
            }

            // Increase speed slightly over time
            gameSpeed = Math.min(15, 6 + (Math.floor(scoreTimer) / 10));
            if (gameSpeed > 6 && deltaTime > 0) {
                // Force a redraw/repaint on speed change for visual feedback if needed
            }

            requestAnimationFrame(gameUpdate);
        }

        function updateScoreDisplay() {
             scoreDisplay.textContent = `Score: ${Math.floor(score)}`;
        }


        // --- Event Listeners ---

        window.addEventListener('keydown', (e) => {
            if (isGameOver && e.key !== 'Enter') return; // Only allow input if game is running or on retry button press
            if ((e.code === 'Space' || e.key === 'ArrowUp') && !isGameOver) {
                jump();
            }
        });

        canvas.addEventListener('click', () => {
             if (isGameOver && gameOverScreen.style.display !== 'flex') return; // Ignore clicks if game over screen is showing but button hasn't been pressed
             if (!isGameOver) {
                 jump();
             }
        });
        
        // Handle the retry button click
        retryButton.addEventListener('click', () => {
            resetGame();
        });

        // --- Initialization ---
        function initialize() {
            initAudio();
            highScoreDisplay.textContent = `High Score: ${Math.floor(highScore)}`;
            
            // Set initial state and wait for the first user action to start audio context
            console.log("Welcome! Press Space or Click/Tap to Jump.");

            // Display instructions until first play
            gameOverScreen.querySelector('h2').textContent = "ollama's Adventure";
            gameOverScreen.querySelector('#finalScoreText').innerHTML = `Highest Score: ${Math.floor(highScore)}<br>Click START or Press Spacebar!`;
            retryButton.textContent = "START GAME";
            retryButton.onclick = () => {
                if (audioContext && audioContext.state === 'suspended') {
                    audioContext.resume(); // Crucial for browser autoplay policy
                }
                resetGame();
            };
            gameOverScreen.style.display = 'flex';

        }

        window.onload = initialize;

    </script>
</body>
</html>
```

139 t/s, 4705 tokens, 34s
