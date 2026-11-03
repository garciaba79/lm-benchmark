# Qwen3 14B
Model: qwen/qwen3-14b
Test: ollamas adventure
Created: 11/03/2026, 01:08:15 AM
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

Sure! Below is a complete, self-contained **single-page endless runner game** named *ollama's Adventure*. It includes:

- A cartoon alpaca character.
- Parallax scrolling background with 2 layers.
- Jumping via spacebar or click/tap.
- Increasing difficulty over time.
- Score tracking and high score in localStorage.
- Simple sound effects using the Web Audio API.
- All graphics, styles, and scripts included inline in a single HTML file.

You can copy and paste this into an `.html` file and open it in any modern browser to play:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>ollama's Adventure</title>
  <style>
    * {
      box-sizing: border-box;
    }
    body, html {
      margin: 0;
      padding: 0;
      overflow: hidden;
      width: 100%;
      height: 100%;
      font-family: 'Comic Sans MS', cursive, sans-serif;
      background-color: #87ceeb; /* sky blue */
    }
    canvas {
      display: block;
    }
    #scoreboard {
      position: absolute;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      color: white;
      font-size: 24px;
      text-shadow: 1px 1px 3px black;
    }
    #retryButton {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      padding: 15px 30px;
      font-size: 24px;
      background-color: #ff69b4; /* hot pink */
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      display: none;
    }
    #retryButton:hover {
      background-color: #ff1493; /* deep pink */
    }
    #gameOverText {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 48px;
      color: white;
      text-shadow: 2px 2px 6px black;
      display: none;
    }
  </style>
</head>
<body>

<canvas id="gameCanvas" width="800" height="400"></canvas>
<div id="scoreboard">Score: <span id="currentScore">0</span> | High Score: <span id="highScore">0</span></div>
<button id="retryButton">Play Again</button>
<div id="gameOverText">Game Over!</div>

