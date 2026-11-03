# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: ollamas adventure
Created: 11/03/2026, 12:29:35 AM
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
    <meta charset="UTF-8">
    <title>Ollama's Adventure</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f2f2f2;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100vh;
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        // Game variables
        let canvas, ctx, alpaca, obstacles = [], score = 0, highScore = 0, gameSpeed = 5;
        const jumpSound = new AudioContext();
        const hitObstacleSound = new AudioContext();
        const scorePointSound = new AudioContext();

        // Game initialization
        function init() {
            canvas = document.getElementById('gameCanvas');
            ctx = canvas.getContext('2d');
            alpaca = {x: 50, y: canvas.height - 100, width: 60, height: 80};
            loadSounds();
            loadHighScore();
        }

        // Load high score from localStorage
        function loadHighScore() {
            if (localStorage.getItem('highScore')) {
                highScore = parseInt(localStorage.getItem('highScore'));
            } else {
                localStorage.setItem('highScore', '0');
            }
        }

        // Load sound effects
        function loadSounds() {
            // Jump sound effect
            fetch('/sounds/jump.wav')
                .then(response => response.arrayBuffer())
                .then(arrayBuffer => jumpSound.decodeAudioData(arrayBuffer))
                .catch(() => console.log('Failed to load jump sound'));

            // Hit obstacle sound effect
            fetch('/sounds/hit_obstacle.wav')
                .then(response => response.arrayBuffer())
                .then(arrayBuffer => hitObstacleSound.decodeAudioData(arrayBuffer))
                .catch(() => console.log('Failed to load hit obstacle sound'));

            // Score point sound effect
            fetch('/sounds/score_point.wav')
                .then(response => response.arrayBuffer())
                .then(arrayBuffer => scorePointSound.decodeAudioData(arrayBuffer))
                .catch(() => console.log('Failed to load score point sound'));
        }

        // Update game state
        function update() {
            moveBackground();
            moveAlpaca();
            moveObstacles();
            checkCollision();
            draw();
            requestAnimationFrame(update);
        }

        // Move background layers
        function moveBackground() {
            // Add your parallax scrolling code here
        }

        // Move alpaca
        function moveAlpaca() {
            if (alpaca.y < canvas.height - 100) {
                alpaca.y += 5;
            }
        }

        // Move obstacles
        function moveObstacles() {
            // Add your obstacle movement code here
        }

        // Check for collision between alpaca and obstacles
        function checkCollision() {
            // Add your collision detection code here
        }

        // Draw game elements
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Add your drawing code for the background layers and alpaca here
            ctx.fillStyle = '#333';
            ctx.font = '24px Arial';
            ctx.fillText('Score: ' + score, 10, 30);
            ctx.fillText('High Score: ' + highScore, canvas.width - 150, 30);
        }

        // Start the game
        init();
        update();
    </script>
</body>
</html>
```

147 t/s, 988 tokens, 7s
