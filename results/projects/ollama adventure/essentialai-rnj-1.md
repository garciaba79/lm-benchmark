# Rnj 1
Model: essentialai/rnj-1
Test: ollamas adventure
Created: 11/03/2026, 12:44:44 AM
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

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>ollama's Adventure</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background-color: #87CEEB; /* Sky blue */
      font-family: Arial, sans-serif;
    }

    canvas {
      display: block;
      width: 100vw;
      height: 100vh;
    }

    .ui {
      position: absolute;
      top: 20px;
      left: 20px;
      color: white;
      font-size: 24px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    button {
      display: block;
      margin: 20px auto;
      padding: 10px 20px;
      font-size: 18px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas"></canvas>
  <div class="ui">
    Score: <span id="score">0</span><br/>
    High Score: <span id="highScore">0</span>
  </div>
  <button id="retryButton" style="display:none;">Play Again</button>

  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // Resize canvas to fit the window
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Game constants
    const GRAVITY = 0.5;
    const JUMP_FORCE = -10;
    const OBSTACLE_SPEED = 3;
    const ALPACA_WIDTH = 50;
    const ALPACA_HEIGHT = 50;

    // Game state
    let alpacaX, alpacaY, alpacaVelocityY;
    let obstacles = [];
    let score = 0;
    let highScore = parseInt(localStorage.getItem('ollamaHighScore')) || 0;
    let gameSpeed = 1;
    let isGameOver = false;

    // Audio context for sound effects
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSound(frequency, duration) {
      const oscillator = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
      gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
      oscillator.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      oscillator.start();
      setTimeout(() => {
        oscillator.stop();
      }, duration);
    }

    function drawAlpaca() {
      ctx.fillStyle = '#FFD700'; // Gold color for alpaca
      ctx.fillRect(alpacaX, alpacaY, ALPACA_WIDTH, ALPACA_HEIGHT);

      // Simple eyes and legs
      ctx.fillStyle = 'black';
      ctx.beginPath();
      ctx.arc(alpacaX + 15, alpacaY + 20, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(alpacaX + 35, alpacaY + 20, 5, 0, Math.PI * 2);
      ctx.fill();

      // Legs
      ctx.fillRect(alpacaX + 10, alpacaY + ALPACA_HEIGHT - 10, 30, 10);
    }

    function drawObstacles() {
      obstacles.forEach(obstacle => {
        ctx.fillStyle = '#8B0000'; // Dark red for obstacles
        ctx.fillRect(obstacle.x, obstacle.y, 20, 50);
      });
    }

    function updateAlpaca() {
      alpacaY += alpacaVelocityY;
      alpacaVelocityY += GRAVITY;

      // Keep alpaca within canvas bounds
      if (alpacaY + ALPACA_HEIGHT > canvas.height) {
        alpacaY = canvas.height - ALPACA_HEIGHT;
        alpacaVelocityY = 0;
      }
    }

    function updateObstacles() {
      obstacles.forEach((obstacle, index) => {
        obstacle.x -= OBSTACLE_SPEED * gameSpeed;

        // Remove off-screen obstacles
        if (obstacle.x + 20 < 0) {
          obstacles.splice(index, 1);
        }
      });

      // Add new obstacles randomly
      if (Math.random() < 0.02 * gameSpeed) {
        obstacles.push({
          x: canvas.width,
          y: Math.random() * (canvas.height - 50)
        });
      }
    }

    function checkCollisions() {
      obstacles.forEach(obstacle => {
        if (
          alpacaX < obstacle.x + 20 &&
          alpacaX + ALPACA_WIDTH > obstacle.x &&
          alpacaY < obstacle.y + 50 &&
          alpacaY + ALPACA_HEIGHT > obstacle.y
        ) {
          isGameOver = true;
          playSound(100, 200); // Hit sound effect
        }
      });
    }

    function updateScore() {
      score += Math.floor(gameSpeed);
      document.getElementById('score').textContent = score;

      if (score > highScore) {
        highScore = score;
        localStorage.setItem('ollamaHighScore', highScore);
        document.getElementById('highScore').textContent = highScore;
      }
    }

    function increaseDifficulty() {
      gameSpeed += 0.001;
    }

    function drawBackground() {
      // Parallax scrolling background
      const bg1Y = (Date.now() * 0.002) % canvas.height;
      const bg2Y = (Date.now() * 0.001) % canvas.height;

      ctx.fillStyle = '#87CEEB'; // Sky blue
      ctx.fillRect(0, bg1Y - canvas.height, canvas.width, canvas.height);
      ctx.fillRect(0, bg2Y - canvas.height, canvas.width, canvas.height);

      ctx.fillStyle = '#FFA500'; // Orange for hills
      ctx.fillRect(0, bg1Y, canvas.width * 0.5, canvas.height * 0.3);
      ctx.fillRect(0, bg2Y, canvas.width * 0.7, canvas.height * 0.4);

      ctx.fillStyle = '#228B22'; // Forest green for trees
      ctx.fillRect(canvas.width * 0.8, bg1Y + canvas.height * 0.2, canvas.width * 0.2, canvas.height * 0.3);
    }

    function gameLoop() {
      if (!isGameOver) {
        drawBackground();
        updateAlpaca();
        updateObstacles();
        checkCollisions();
        updateScore();
        increaseDifficulty();

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        drawAlpaca();
        drawObstacles();
      } else {
        document.getElementById('retryButton').style.display = 'block';
      }

      requestAnimationFrame(gameLoop);
    }

    function initGame() {
      alpacaX = 50;
      alpacaY = canvas.height / 2 - ALPACA_HEIGHT / 2;
      alpacaVelocityY = 0;

      obstacles = [];
      score = 0;
      gameSpeed = 1;
      isGameOver = false;

      document.getElementById('retryButton').style.display = 'none';
    }

    function jump() {
      if (!isGameOver) {
        playSound(220, 100); // Jump sound effect
        alpacaVelocityY = JUMP_FORCE;
      }
    }

    // Event listeners
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') jump();
    });

    canvas.addEventListener('click', () => {
      if (!isGameOver) jump();
    });

    document.getElementById('retryButton').addEventListener('click', initGame);

    // Initialize game
    initGame();

    // Start game loop
    gameLoop();
  </script>
</body>
</html>
```

123 t/s, 1749 tokens, 14s