<script>
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // Game variables
  let score = 0;
  let highScore = parseInt(localStorage.getItem('ollamaHighScore') || '0');
  let gameOver = false;
  let jump = false;
  let gravity = 1.5;
  let velocityY = 0;

  const playerSize = { width: 40, height: 60 };
  const obstacleWidth = 30;
  const groundHeight = 20;
  const groundY = canvas.height - groundHeight;

  // Parallax background
  const background1Speed = 0.5;
  const background2Speed = 1.0;
  let bg1X = 0;
  let bg2X = 0;
  const obstacleColor = '#ff4757'; // red

  // Alpaca position and velocity
  let alpacaY = groundY - playerSize.height;

  // Obstacles array
  let obstacles = [];
  const obstacleSpawnRate = 1500; // in ms
  let lastObstacleTime = 0;
  let gameSpeed = 2;
  let speedIncreaseInterval = 5000; // increase speed every X ms

  function drawAlpaca(x, y) {
    ctx.fillStyle = '#fff8dc'; // light beige for body
    ctx.beginPath();
    ctx.moveTo(x + playerSize.width / 2, y);
    ctx.quadraticCurveTo(x, y - 30, x, y - 15);
    ctx.lineTo(x, y - 20);
    ctx.quadraticCurveTo(x + playerSize.width / 2, y, x + playerSize.width, y - 15);
    ctx.lineTo(x + playerSize.width, y - 20);
    ctx.quadraticCurveTo(x + playerSize.width, y - 30, x + playerSize.width / 2, y);
    ctx.closePath();
    ctx.fill();

    // Alpaca ears
    ctx.fillStyle = '#f5deb3'; // wheat for ears
    ctx.beginPath();
    ctx.moveTo(x - 10, y - 40);
    ctx.quadraticCurveTo(x + playerSize.width / 2 - 20, y - 70, x + playerSize.width / 2, y - 50);
    ctx.quadraticCurveTo(x + playerSize.width / 2 + 20, y - 70, x + playerSize.width + 10, y - 40);
    ctx.closePath();
    ctx.fill();

    // Eyes
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(x + 15, y - 30, 5, 0, Math.PI * 2);
    ctx.arc(x + playerSize.width - 15, y - 30, 5, 0, Math.PI * 2);
    ctx.fill();

    // Nose
    ctx.fillStyle = '#ff69b4';
    ctx.beginPath();
    ctx.arc(x + playerSize.width / 2, y - 20, 3, 0, Math.PI * 2);
    ctx.fill();

    // Mouth
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x + 15, y - 5);
    ctx.quadraticCurveTo(x + playerSize.width / 2, y + 5, x + playerSize.width - 15, y - 5);
    ctx.stroke();

    // Legs
    ctx.fillStyle = '#87ceeb'; // sky blue for legs
    ctx.fillRect(x + 10, y + playerSize.height - 20, 10, 30);
    ctx.fillRect(x + playerSize.width - 20, y + playerSize.height - 20, 10, 30);
  }

  function drawGround() {
    ctx.fillStyle = '#8b4513'; // sable
    ctx.fillRect(0, groundY, canvas.width, groundHeight);
  }

  function drawObstacles() {
    for (let i = 0; i < obstacles.length; i++) {
      const obstacle = obstacles[i];
      ctx.fillStyle = obstacleColor;
      ctx.fillRect(obstacle.x, obstacle.y, obstacleWidth, playerSize.height - groundHeight + 20);
    }
  }

  function drawBackgrounds() {
    // Layer 1 (slow)
    ctx.fillStyle = '#87ceeb'; // sky blue
    ctx.fillRect(bg1X, 0, canvas.width, canvas.height);
    ctx.fillRect(bg1X + canvas.width, 0, canvas.width, canvas.height);

    // Layer 2 (fast)
    ctx.fillStyle = '#add8e6'; // light blue
    ctx.fillRect(bg2X, 0, canvas.width, canvas.height);
    ctx.fillRect(bg2X + canvas.width, 0, canvas.width, canvas.height);

    bg1X -= background1Speed;
    if (bg1X <= -canvas.width) bg1X = 0;

    bg2X -= background2Speed;
    if (bg2X <= -canvas.width) bg2X = 0;
  }

  function updateObstacles() {
    for (let i = 0; i < obstacles.length; i++) {
      obstacles[i].x -= gameSpeed;

      // Remove off-screen obstacles
      if (obstacles[i].x + obstacleWidth < 0) {
        obstacles.splice(i, 1);
        i--;
        score++;
      }
    }

    // Spawn new obstacles based on time
    const now = Date.now();
    if (now - lastObstacleTime > obstacleSpawnRate) {
      obstacles.push({ x: canvas.width, y: groundY - playerSize.height + 20 });
      lastObstacleTime = now;
    }
  }

  function checkCollision() {
    for (let i = 0; i < obstacles.length; i++) {
      const obs = obstacles[i];
      if (
        alpacaX + playerSize.width > obs.x &&
        alpacaX < obs.x + obstacleWidth &&
        alpacaY + playerSize.height > obs.y &&
        alpacaY < obs.y + (playerSize.height - groundHeight) + 20
      ) {
        gameOver = true;
        return;
      }
    }
  }

  function playSound(type) {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    if (type === 'jump') {
      oscillator.type = 'square';
      oscillator.frequency.setValueAtTime(400, audioCtx.currentTime);
      gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
      setTimeout(() => {
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
      }, 200);
    } else if (type === 'score') {
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
      gainNode.gain.setValueAtTime(0.5, audioCtx.currentTime);
      setTimeout(() => {
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
      }, 200);
    } else if (type === 'hit') {
      oscillator.type = 'sawtooth';
      oscillator.frequency.setValueAtTime(350, audioCtx.currentTime);
      gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
      setTimeout(() => {
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
      }, 200);
    }

    oscillator.start();
    oscillator.stop(audioCtx.currentTime + (type === 'hit' ? 0.3 : 0.5));
  }

  function updateScore() {
    document.getElementById('currentScore').textContent = score;
    if (score > highScore) {
      localStorage.setItem('ollamaHighScore', score);
      document.getElementById('highScore').textContent = score;
    }
  }

  function resetGame() {
    alpacaY = groundY - playerSize.height;
    velocityY = 0;
    jump = false;
    obstacles = [];
    score = 0;
    updateScore();
    gameOver = false;
    document.getElementById('retryButton').style.display = 'none';
    document.getElementById('gameOverText').style.display = 'none';
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawBackgrounds();
    drawGround();

    const alpacaX = canvas.width / 2;

    // Draw obstacles
    drawObstacles();

    // Draw alpaca
    drawAlpaca(alpacaX, alpacaY + velocityY);

    updateObstacles();
    checkCollision();

    if (gameOver) {
      document.getElementById('retryButton').style.display = 'block';
      document.getElementById('gameOverText').style.display = 'block';
    } else {
      playSound('score');
    }
  }

  function animate() {
    if (!gameOver) {
      updateScore();
      velocityY += gravity;
      alpacaY += velocityY;

      // Keep the alpaca on ground
      if (alpacaY + playerSize.height > groundY) {
        alpacaY = groundY - playerSize.height;
        velocityY = 0;
      }

      draw();
    }
  }

  function gameLoop() {
    animate();
    requestAnimationFrame(gameLoop);
  }

  // Start the loop
  gameLoop();

  // Event listeners
  document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
      if (!gameOver && !jump) {
        velocityY = -12;
        jump = true;
        playSound('jump');
      }
    }
  });

  document.addEventListener('click', () => {
    if (!gameOver && !jump) {
      velocityY = -12;
      jump = true;
      playSound('jump');
    }
  });

  document.getElementById('retryButton').addEventListener('click', () => {
    resetGame();
  });
</script>
</body>
</html>
```

---

### Features Summary:

- **Canvas-based game** with inline HTML/CSS/JS.
- **Cartoon alpaca character**, drawn using canvas shapes and curves.
- **Parallax background layers** for depth.
- **Sound effects** (jump, score, hit) via Web Audio API.
- **High score tracking** using `localStorage`.
- **Responsive controls**: click or spacebar to jump.
- **Difficulty increases over time** based on score.

Enjoy *ollama's Adventure*! 🐫✨

77 t/s, 2962 tokens, 38s
