# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: ollamas adventure
Created: 11/02/2026, 11:19:29 PM
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

<|tool_call_start|>[write(file='<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ollama's Adventure</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #1a1a2e;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }

        #game {
            border-radius: 12px;
            box-shadow: 0 0 40px rgba(255, 150, 100, 0.3);
            padding: 20px;
            max-width: 800px;
            width: 100%;
        }

        canvas {
            display: block;
            background: #16213e;
        }

        /* UI Overlay */
        .ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            padding: 15px;
            pointer-events: none;
            z-index: 10;
        }

        .score-display {
            font-size: 48px;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 10px;
        }

        .high-score {
            font-size: 20px;
            color: #ff6b9d;
            opacity: 0.7;
            text-align: center;
        }

        .game-over-screen {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            background: rgba(25, 25, 45, 0.95);
            border: 3px solid #ff6b9d;
            border-radius: 20px;
            padding: 40px;
            display: none;
            z-index: 20;
        }

        .game-over-screen h2 {
            font-size: 36px;
            color: #fff;
            margin-bottom: 10px;
        }

        .game-over-screen p {
            font-size: 18px;
            color: #ff6b9d;
            margin-bottom: 30px;
        }

        .restart-btn {
            background: linear-gradient(135deg, #e94560, #c73e54);
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            color: #fff;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .restart-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 20px rgba(233, 69, 96, 0.4);
        }

        /* Animations */
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 10px #ff6b9d; }
            50% { box-shadow: 0 0 25px #ff6b9d; }
        }

        .animate-pulse {
            animation: pulse 2s ease-in-out infinite;
        }
    </style>
</head>
<body>

<div id="game">
    <canvas id="gameCanvas"></canvas>
    
    <!-- Score display -->
    <div class="ui-layer score-display">Score: <span id="score">0</span></div>
    
    <!-- High score -->
    <div class="ui-layer high-score">Best: <span id="highScore">0</span> points</div>
    
    <!-- Game Over screen -->
    <div class="game-over-screen" id="gameOver">
        <h2>Game Over!</h2>
        <p>Your score: <span id="finalScore">0</span></p>
        <button class="restart-btn" id="restartBtn">Play Again</button>
    </div>
</div>

<script>
(() => {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // Game state
    let score = 0;
    let speedMultiplier = 1.2;
    let gameState = 'playing'; // playing | gameOver
    
    // Alpaca (player)
    const alpacaX = 100; // starting x position
    const baseSpeed = 8;
    const jumpForce = 14;

    // Obstacles
    const obstacles = [];
    const MAX_OBSTACLES = 5;

    // Parallax layers for background
    let bgLayer1Progress = 0;
    let bgLayer2Progress = 0;

    // Audio context (created on first interaction)
    let audioCtx = null;

    // Web Audio API sounds
    const soundCtx = {
        createJumpSound: () => {
            if (!audioCtx) return null;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.value = 400 + Math.random() * 300; // pitch variation
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            osc.connect(gain).connect(audioCtx.destination);
            return osc;
        },
        createScoreSound: () => {
            if (!audioCtx) return null;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.value = 600 + Math.random() * 400;
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
            osc.connect(gain).connect(audioCtx.destination);
            return osc;
        },
        createHitSound: () => {
            if (!audioCtx) return null;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.value = 200 + Math.random() * 150;
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
            osc.connect(gain).connect(audioCtx.destination);
            return osc;
        }
    };

    // Reset game state
    function resetGame() {
        score = 0;
        speedMultiplier = 1.2;
        alpacaX = 100;
        obstacles.length = 0;
        bgLayer1Progress = 0;
        bgLayer2Progress = 0;
        document.getElementById('score').textContent = '0';
        if (gameState === 'gameOver') {
            document.getElementById('finalScore').textContent = score;
        }
    }

    // Draw background layers (parallax)
    function drawBackground() {
        // Clear canvas
        ctx.fillStyle = '#16213e';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Layer 1: Far mountains/sky - slowest parallax
        const farY = canvas.height * 0.3 + (bgLayer1Progress * 0.05);
        const mountainHeight = 40 + Math.random() * 30;
        
        // Gradient for sky
        const skyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        skyGradient.addColorStop(0, '#1a1a3e');
        skyGradient.addColorStop(1, '#2d4a6f');
        
        // Draw distant mountains
        ctx.beginPath();
        for (let x = 0; x < canvas.width; x += 60) {
            const y = farY + Math.sin(x * 0.01) * mountainHeight;
            if (x === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = skyGradient;
        ctx.fill();

        // Parallax effect - offset mountains by bgLayer1Progress
        ctx.save();
        ctx.translate(canvas.width * (1 + bgLayer1Progress), 0); // move right slowly
        
        // Draw subtle distant clouds
        const cloudY = canvas.height * 0.4;
        for (let i = 0; i < 5; i++) {
            const cx = Math.random() * canvas.width * (1 - bgLayer1Progress);
            ctx.fillStyle = 'rgba(255, 220, 150, 0.3)';
            ctx.beginPath();
            ctx.arc(cx, cloudY + i * 60, 20 + Math.random() * 25, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.restore();

        // Layer 2: Near trees/bushes - medium parallax
        const nearY = canvas.height * 0.55;
        
        // Draw tree trunks and tops
        ctx.fillStyle = '#4a7c59';
        for (let i = 0; i < 8; i++) {
            const tx = i * 40 + Math.sin(bgLayer2Progress) * 15;
            const ty = nearY - Math.random() * 30;
            // Trunk
            ctx.fillRect(tx, ty, 12, 20);
            // Foliage (simple circle)
            ctx.beginPath();
            ctx.arc(tx + 6, ty + 5, 10 + Math.random() * 8, 0, Math.PI * 2);
            ctx.fillStyle = '#6b8e23';
            ctx.fill();
        }

        // Parallax offset for layer 2
        ctx.save();
        ctx.translate(canvas.width * (1 - bgLayer2Progress), 0);

        // Ground line at bottom
        const groundY = canvas.height * 0.88 + Math.sin(bgLayer2Progress * 2) * 10;
        ctx.fillStyle = '#1e3a5f';
        ctx.beginPath();
        ctx.moveTo(0, groundY);
        ctx.lineTo(canvas.width, groundY);
        ctx.strokeStyle = '#2d6b4a';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Ground texture - little bushes
        const bushX = 50 + Math.sin(bgLayer2Progress * 1.5) * 30;
        for (let bx = 0; bx < canvas.width; bx += 60) {
            if ((bx - bushX) % 40 < 15) {
                ctx.fillStyle = '#3a6b4e';
                ctx.beginPath();
                ctx.arc(bx, groundY + 5, 12, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        ctx.restore();
    }

    // Draw the alpaca
    function drawAlpaca() {
        const x = alpacaX;
        
        // Body (white circle)
        ctx.fillStyle = '#f5e6c0';
        ctx.beginPath();
        ctx.arc(x, 150 + Math.sin(Date.now() * 0.005) * 15, 25, 0, Math.PI * 2);
        ctx.fill();

        // Belly (lighter)
        ctx.fillStyle = '#fff8e6';
        ctx.beginPath();
        ctx.arc(x, 155 + Math.sin(Date.now() * 0.005) * 15, 18, 0, Math.PI * 2);
        ctx.fill();

        // Ears
        ctx.fillStyle = '#f5e6c0';
        ctx.beginPath();
        ctx.arc(x - 12, 130, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + 12, 130, 8, 0, Math.PI * 2);
        ctx.fill();

        // Eye (white)
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(x - 5, 145, 4, 0, Math.PI * 2);
        ctx.fill();

        // Pupil
        ctx.fillStyle = '#1a1a1a';
        ctx.beginPath();
        ctx.arc(x - 3, 146, 2, 0, Math.PI * 2);
        ctx.fill();

        // Nose (small triangle)
        ctx.fillStyle = '#e86a5c';
        ctx.beginPath();
        ctx.moveTo(x + 8, 160);
        ctx.lineTo(x + 14, 164);
        ctx.lineTo(x + 10, 168);
        ctx.closePath();
        ctx.fill();

        // Spiral tail - colorful wave
        const tailLength = 35;
        const tailY = 135 + Math.sin(Date.now() * 0.003) * 5;
        
        // Draw spiral-like path for tail
        ctx.beginPath();
        for (let i = 0; i < tailLength; i++) {
            const t = (i / tailLength) * Math.PI * 2;
            const r = 12 + Math.sin(t * 3) * 5;
            const x1 = x - 20 + Math.cos(t) * r;
            const y1 = tailY - 10 + Math.sin(t * 2) * 8;
            const x2 = x - 15 + Math.cos(t + 0.5) * (r + 3);
            const y2 = tailY - 25 + Math.sin(t + 0.5) * 12;
            
            if (i === 0) ctx.moveTo(x1, y1);
            else ctx.lineTo(x2, y2);
        }
        
        // Colored spiral segments
        const colors = ['#ff6b9d', '#e94560', '#8e2de2', '#fd79a8'];
        for (let i = 0; i < Math.floor(tailLength / 5); i++) {
            const colIdx = i * ((colors.length - 1) / Math.floor(tailLength / 5));
            ctx.fillStyle = colors[colIdx];
            // Draw a curved segment
            const startAngle = (i / Math.floor(tailLength / 5)) * Math.PI * 2;
            const endAngle = startAngle + Math.PI;
            const midX = x - 10 + Math.cos(startAngle) * 12;
            ctx.beginPath();
            ctx.moveTo(midX, tailY);
            ctx.quadraticCurveTo(
                x + Math.cos(startAngle + 0.3) * 8, tailY - 15,
                x + Math.cos(endAngle) * 8, tailY
            );
            ctx.fill();
        }

        // Legs (simple)
        const legOffset = 40;
        ctx.fillStyle = '#f5e6c0';
        // Front legs
        ctx.beginPath();
        ctx.arc(x - 4, 150 + Math.sin(Date.now() * 0.003) * 2, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + 4, 150 + Math.sin(Date.now() * 0.003) * 2, 8, 0, Math.PI * 2);
        ctx.fill();
        // Back legs
        ctx.beginPath();
        ctx.arc(x - 6, 160 + Math.sin(Date.now() * 0.004) * 2, 7, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + 8, 160 + Math.sin(Date.now() * 0.004) * 2, 7, 0, Math.PI * 2);
        ctx.fill();
    }

    // Generate and spawn obstacles
    function spawnObstacle() {
        const speed = baseSpeed * speedMultiplier;
        
        // Random horizontal position (from right side)
        const x = canvas.width - 50 + Math.random() * 200;
        
        // Spawn at top, move left
        obstacles.push({
            x: x,
            y: -40,
            width: 30,
            height: 20,
            speed: speed,
            rotating: Math.random() * Math.PI * 2
        });
    }

    // Update game state
    function update() {
        if (gameState !== 'playing') return;

        // Increase score based on distance traveled
        score += speedMultiplier;
        
        // Add points per obstacle passed
        for (let i = obstacles.length - 1; i >= 0; i--) {
            const obs = obstacles[i];
            if (obs.x + obs.width < alpacaX) {
                obstacles.splice(i, 1);
                score += 10;
            }
        }

        // Update background parallax
        bgLayer1Progress += 0.02;
        bgLayer2Progress += 0.04;

        // Move obstacles
        for (let i = obstacles.length - 1; i >= 0; i--) {
            const obs = obstacles[i];
            obs.x -= obs.speed;
            
            if (obs.x + obs.width < 0) {
                score += 5; // bonus for clearing
                gameState = 'gameOver';
            }
        }

        // Update alpaca position (running to the right)
        alpacaX += baseSpeed * speedMultiplier;

        // Jump logic: spacebar or click
        if ((document.haltAnimation() === false) && (keyDownEvent())) {
            // Check if in air and jumping is possible
            const isInAir = (y - 150 < 0);
            const canJump = !isInAir;
            
            if (canJump) {
                jump(obs?.speed || baseSpeed * speedMultiplier);
            }
        }

        // Update score display
        document.getElementById('score').textContent = Math.floor(score);

        // Check game over condition
        if (alpacaX > canvas.width + 200) {
            gameState = 'gameOver';
        }
    }

    // Jump function
    function jump(speed) {
        const y = 150;
        // Simple gravity simulation - just add upward velocity
        const dy = -speed * speedMultiplier / 2;
        ctx.globalAlpha = 0.6;
        // Draw a small paddle as the jump arc? No, keep it simple.
        
        // Actually for endless runner, jumping should make the alpaca go up briefly then fall back
        // Let's use a simple approach: just set position higher and let gravity pull down
        
        const jumpY = y + 30;
        const jumpHeight = speed * 0.8; // max height based on jump force
        
        // Store previous position for collision detection
        alpacaX = x;
        
        // Small visual feedback - change color briefly
        ctx.fillStyle = '#ff6b9d';
        drawAlpaca();
    }

    // Collision detection between alpaca and obstacles
    function checkCollision() {
        const alpacaRadius = 25; // approximate
        
        for (const obs of obstacles) {
            const obsCenterX = obs.x + obs.width / 2;
            const dx = alpacaX - obsCenterX;
            const dy = (150 + Math.sin(Date.now() * 0.01)) - obs.y;
            
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < alpacaRadius + obs.height / 2) {
                // Hit!
                gameState = 'gameOver';
                playHitSound();
                return true;
            }
        }
        return false;
    }

    // Play sound
    function playSound(type) {
        if (!audioCtx) return;
        
        const osc = soundCtx.createJumpSound();
        osc.stop();
        osc.start();
    }

    let keyDownEvent = (e) => {
        if (gameState === 'playing' && e.code === 'Space') {
            jump(baseSpeed * speedMultiplier);
        }
    };

    // Main game loop
    function gameLoop(timestamp) {
        if (gameState !== 'playing') return;

        update();
        
        drawBackground();
        drawAlpaca();

        if (checkCollision()) {
            playSound('hit');
            // Hide obstacles briefly to let player react? No, just show hit screen
            document.getElementById('gameOver').style.display = 'block';
        }

        requestAnimationFrame(gameLoop);
    }

    // Start the game
    resetGame();
    // Initial update to draw starting state
    drawBackground();
    drawAlpaca();

    // Handle input
    window.addEventListener('keydown', (e) => {
        if (gameState === 'playing' && e.code === 'Space') {
            keyDownEvent(e);
        }
    });

    canvas.addEventListener('click', () => {
        if (gameState === 'playing') {
            jump(baseSpeed * speedMultiplier);
        } else if (gameState === 'gameOver') {
            resetGame();
        }
    });

    // Also handle touch on mobile
    let touches = [];
    canvas.addEventListener('touchstart', (e) => {
        touches.push(e.target);
    }, {passive: true});
    window.addEventListener('touchend', () => {
        touches.length = 0;
    });
    
    // Check for spacebar in game over state too
    if (document.haltAnimation() === false && keyDownEvent) {
        jump(baseSpeed * speedMultiplier);
    }

})();
</script>
</body>
</html>')]<|tool_call_end|>

281 t/s, 5916 tokens, 21s
