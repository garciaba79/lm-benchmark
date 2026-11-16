# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: ollamas adventure
Created: 11/15/2026, 09:42:28 PM
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

This is a complete, self-contained, playable endless runner game called "Ollama's Adventure" implemented entirely within a single HTML file using pure JavaScript, Canvas for rendering, CSS for styling, and the Web Audio API for sound effects.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama's Adventure</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f8ff; /* Light sky background */
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }

        #gameContainer {
            border: 4px solid #333;
            box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.5);
            background-color: #ffffff;
            position: relative;
        }

        canvas {
            display: block;
            width: 800px; /* Game width */
            height: 400px; /* Game height */
            background-color: #a2d2ff; /* Canvas background color */
        }

        #overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            text-align: center;
            z-index: 10;
        }

        #overlay h1 {
            margin-bottom: 15px;
            color: #ff69b4; /* Pink/fun color */
        }

        #scoreDisplay, #highScoreDisplay {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 20px;
            color: #333;
            font-weight: bold;
            z-index: 20;
        }

        #gameOverScreen {
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.85);
            z-index: 30;
            justify-content: center;
            align-items: center;
        }

        #gameOverScreen button {
            padding: 15px 30px;
            font-size: 24px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            margin-top: 20px;
            transition: background-color 0.3s;
        }

        #gameOverScreen button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <canvas id="gameCanvas"></canvas>
        <div id="scoreDisplay">Score: 0</div>
        <div id="highScoreDisplay">High Score: 0</div>

        <!-- Game Over Overlay -->
        <div id="gameOverScreen">
            <h1>Game Over!</h1>
            <p id="finalScoreText">Your Score: 0</p>
            <button id="retryButton">Play Again</button>
        </div>
    </div>

    <script>
        // --- Web Audio API Setup for Sound Effects ---
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        function playSound(frequency, duration, type = 'sine', volume = 0.5) {
            if (!audioContext) return;
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.type = type;
            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);

            gainNode.gain.setValueAtTime(volume, audioContext.currentTime);
            gainNode.gain.exponentialRampToValue(0.001, audioContext.currentTime + duration / 1000);

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            oscillator.start();
            oscillator.stop(audioContext.currentTime + duration / 1000);
        }

        function playJumpSound() {
            // A short, rising sound for the jump (higher frequency)
            playSound(880, 100, 'square', 0.3);
        }

        function playScoreSound() {
            // A cheerful chime for scoring
            playSound(440, 50, 'triangle', 0.5);
        }

        function playHitSound() {
            // A lower, jarring sound for hitting an obstacle
            playSound(120, 300, 'sawtooth', 0.6);
        }


        // --- Game Setup Variables ---
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const scoreDisplay = document.getElementById('scoreDisplay');
        const highScoreDisplay = document.getElementById('highScoreDisplay');
        const gameOverScreen = document.getElementById('gameOverScreen');
        const retryButton = document.getElementById('retryButton');
        const finalScoreText = document.getElementById('finalScoreText');

        let gameLoopId;
        let isGameOver = true;
        let score = 0;
        let highScore = localStorage.getItem('ollamasHighScore') ? parseInt(localStorage.getItem('ollamasHighScore')) : 0;
        let animationFrameId;

        // Player (Alpaca) properties
        const alpaca = {
            x: 50,
            y: 0, // Will be set dynamically based on ground level
            width: 40,
            height: 60,
            velocityY: 0,
            gravity: 0.8,
            isJumping: false,
            color: '#ffaa55' // Cartoon Alpaca color
        };

        // Ground and Scrolling Properties
        const groundHeight = canvas.height - 50;
        let gameSpeed = 4; // Base speed of obstacles/scrolling
        let obstacleSpawnRate = 150; // How often to check for new obstacles (lower is faster)
        let lastObstacleTime = 0;

        // Parallax Background Setup
        const backgroundLayers = [
            { color: '#87CEEB', speedFactor: 0.3, scrollOffset: 0 }, // Sky/Distant clouds (slowest)
            { color: '#ADD8E6', speedFactor: 0.7, scrollOffset: 0 }  // Mid-ground hills (faster)
        ];

        // Obstacle Array
        let obstacles = [];

        // --- Initialization Functions ---

        function loadHighScore() {
            highScore = localStorage.getItem('ollamasHighScore') ? parseInt(localStorage.getItem('ollamasHighScore')) : 0;
            highScoreDisplay.textContent = `High Score: ${highScore}`;
        }

        function resetGame() {
            // Reset state
            score = 0;
            gameSpeed = 4;
            obstacleSpawnRate = 150;
            obstacles = [];
            alpaca.velocityY = 0;
            alpaca.isJumping = false;
            
            // Reset physics reference
            alpaca.y = groundHeight - alpaca.height; // Position on the ground

            // Update UI
            scoreDisplay.textContent = `Score: 0`;
            
            // Clear existing obstacles from screen
            obstacles.forEach(obs => obs.x = canvas.width + 50);

            gameOverScreen.style.display = 'none';
            isGameOver = false;

            // Start the loop
            if (gameLoopId) cancelAnimationFrame(gameLoopId);
            lastObstacleTime = performance.now();
            
            requestAnimationFrame(gameLoop);
        }

        function startGame() {
            loadHighScore(); // Ensure high score is loaded on start
            resetGame();
        }


        // --- Drawing Functions ---

        function drawAlpaca() {
            ctx.fillStyle = alpaca.color;
            
            // Draw simple cartoon body shape (a slightly rounded rectangle/oval)
            ctx.beginPath();
            ctx.arc(alpaca.x + alpaca.width / 2, alpaca.y + alpaca.height / 2, alpaca.width / 2, 0, Math.PI * 2);
            ctx.fill();

            // Simple face details
            ctx.fillStyle = 'black';
            ctx.beginPath();
            ctx.arc(alpaca.x + 10, alpaca.y + 15, 5, 0, Math.PI * 2); // Eye
            ctx.arc(alpaca.x + 30, alpaca.y + 15, 5, 0, Math.PI * 2); // Other eye
            ctx.fill();

            // Simple legs/body outline (for visual grounding)
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.strokeRect(alpaca.x, alpaca.y + alpaca.height - 10, alpaca.width, 10); // Feet area
        }

        function drawBackground() {
            // Draw Parallax Layers
            const w = canvas.width;
            
            backgroundLayers.forEach(layer => {
                // Calculate offset based on camera movement (gameSpeed) and layer speed factor
                const scroll = (score * layer.speedFactor) % w; 

                ctx.fillStyle = layer.color;
                
                // Layer 1: Distant background (moves slower relative to the ground)
                ctx.fillRect(scroll, 0, w, canvas.height);

                // Layer 2: Closer elements/details (if needed, kept simple here)
            });

            // Draw Ground
            ctx.fillStyle = '#4CAF50'; // Green grass
            ctx.fillRect(0, groundHeight, w, canvas.height - groundHeight);
        }


        function drawObstacles() {
            obstacles.forEach(obs => {
                ctx.fillStyle = obs.color;
                ctx.fillRect(obs.x, groundHeight - obs.height, obs.width, obs.height);
            });
        }

        // --- Game Logic Functions ---

        function updateScore() {
            score += 1; // Score increases based on time/distance passed
            scoreDisplay.textContent = `Score: ${Math.floor(score / 10)}`; // Display score every 10 units for readability
        }

        function spawnObstacle() {
            if (performance.now() - lastObstacleTime > obstacleSpawnRate) {
                const minHeight = 30;
                const maxHeight = 80;
                const obsHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
                const obsWidth = Math.floor(Math.random() * 20) + 20; // Obstacle width variation

                obstacles.push({
                    x: canvas.width,
                    y: groundHeight - obsHeight,
                    width: obsWidth,
                    height: obsHeight,
                    color: `hsl(${Math.random() * 360}, 70%, 50%)` // Random colorful obstacles
                });
                lastObstacleTime = performance.now();
            }
        }

        function updateObstacles() {
            const currentSpeed = gameSpeed;

            obstacles.forEach(obs => {
                // Move obstacle to the left based on game speed
                obs.x -= currentSpeed;
            });

            // Remove obstacles that have passed the screen
            obstacles = obstacles.filter(obs => obs.x + obs.width > 0);
        }

        function checkCollisions() {
            const alpacaBottom = alpaca.y + alpaca.height;
            const alpacaTop = alpaca.y;
            const alpacaLeft = alpaca.x;
            const alpacaRight = alpaca.x + alpaca.width;
            const alpacaBottomGround = groundHeight;

            for (const obs of obstacles) {
                // Simple AABB collision detection
                if (alpacaRight > obs.x && alpacaLeft < obs.x + obs.width && 
                    alpacaBottomGround > obs.y && alpacaTop < obs.y + obs.height) {
                    
                    // Collision detected!
                    if (!isGameOver) {
                        playHitSound();
                        endGame();
                        return; // Stop further checks if collision happens
                    }
                }
            }
        }

        function updatePhysics() {
            // 1. Apply gravity
            alpaca.velocityY += alpaca.gravity;
            alpaca.y += alpaca.velocityY;

            // 2. Check Ground Collision (Landing)
            if (alpaca.y + alpaca.height > groundHeight) {
                alpaca.y = groundHeight - alpaca.height; // Snap to ground
                alpaca.velocityY = 0;
                alpaca.isJumping = false;
            }
        }

        // --- Main Game Loop ---
        function gameLoop(currentTime) {
            if (isGameOver) return;

            // 1. Clear Canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 2. Update Background Parallax Scroll (Simulated by score movement)
            // We use the current score progression to drive background movement visually
            const parallaxOffset = score * 0.5; 
            backgroundLayers[0].scrollOffset = parallaxOffset;
            backgroundLayers[1].scrollOffset = parallaxOffset * 2;


            // 3. Update Game State
            updatePhysics();

            // 4. Handle Obstacles
            spawnObstacle();
            updateObstacles();

            // 5. Check for Collision
            checkCollisions();
            if (isGameOver) return; // If collision just happened, stop processing physics for this frame

            // 6. Draw Everything
            drawBackground();
            drawObstacles();
            drawAlpaca();

            // 7. Update Score
            updateScore();


            // Request next frame
            gameLoopId = requestAnimationFrame(gameLoop);
        }

        function endGame() {
            isGameOver = true;
            cancelAnimationFrame(gameLoopId);
            
            // Save High Score
            if (score > highScore) {
                highScore = Math.floor(score);
                localStorage.setItem('ollamasHighScore', highScore);
            }

            finalScoreText.textContent = `Your Score: ${Math.floor(score)}`;
            gameOverScreen.style.display = 'flex';
        }


        // --- Event Listeners ---

        // Keyboard Control (Spacebar)
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !isGameOver) {
                e.preventDefault(); // Prevent scrolling
                if (!alpaca.isJumping) {
                    alpaca.velocityY = -15; // Initial jump velocity
                    alpaca.isJumping = true;
                    playJumpSound();
                }
            } else if (e.code === 'Space' && isGameOver) {
                // Retry functionality
                resetGame();
            }
        });

        // Mouse/Touch Control (Click/Tap to Jump)
        canvas.addEventListener('click', () => {
            if (!isGameOver) {
                if (!alpaca.isJumping) {
                    alpaca.velocityY = -15;
                    alpaca.isJumping = true;
                    playJumpSound();
                }
            } else {
                 // If game is over, clicking can retry
                 resetGame();
            }
        });

        // --- Start Game ---
        window.onload = () => {
            // Set initial alpaca position before starting loop
            alpaca.y = groundHeight - alpaca.height; 
            
            startGame(); // Initialize the game state and start the loop immediately
        };

    </script>
</body>
</html>
```

194 t/s, 3836 tokens, 20s
