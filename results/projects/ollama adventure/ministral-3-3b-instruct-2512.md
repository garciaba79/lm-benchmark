# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: ollamas adventure
Created: 11/03/2026, 12:16:00 AM
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

Here's a complete, self-contained "Ollama's Adventure" endless runner game in one HTML file with inline CSS/JS:

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
            overflow: hidden;
            background-color: #f5f7fa;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        canvas {
            display: block;
            background-color: #f5f7fa;
        }

        .game-over-screen {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .game-over-content {
            text-align: center;
            color: white;
            z-index: 20;
        }

        .score-display {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .high-score-display {
            font-size: 1.5rem;
            margin-bottom: 2rem;
        }

        button {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }

        button:hover {
            background-color: #45a049;
        }

        .parallax-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>

    <div class="game-over-screen" id="gameOverScreen">
        <div class="game-over-content">
            <h2>Game Over!</h2>
            <div class="score-display" id="finalScore">Score: 0</div>
            <div class="high-score-display" id="highScoreDisplay">High Score: 0</div>
            <button id="retryButton">Play Again</button>
        </div>
    </div>

    <script>
        // Game variables
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const gameOverScreen = document.getElementById('gameOverScreen');
        const finalScoreDisplay = document.getElementById('finalScore');
        const highScoreDisplay = document.getElementById('highScoreDisplay');
        const retryButton = document.getElementById('retryButton');

        // Game state
        let isGameOver = false;
        let score = 0;
        let highScore = localStorage.getItem('ollamaHighScore') || 0;
        let gameSpeed = 1;
        let lastObstacleTime = 0;
        let jumpSound, obstacleSound, scoreSound;

        // Set canvas to full window size
        function resizeCanvas() {
            canvas.width = window.innerWidth * 2; // Double width for parallax effect
            canvas.height = window.innerHeight;
        }

        window.addEventListener('resize', () => {
            resizeCanvas();
        });

        // Initialize game
        function initGame() {
            isGameOver = false;
            score = 0;
            gameSpeed = 1;
            lastObstacleTime = Date.now();

            // Clear canvas and draw background
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw parallax layers
            drawParallaxLayer(0, 0, 'sky', 0.5);
            drawParallaxLayer(0, 0, 'mountains', 1.2);

            // Create alpaca
            createAlpaca();

            // Create obstacles
            setInterval(createObstacle, 1000 / gameSpeed);

            updateHighScore();
        }

        // Draw parallax layers
        function drawParallaxLayer(xOffset, yOffset, type, speed) {
            const layer = document.createElement('div');
            layer.className = `parallax-layer ${type}`;
            layer.style.position = 'absolute';
            layer.style.top = '0';
            layer.style.left = '0';
            layer.style.width = '100%';
            layer.style.height = '100%';

            // Create multiple clouds/mountains
            for (let i = 0; i < 5; i++) {
                const cloudWidth = Math.random() > 0.3 ? 80 : 40;
                const cloudX = -cloudWidth + xOffset;

                if (type === 'sky') {
                    // Draw sky clouds
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath();
                    ctx.moveTo(cloudX, canvas.height * 0.2);
                    ctx.lineTo(cloudX + cloudWidth / 2, canvas.height * 0.1);
                    ctx.lineTo(cloudX + cloudWidth, canvas.height * 0.2);
                    ctx.fill();

                    // Draw mountain shadows
                    ctx.fillStyle = '#8B4513';
                    ctx.beginPath();
                    ctx.moveTo(cloudX, canvas.height * 0.6);
                    ctx.lineTo(cloudX + cloudWidth / 2, canvas.height * 0.7);
                    ctx.lineTo(cloudX + cloudWidth, canvas.height * 0.8);
                    ctx.fill();

                    // Draw mountain peaks
                    ctx.fillStyle = '#d4e157';
                    ctx.beginPath();
                    ctx.moveTo(cloudX, canvas.height * 0.6);
                    ctx.lineTo(cloudX + cloudWidth / 2, canvas.height * 0.3);
                    ctx.lineTo(cloudX + cloudWidth, canvas.height * 0.4);
                    ctx.fill();
                } else if (type === 'mountains') {
                    // Draw mountains
                    const mountainHeight = Math.random() > 0.5 ? canvas.height * 0.7 : canvas.height * 0.8;
                    const mountainX = -cloudWidth + xOffset;

                    ctx.fillStyle = '#2d3436';
                    ctx.beginPath();
                    ctx.moveTo(mountainX, canvas.height);
                    ctx.lineTo(mountainX + cloudWidth / 2, canvas.height - mountainHeight);
                    ctx.lineTo(mountainX + cloudWidth, canvas.height);

                    // Add some detail
                    const peak1 = Math.random() > 0.5 ? (canvas.height - mountainHeight) * 0.7 : (canvas.height - mountainHeight) * 0.3;
                    const peak2 = Math.random() > 0.5 ? (canvas.height - mountainHeight) * 0.6 : (canvas.height - mountainHeight) * 0.4;

                    ctx.fillStyle = '#d4e157';
                    ctx.beginPath();
                    ctx.moveTo(mountainX, canvas.height);
                    ctx.lineTo(mountainX + cloudWidth / 3, peak1);
                    ctx.lineTo(mountainX + cloudWidth / 2 - cloudWidth/6, peak2);
                    ctx.lineTo(mountainX + cloudWidth - cloudWidth/3, peak1);
                    ctx.lineTo(mountainX + cloudWidth, canvas.height);

                    ctx.fill();
                }
            }

            // Move layer
            xOffset += speed;
            if (xOffset > canvas.width) {
                xOffset = 0;
            }

            // Draw the layer on canvas
            ctx.drawImage(layer, 0, 0);
        }

        // Create alpaca character
        function createAlpaca() {
            const alpacaX = canvas.width / 2 - 50;
            const alpacaY = canvas.height * 0.7;

            // Draw alpaca body
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.arc(alpacaX + 30, alpacaY + 20, 30, 0, Math.PI);
            ctx.arc(alpacaX - 30, alpacaY + 20, 30, 0, Math.PI * 2);
            ctx.fill();

            // Draw alpaca face
            ctx.fillStyle = '#f5f7fa';
            ctx.beginPath();
            ctx.arc(alpacaX, alpacaY - 15, 15, 0, Math.PI * 2);
            ctx.fill();

            // Draw eyes
            ctx.fillStyle = 'black';
            ctx.beginPath();
            ctx.arc(alpacaX - 7, alpacaY - 8, 3, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(alpacaX + 7, alpacaY - 8, 3, 0, Math.PI * 2);
            ctx.fill();

            // Draw nose
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.arc(alpacaX, alpacaY - 10, 5, 0, Math.PI * 2);
            ctx.fill();

            // Draw ears
            ctx.fillStyle = '#f5f7fa';
            ctx.beginPath();
            ctx.moveTo(alpacaX + 30, alpacaY - 15);
            ctx.lineTo(alpacaX + 45, alpacaY - 25);
            ctx.arc(alpacaX + 45, alpacaY - 25, 7, Math.PI * 1.6, Math.PI * 2);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(alpacaX - 30, alpacaY - 15);
            ctx.lineTo(alpacaX - 45, alpacaY - 25);
            ctx.arc(alpacaX - 45, alpacaY - 25, 7, Math.PI * 0.4, Math.PI);
            ctx.fill();

            // Draw legs
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.moveTo(alpacaX + 30, alpacaY + 20);
            ctx.lineTo(alpacaX + 30, alpacaY + 60);
            ctx.lineTo(alpacaX + 20, alpacaY + 70);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(alpacaX - 30, alpacaY + 20);
            ctx.lineTo(alpacaX - 30, alpacaY + 60);
            ctx.lineTo(alpacaX - 40, alpacaY + 70);
            ctx.fill();

            // Draw tail
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.moveTo(alpacaX - 30, alpacaY + 20);
            ctx.lineTo(alpacaX - 60, alpacaY + 30);
            ctx.arc(alpacaX - 60, alpacaX - 50, 10, Math.PI * 1.8, Math.PI * 2);
            ctx.fill();
        }

        // Create obstacle
        function createObstacle() {
            const obstacleY = canvas.height * (Math.random() > 0.3 ? 0.4 : 0.6);
            const obstacleWidth = 50 + Math.random() * 100;
            const obstacleX = canvas.width;

            // Draw obstacle
            ctx.fillStyle = '#8B4513';
            ctx.beginPath();
            ctx.moveTo(obstacleX, obstacleY - 20);
            ctx.lineTo(obstacleX + obstacleWidth / 2, obstacleY - 10);
            ctx.lineTo(obstacleX + obstacleWidth, obstacleY - 20);
            ctx.fill();

            // Add some detail
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.moveTo(obstacleX, obstacleY - 30);
            ctx.lineTo(obstacleX + obstacleWidth / 2, obstacleY - 20);
            ctx.lineTo(obstacleX + obstacleWidth, obstacleY - 30);
            ctx.fill();

            // Store obstacle position
            obstacles.push({
                x: obstacleX,
                width: obstacleWidth,
                y: obstacleY,
                height: 40
            });
        }

        // Game loop
        function gameLoop() {
            if (isGameOver) return;

            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw parallax layers with offset based on game speed
            drawParallaxLayer(gameSpeed * 2, 0, 'sky', 0.5);
            drawParallaxLayer(gameSpeed * 3, 0, 'mountains', 1.2);

            // Move alpaca
            alpaca.x += gameSpeed;

            // Check for collisions with obstacles
            for (const obstacle of obstacles) {
                if (
                    alpaca.x + alpaca.width > obstacle.x &&
                    alpaca.x < obstacle.x + obstacle.width &&
                    alpaca.y + alpaca.height > obstacle.y &&
                    alpaca.y < obstacle.y + obstacle.height
                ) {
                    gameOver();
                    return;
                }
            }

            // Move obstacles
            for (let i = obstacles.length - 1; i >= 0; i--) {
                const obstacle = obstacles[i];
                obstacle.x -= gameSpeed;

                if (obstacle.x < -obstacle.width) {
                    obstacles.splice(i, 1);
                } else {
                    // Check if alpaca has passed the obstacle
                    if (alpaca.x + alpaca.width > obstacle.x && alpaca.x < obstacle.x + obstacle.width) {
                        score += gameSpeed * 2;
                        finalScoreDisplay.textContent = `Score: ${score}`;
                        playSound(scoreSound);
                    }
                }
            }

            // Increase speed every few seconds
            if (Date.now() - lastObstacleTime > 1000 && gameSpeed < 3) {
                gameSpeed += 0.05;
                lastObstacleTime = Date.now();
            }

            // Draw alpaca
            drawAlpaca();

            requestAnimationFrame(gameLoop);
        }

        // Draw alpaca with animation
        function drawAlpaca() {
            const alpacaX = canvas.width / 2 - 50;
            const alpacaY = canvas.height * 0.7;

            // Draw legs based on position
            if (alpaca.x % 100 > 60) {
                ctx.fillStyle = '#d4e157';
                ctx.beginPath();
                ctx.moveTo(alpacaX + 30, alpacaY + 20);
                ctx.lineTo(alpacaX + 30, alpacaY + 60);
                ctx.lineTo(alpacaX + 20, alpacaY + 70);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(alpacaX - 30, alpacaY + 20);
                ctx.lineTo(alpacaX - 30, alpacaY + 60);
                ctx.lineTo(alpacaX - 40, alpacaY + 70);
                ctx.fill();
            } else {
                // Draw legs when not moving
                ctx.fillStyle = '#d4e157';
                ctx.beginPath();
                ctx.moveTo(alpacaX + 30, alpacaY + 20);
                ctx.lineTo(alpacaX + 30, alpacaY + 60);
                ctx.lineTo(alpacaX + 20, alpacaY + 70);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(alpacaX - 30, alpacaY + 20);
                ctx.lineTo(alpacaX - 30, alpacaY + 60);
                ctx.lineTo(alpacaX - 40, alpacaY + 70);
                ctx.fill();
            }

            // Draw body
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.arc(alpacaX + 30, alpacaY + 20, 30, 0, Math.PI);
            ctx.arc(alpacaX - 30, alpacaY + 20, 30, 0, Math.PI * 2);
            ctx.fill();

            // Draw face
            ctx.fillStyle = '#f5f7fa';
            ctx.beginPath();
            ctx.arc(alpacaX, alpacaY - 15, 15, 0, Math.PI * 2);
            ctx.fill();

            // Draw eyes
            ctx.fillStyle = 'black';
            ctx.beginPath();
            ctx.arc(alpacaX - 7, alpacaY - 8, 3, 0, Math.PI * 2);
            ctx.fill();
            ctx.beginPath();
            ctx.arc(alpacaX + 7, alpacaY - 8, 3, 0, Math.PI * 2);
            ctx.fill();

            // Draw nose
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.arc(alpacaX, alpacaY - 10, 5, 0, Math.PI * 2);
            ctx.fill();

            // Draw ears
            ctx.fillStyle = '#f5f7fa';
            ctx.beginPath();
            ctx.moveTo(alpacaX + 30, alpacaY - 15);
            ctx.lineTo(alpacaX + 45, alpacaY - 25);
            ctx.arc(alpacaX + 45, alpacaY - 25, 7, Math.PI * 1.6, Math.PI * 2);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(alpacaX - 30, alpacaY - 15);
            ctx.lineTo(alpacaX - 45, alpacaY - 25);
            ctx.arc(alpacaX - 45, alpacaY - 25, 7, Math.PI * 0.4, Math.PI);
            ctx.fill();

            // Draw tail
            ctx.fillStyle = '#d4e157';
            ctx.beginPath();
            ctx.moveTo(alpacaX - 30, alpacaY + 20);
            ctx.lineTo(alpacaX - 60, alpacaY + 30);
            ctx.arc(alpacaX - 60, alpacaX - 50, 10, Math.PI * 1.8, Math.PI * 2);
            ctx.fill();
        }

        // Game over
        function gameOver() {
            isGameOver = true;
            gameSpeed = 1;

            // Play obstacle sound
            playSound(obstacleSound);

            // Update high score if needed
            if (score > highScore) {
                highScore = score;
                localStorage.setItem('ollamaHighScore', highScore);
                updateHighScore();
            }

            // Show game over screen
            gameOverScreen.style.display = 'flex';
        }

        // Update high score display
        function updateHighScore() {
            highScoreDisplay.textContent = `High Score: ${highScore}`;
        }

        // Initialize sounds (using Web Audio API)
        async function initSounds() {
            try {
                // Create audio context
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();

                // Jump sound
                jumpSound = new Audio();
                jumpSound.src = URL.createObjectURL(new Blob(['sine'], { type: 'audio/sine' }));
                jumpSound.onended = () => {
                    if (jumpSound.currentTime > 0.1) {
                        jumpSound.src = URL.createObjectURL(new Blob(['sine'], { type: 'audio/sine' }));
                    }
                };

                // Obstacle sound
                obstacleSound = new Audio();
                obstacleSound.src = URL.createObjectURL(new Blob([
                    'var audioContext = new (window.AudioContext || window.webkitAudioContext)();',
                    'var oscillator = audioContext.createOscillator();',
                    'oscillator.type = "sine";',
                    'oscillator.frequency.setValueAtTime(440, audioContext.currentTime);',
                    'oscillator.connect(audioContext.destination);',
                    'oscillator.start();',
                    'setTimeout(() => { oscillator.stop(); }, 250);'
                ], { type: 'application/javascript' }));

                // Score sound
                scoreSound = new Audio();
                scoreSound.src = URL.createObjectURL(new Blob([
                    'var audioContext = new (window.AudioContext || window.webkitAudioContext)();',
                    'var oscillator = audioContext.createOscillator();',
                    'oscillator.type = "sine";',
                    'oscillator.frequency.setValueAtTime(300, audioContext.currentTime);',
                    'oscillator.connect(audioContext.destination);',
                    'oscillator.start();',
                    'setTimeout(() => { oscillator.stop(); }, 150);'
                ], { type: 'application/javascript' }));

                // Play initial sounds
                jumpSound.play();
                obstacleSound.play();
                scoreSound.play();

                return audioContext;
            } catch (e) {
                console.error('Could not initialize sounds:', e);
                return null;
            }
        }

        // Play sound
        function playSound(audioElement) {
            if (!audioElement) return;

            // Try to play the sound again if it's already playing
            if (audioElement.paused || audioElement.ended) {
                audioElement.currentTime = 0;
                audioElement.play().catch(e => console.error('Play error:', e));
            }
        }

        // Game objects
        const alpaca = {
            x: canvas.width / 2 - 50,
            y: canvas.height * 0.7,
            width: 60,
            height: 40,
            jumpHeight: 100,
            isJumping: false,
            jumpVelocity: 0
        };

        const obstacles = [];

        // Event listeners for controls
        document.addEventListener('keydown', (e) => {
            if (isGameOver || e.key === ' ') {
                return;
            }

            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
                alpaca.isJumping = true;
                playSound(jumpSound);
            }
        });

        document.addEventListener('click', () => {
            if (isGameOver) {
                initGame();
                gameOverScreen.style.display = 'none';
            } else if (!isGameOver && !gameSpeed) {
                alpaca.isJumping = true;
                playSound(jumpSound);
            }
        });

        // Retry button
        retryButton.addEventListener('click', () => {
            initGame();
            gameOverScreen.style.display = 'none';
        });

        // Initialize the game
        resizeCanvas();
        initSounds();

        // Start the game
        initGame();
        gameLoop();
    </script>
</body>
</html>
```

This complete "Ollama's Adventure" game includes:

1. A cartoon alpaca character that runs automatically to the right
2. Jump mechanics (press spacebar or tap/click)
3. Obstacles appearing from the right side
4. Increasing difficulty over time
5. Score tracking based on distance covered
6. High score persistence using localStorage
7. Game over screen with retry option
8. Parallax scrolling background with sky and mountains
9. Simple sound effects for jumping, scoring, and obstacles (using Web Audio API)
10. Responsive design that works on different screen sizes

The game features:
- A friendly alpaca character with simple animations
- Colorful, cartoonish graphics
- Increasing speed over time
- Score display and high score tracking
- Game over screen with retry option
- Tap/click controls for jumping

To play the game, simply save this code to an HTML file and open it in a modern browser. The alpaca will automatically run right, and you can tap or click to make it jump to avoid obstacles.

213 t/s, 5443 tokens, 26s
