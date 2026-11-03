# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: ollamas adventure
Created: 11/03/2026, 12:50:44 AM
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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Ollama's Adventure</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #1a1a2e;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', system-ui, sans-serif;
        -webkit-tap-highlight-color: transparent;
        touch-action: manipulation;
    }

    body {
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(ellipse at 50% 30%, #2d1b6e 0%, #1a1a2e 70%);
    }

    #game-container {
        position: relative;
        width: min(96vw, 900px);
        height: min(54vh, 520px);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 25px 70px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.08);
    }

    canvas {
        display: block;
        width: 100%;
        height: 100%;
        cursor: pointer;
    }

    .overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 24px;
    }

    #start-screen {
        background: linear-gradient(180deg, rgba(30,15,66,0.92) 0%, rgba(15,10,40,0.95) 100%);
    }

    #game-over-screen {
        display: none;
        background: linear-gradient(180deg, rgba(60,15,20,0.92) 0%, rgba(30,8,15,0.96) 100%);
    }

    .title {
        font-size: clamp(2rem, 7vw, 3.4rem);
        color: #ffd93d;
        text-shadow: 0 4px 0 #c8a015, 0 8px 20px rgba(0,0,0,0.6), 3px 3px 0 #e8b923;
        letter-spacing: 1px;
        margin-bottom: 6px;
        animation: titleBounce 2s ease-in-out infinite;
    }

    @keyframes titleBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    .subtitle {
        font-size: clamp(0.9rem, 3vw, 1.2rem);
        color: #b8c6ff;
        margin-bottom: 24px;
        opacity: 0.9;
        line-height: 1.5;
    }

    .btn {
        font-family: inherit;
        font-size: clamp(1rem, 4vw, 1.3rem);
        font-weight: bold;
        color: #fff;
        background: linear-gradient(180deg, #ff6b6b, #ee5253);
        border: none;
        border-radius: 50px;
        padding: 16px 44px;
        margin: 8px;
        cursor: pointer;
        box-shadow: 0 6px 0 #b33939, 0 8px 20px rgba(0,0,0,0.4);
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        text-shadow: 0 2px 3px rgba(0,0,0,0.3);
    }

    .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 0 #b33939, 0 12px 24px rgba(0,0,0,0.45); }
    .btn:active { transform: translateY(4px); box-shadow: 0 2px 0 #b33939, 0 4px 10px rgba(0,0,0,0.4); }

    .hint {
        margin-top: 26px;
        color: #8f9bd0;
        font-size: clamp(0.75rem, 2.6vw, 0.95rem);
        line-height: 1.7;
        opacity: 0.85;
    }

    .hint kbd {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 6px;
        padding: 2px 10px;
        font-family: inherit;
        color: #dfe6ff;
    }

    .final-score {
        font-size: clamp(1rem, 4vw, 1.5rem);
        color: #ffe08a;
        margin-bottom: 6px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }

    .new-record {
        font-size: clamp(1.1rem, 4.5vw, 1.7rem);
        color: #ffd93d;
        margin-bottom: 20px;
        text-shadow: 0 3px 0 #c8a015, 0 6px 16px rgba(0,0,0,0.5);
        animation: pulse 0.7s ease-in-out infinite alternate;
    }

    @keyframes pulse { from { transform: scale(1); opacity: 1; } to { transform: scale(1.08); opacity: 0.85; } }

    .go-title { font-size: clamp(2rem, 7vw, 3rem); color: #ff6b6b; text-shadow: 0 4px 0 #c0392b, 0 8px 20px rgba(0,0,0,0.5); }

    .best-display {
        font-size: clamp(0.8rem, 3vw, 1.05rem);
        color: #a8d8ff;
        margin-top: 14px;
        opacity: 0.9;
    }

    /* HUD */
    #hud {
        position: absolute;
        top: 0; left: 0; right: 0;
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        padding: 14px 20px;
        pointer-events: none;
        z-index: 5;
    }

    .hud-box {
        background: rgba(15,10,40,0.5);
        backdrop-filter: blur(4px);
        border-radius: 14px;
        padding: 8px 16px;
        color: #fff;
        font-size: clamp(0.9rem, 3vw, 1.2rem);
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3), inset 0 0 0 1px rgba(255,255,255,0.08);
    }

    #score-value { color: #ffd93d; font-size: clamp(1.1rem, 4vw, 1.6rem); }
    #best-value { color: #a8e6cf; font-size: clamp(0.75rem, 2.5vw, 0.95rem); opacity: 0.9; }

    .speed-bar-wrap {
        width: min(45vw, 150px);
        height: 12px;
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
        margin-top: 6px;
        overflow: hidden;
    }

    #speed-bar {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #4ecdc4, #ffe66d);
        border-radius: 8px;
        transition: width 0.2s ease;
    }

    .tap-hint {
        position: absolute;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255,255,255,0.4);
        font-size: clamp(0.65rem, 2.2vw, 0.8rem);
        pointer-events: none;
        z-index: 5;
    }

    @media (max-width: 560px) {
        .hud-box { padding: 6px 12px; }
        #game-container { height: min(60vh, 480px); }
    }
</style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas"></canvas>

    <div id="hud" style="display:none;">
        <div class="hud-box">
            Score<br><span id="score-value">0</span>
        </div>
        <div class="hud-box" style="text-align:right;">
            Best<br><span id="best-value">0</span>
        </div>
    </div>

    <div id="start-screen" class="overlay">
        <div class="title">🦙 Ollama's Adventure</div>
        <p class="subtitle">Help little Ollama the alpaca run, jump &amp; survive!</p>
        <button class="btn" id="play-btn">▶ Play</button>
        <p class="hint">
            Press <kbd>Space</kbd> or click / tap to jump<br>
            Dodge rocks 🪨, logs 🪵 and cacti 🌵<br>
            Speed gets faster the longer you survive!
        </p>
    </div>

    <div id="game-over-screen" class="overlay">
        <div class="go-title">💥 Oops!</div>
        <div class="final-score">Score: <span id="final-score-value">0</span></div>
        <div class="new-record" id="record-banner" style="display:none;">🏆 New High Score! 🏆</div>
        <button class="btn" id="retry-btn">↻ Play Again</button>
        <p class="best-display">Best: <span id="go-best-value">0</span></p>
    </div>

    <div id="tap-hint" class="tap-hint">Tap or press Space to jump</div>
</div>

<script>
(function () {
    "use strict";

    // ===================== CANVAS SETUP =====================
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    const container = document.getElementById('game-container');
    let W = 0, H = 0, DPR = 1;

    function resize() {
        const rect = container.getBoundingClientRect();
        DPR = Math.min(window.devicePixelRatio || 1, 2);
        W = rect.width;
        H = rect.height;
        canvas.width = Math.floor(W * DPR);
        canvas.height = Math.floor(H * DPR);
        ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    }
    window.addEventListener('resize', resize);
    resize();

    // ===================== GAME CONSTANTS =====================
    const GROUND_Y_RATIO = 0.82;      // ground line as fraction of height
    let GROUND_Y = 0;                 // computed each frame from H

    function getGroundY() { return H * GROUND_Y_RATIO; }

    const GRAVITY = 2600;             // px/s^2
    const JUMP_VELOCITY = -900;       // px/s initial jump velocity
    const START_SPEED = 320;          // base scroll speed px/s
    const MAX_SPEED = 780;            // cap
    const SPEED_RAMP = 6;             // +px/s per second survived

    // ===================== AUDIO (Web Audio API) =====================
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            try {
                const AC = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AC();
            } catch (e) { audioCtx = null; }
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    // Play a short square-wave blip. Nice for cartoonish SFX.
    function playBlip(freq, dur, type, gainVal) {
        if (!audioCtx) return;
        const t = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = type || 'square';
        osc.frequency.setValueAtTime(freq, t);
        // quick envelope to avoid clicks
        g.gain.setValueAtTime(gainVal != null ? gainVal : 0.12, t);
        g.gain.exponentialRampToValueAtTime(0.001, t + dur);
        osc.connect(g).connect(audioCtx.destination);
        osc.start(t);
        osc.stop(t + dur + 0.02);
    }

    function sfxJump() {
        if (!audioCtx) return;
        // rising "boing" - two quick ascending blips
        playBlip(320, 0.14, 'square', 0.13);
        setTimeout(function () { playBlip(480, 0.16, 'square', 0.11); }, 55);
    }

    function sfxScore() {
        if (!audioCtx) return;
        // happy little chime: major-ish arpeggio
        const notes = [523, 659, 784];
        notes.forEach(function (f, i) {
            setTimeout(function () { playBlip(f, 0.12, 'triangle', 0.1); }, i * 65);
        });
    }

    function sfxCrash() {
        if (!audioCtx) return;
        // low "thud" + descending buzz
        playBlip(180, 0.28, 'sawtooth', 0.16);
        setTimeout(function () { playBlip(90, 0.35, 'sawtooth', 0.14); }, 70);
    }

    // ===================== GAME STATE =====================
    const STATE = { MENU: 0, PLAYING: 1, DEAD: 2 };
    let state = STATE.MENU;

    let score = 0;
    let bestScore = parseInt(localStorage.getItem('ollama_best') || '0', 10) || 0;
    let gameSpeed = START_SPEED;
    let distance = 0;
    let spawnTimer = 0;
    let nextSpawnIn = 1.1;
    let elapsed = 0;

    // ===================== ALPACA (player) =====================
    const alpaca = {
        x: 0,          // set on resize
        y: 0,
        w: 96,         // body width (visual)
        h: 84,         // body height
        vy: 0,
        onGround: true,
        jumpHeld: false,   // for variable-height jump
        runPhase: 0,       // animation timer
        tilt: 0,           // rotation for jump arc (deg)
    };

    function resetAlpaca() {
        alpaca.x = W * 0.22;
        alpaca.y = getGroundY() - 46;   // resting on ground
        alpaca.vy = 0;
        alpaca.onGround = true;
        alpaca.jumpHeld = false;
        alpaca.tilt = 0;
        alpaca.runPhase = 0;
    }

    function jump() {
        if (state !== STATE.PLAYING) return;
        if (alpaca.onGround) {
            alpaca.vy = JUMP_VELOCITY;
            alpaca.onGround = false;
            alpaca.jumpHeld = true;
            sfxJump();
        }
    }

    // ===================== OBSTACLES =====================
    let obstacles = [];

    const OBS_TYPES = ['rock', 'log', 'cactus'];

    function spawnObstacle() {
        const type = OBS_TYPES[Math.floor(Math.random() * OBS_TYPES.length)];
        let w, h;
        if (type === 'rock') { w = 46 + Math.random() * 20; h = 38 + Math.random() * 16; }
        else if (type === 'log') { w = 74 + Math.random() * 22; h = 30 + Math.random() * 8; }
        else { // cactus
            w = 30 + Math.random() * 14;
            h = 62 + Math.random() * 22;
        }

        obstacles.push({
            type: type,
            x: W + 60,
            y: getGroundY() - h,
            w: w,
            h: h,
            passed: false,
        });
    }

    // ===================== CLOUDS & BIRDS (decorative) =====================
    let clouds = [];
    let birds = [];

    function initDecor() {
        clouds = [];
        for (let i = 0; i < 5; i++) {
            clouds.push({
                x: Math.random() * W,
                y: 30 + Math.random() * (H * 0.35),
                scale: 0.6 + Math.random() * 0.8,
                speed: 12 + Math.random() * 14,
            });
        }
        birds = [];
        for (let i = 0; i < 4; i++) {
            birds.push({
                x: Math.random() * W,
                y: 50 + Math.random() * (H * 0.3),
                speed: 28 + Math.random() * 22,
                flap: Math.random() * Math.PI * 2,
            });
        }
    }

    // ===================== STARS (night sky) =====================
    let stars = [];
    function initStars() {
        stars = [];
        for (let i = 0; i < 40; i++) {
            stars.push({ x: Math.random() * W, y: Math.random() * H * 0.5, s: Math.random() * 1.8 + 0.4 });
        }
    }

    // ===================== PARTICLES (dust & sparkles) =====================
    let particles = [];

    function addDust(x, y) {
        for (let i = 0; i < 3; i++) {
            particles.push({
                x: x - Math.random() * 10,
                y: y,
                vx: -(60 + Math.random() * 80),
                vy: -Math.random() * 40,
                life: 0.35,
                maxLife: 0.35,
                size: 3 + Math.random() * 3,
                color: '#d9c9a3',
            });
        }
    }

    function addSparkles(x, y) {
        for (let i = 0; i < 8; i++) {
            const a = (Math.PI * 2 / 8) * i;
            particles.push({
                x: x, y: y,
                vx: Math.cos(a) * (120 + Math.random() * 80),
                vy: Math.sin(a) * (120 + Math.random() * 80),
                life: 0.5, maxLife: 0.5,
                size: 2 + Math.random() * 3,
                color: i % 2 === 0 ? '#ffd93d' : '#ff6b6b',
            });
        }
    }

    // ===================== COLLISION =====================
    function hitTest(ax, ay, aw, ah, ox, oy, ow, oh) {
        const pad = 14; // forgiveness padding
        return ax < ox + ow - pad &&
               ax + aw > ox + pad &&
               ay < oy + oh - pad * 0.6 &&
               ay + ah > oy + pad;
    }

    // ===================== DRAWING HELPERS =====================
    function roundRect(x, y, w, h, r) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + w, y, x + w, y + h, r);
        ctx.arcTo(x + w, y + h, x, y + h, r);
        ctx.arcTo(x, y + h, x, y, r);
        ctx.arcTo(x, y, x + w, y, r);
        ctx.closePath();
    }

    // ===================== DRAW ALPACA =====================
    function drawAlpaca() {
        const a = alpaca;
        const cx = a.x + a.w / 2;
        const groundY = getGroundY();
        const bodyTop = a.y - a.h * 0.55;   // top of head/body

        ctx.save();
        ctx.translate(cx, a.y);
        ctx.rotate(a.tilt * Math.PI / 180);
        ctx.translate(-cx, -a.y);

        const legSwing = a.onGround ? Math.sin(a.runPhase) * 14 : 6;
        const legSwing2 = a.onGround ? Math.sin(a.runPhase + Math.PI) * 14 : -6;

        // ---- shadow (on ground) ----
        ctx.save();
        const shScale = 1 - Math.min(0.55, (groundY - (a.y)) / 500);
        ctx.globalAlpha = 0.22 * Math.max(0.15, shScale);
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.ellipse(a.x + a.w / 2, groundY + 3, a.w * 0.42 * shScale, 10 * shScale, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // ---- back legs ----
        ctx.strokeStyle = '#f0e6d8';
        ctx.lineWidth = 9;
        ctx.lineCap = 'round';
        // left back leg
        ctx.beginPath();
        ctx.moveTo(a.x + a.w * 0.32, bodyTop + a.h * 0.5);
        ctx.lineTo(a.x + a.w * 0.28 - legSwing * 0.7, groundY);
        ctx.stroke();
        // right back leg
        ctx.beginPath();
        ctx.moveTo(a.x + a.w * 0.46, bodyTop + a.h * 0.5);
        ctx.lineTo(a.x + a.w * 0.5 - legSwing2 * 0.7, groundY);
        ctx.stroke();

        // ---- fluffy back rump ----
        ctx.fillStyle = '#f5ede0';
        roundRect(a.x + a.w * 0.18, bodyTop + a.h * 0.32, a.w * 0.62, a.h * 0.42, 20);
        ctx.fill();

        // ---- fluffy tail ----
        ctx.fillStyle = '#fffdf7';
        ctx.beginPath();
        ctx.arc(a.x + a.w * 0.18, bodyTop + a.h * 0.52, 13, 0, Math.PI * 2);
        ctx.fill();

        // ---- main body ----
        ctx.fillStyle = '#faf4ea';
        roundRect(a.x + a.w * 0.26, bodyTop + a.h * 0.28, a.w * 0.58, a.h * 0.5, 22);
        ctx.fill();

        // ---- front legs ----
        ctx.strokeStyle = '#f0e6d8';
        ctx.lineWidth = 9;
        // left front leg
        ctx.beginPath();
        ctx.moveTo(a.x + a.w * 0.62, bodyTop + a.h * 0.5);
        ctx.lineTo(a.x + a.w * 0.64 + legSwing, groundY);
        ctx.stroke();
        // right front leg
        ctx.beginPath();
        ctx.moveTo(a.x + a.w * 0.76, bodyTop + a.h * 0.5);
        ctx.lineTo(a.x + a.w * 0.8 - legSwing2, groundY);
        ctx.stroke();

        // ---- neck & head ----
        const headCx = a.x + a.w * 0.74;
        const headCy = bodyTop - a.h * 0.16;
        const headR = a.h * 0.32;

        // neck
        ctx.fillStyle = '#faf4ea';
        roundRect(a.x + a.w * 0.6, bodyTop - a.h * 0.05, a.h * 0.28, a.h * 0.28, 12);
        ctx.fill();

        // head (fluffy)
        ctx.fillStyle = '#fffdf7';
        ctx.beginPath();
        ctx.arc(headCx, headCy, headR, 0, Math.PI * 2);
        ctx.fill();

        // fluffy cheeks
        ctx.beginPath();
        ctx.arc(headCx - headR * 0.9, headCy + headR * 0.35, headR * 0.6, 0, Math.PI * 2);
        ctx.arc(headCx + headR * 0.9, headCy + headR * 0.35, headR * 0.6, 0, Math.PI * 2);
        ctx.fill();

        // ---- ears ----
        ctx.fillStyle = '#f0e6d8';
        ctx.beginPath();
        ctx.ellipse(headCx - headR * 0.7, headCy - headR * 0.9, 7, 15, -0.4, 0, Math.PI * 2);
        ctx.ellipse(headCx + headR * 0.7, headCy - headR * 0.9, 7, 15, 0.4, 0, Math.PI * 2);
        ctx.fill();

        // ---- face mask (dark) ----
        ctx.fillStyle = '#4a3b32';
        // muzzle
        ctx.beginPath();
        ctx.ellipse(headCx + headR * 0.15, headCy + headR * 0.28, headR * 0.72, headR * 0.62, 0, 0, Math.PI * 2);
        ctx.fill();

        // ---- eyes (white) ----
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(headCx - headR * 0.45, headCy - headR * 0.15, 8, 0, Math.PI * 2);
        ctx.arc(headCx + headR * 0.45, headCy - headR * 0.15, 8, 0, Math.PI * 2);
        ctx.fill();

        // ---- pupils (looking forward) ----
        ctx.fillStyle = '#2b2119';
        ctx.beginPath();
        ctx.arc(headCx - headR * 0.4 + 1.5, headCy - headR * 0.15, 4.2, 0, Math.PI * 2);
        ctx.arc(headCx + headR * 0.4 + 1.5, headCy - headR * 0.15, 4.2, 0, Math.PI * 2);
        ctx.fill();

        // eye shine
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(headCx - headR * 0.4 + 2.6, headCy - headR * 0.24, 1.8, 0, Math.PI * 2);
        ctx.arc(headCx + headR * 0.4 + 2.6, headCy - headR * 0.24, 1.8, 0, Math.PI * 2);
        ctx.fill();

        // ---- nose ----
        ctx.fillStyle = '#3a2c24';
        ctx.beginPath();
        ctx.arc(headCx + headR * 0.55, headCy + headR * 0.18, 3.2, 0, Math.PI * 2);
        ctx.fill();

        // ---- smile ----
        ctx.strokeStyle = '#3a2c24';
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.arc(headCx + headR * 0.15, headCy + headR * 0.38, 6, 0.15 * Math.PI, 0.85 * Math.PI);
        ctx.stroke();

        // ---- little blush ----
        ctx.fillStyle = 'rgba(255,140,140,0.28)';
        ctx.beginPath();
        ctx.ellipse(headCx - headR * 0.75, headCy + headR * 0.35, 6, 3.5, 0, 0, Math.PI * 2);
        ctx.fill();

        // ---- name tag ----
        ctx.fillStyle = '#ffd93d';
        ctx.font = 'bold 13px Comic Sans MS, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('ollama', headCx, bodyTop + a.h * 0.72);

        ctx.restore();
    }

    // ===================== DRAW OBSTACLES =====================
    function drawObstacle(o) {
        if (o.type === 'rock') {
            ctx.fillStyle = '#8d99ae';
            roundRect(o.x, o.y + 6, o.w, o.h - 6, 10);
            ctx.fill();
            // top cap lighter
            ctx.fillStyle = '#a3b1c4';
            roundRect(o.x, o.y, o.w, o.h * 0.4, 12);
            ctx.fill();
            // speckles
            ctx.fillStyle = 'rgba(90,100,120,0.5)';
            for (let i = 0; i < 5; i++) {
                const sx = o.x + 8 + ((i * 37) % Math.floor(o.w - 16));
                const sy = o.y + 14 + ((i * 23) % (o.h - 20));
                ctx.beginPath();
                ctx.arc(sx, sy, 2.5, 0, Math.PI * 2);
                ctx.fill();
            }
        } else if (o.type === 'log') {
            // body
            ctx.fillStyle = '#8b5e34';
            roundRect(o.x, o.y + o.h * 0.18, o.w, o.h - o.h * 0.18, 12);
            ctx.fill();
            // top ellipse (end grain)
            ctx.fillStyle = '#a06b3c';
            ctx.beginPath();
            ctx.ellipse(o.x + o.w, o.y + o.h * 0.5, o.w * 0.14, o.h * 0.5, 0, 0, Math.PI * 2);
            ctx.fill();
            // rings on end grain
            ctx.strokeStyle = '#7a5230';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(o.x + o.w, o.y + o.h * 0.5, o.h * 0.28, 0, Math.PI * 2);
            ctx.stroke();
            // wood grain lines
            ctx.strokeStyle = 'rgba(90,55,25,0.4)';
            for (let i = 0; i < 3; i++) {
                const ly = o.y + o.h * 0.28 + i * (o.h * 0.16);
                ctx.beginPath();
                ctx.moveTo(o.x + 6, ly);
                ctx.lineTo(o.x + o.w - 6, ly);
                ctx.stroke();
            }
        } else { // cactus
            const cx = o.x + o.w / 2;
            // main trunk
            ctx.fillStyle = '#3a8f5c';
            roundRect(o.x + o.w * 0.28, o.y, o.w * 0.44, o.h, 16);
            ctx.fill();
            // arms
            ctx.beginPath();
            ctx.moveTo(cx - 2, o.y + o.h * 0.35);
            ctx.lineTo(cx - o.w * 0.7, o.y + o.h * 0.35);
            roundRect(cx - o.w * 0.7, o.y + o.h * 0.35, o.w * 0.4, o.h * 0.28, 10);
            ctx.fill();
            ctx.beginPath();
            ctx.moveTo(cx - 2, o.y + o.h * 0.55);
            ctx.lineTo(cx + o.w * 0.7, o.y + o.h * 0.55);
            roundRect(cx + o.w * 0.3, o.y + o.h * 0.55, o.w * 0.4, o.h * 0.28, 10);
            ctx.fill();
            // arm tops
            ctx.beginPath();
            ctx.arc(cx - o.w * 0.7, o.y + o.h * 0.35, o.w * 0.2, Math.PI, 0);
            ctx.arc(cx + o.w * 0.7, o.y + o.h * 0.55, o.w * 0.2, 0, Math.PI);
            ctx.fill();
            // spines
            ctx.strokeStyle = 'rgba(180,230,200,0.6)';
            ctx.lineWidth = 1.5;
            for (let i = 0; i < 7; i++) {
                const sy = o.y + 10 + i * (o.h / 7);
                ctx.beginPath();
                ctx.moveTo(cx, sy);
                ctx.lineTo(cx - 4, sy - 5);
                ctx.moveTo(cx, sy);
                ctx.lineTo(cx + 4, sy - 5);
                ctx.stroke();
            }
        }
    }

    // ===================== DRAW BACKGROUND =====================
    function drawBackground() {
        const groundY = getGroundY();

        // ---- sky gradient (dusk) ----
        const skyGrad = ctx.createLinearGradient(0, 0, 0, groundY);
        skyGrad.addColorStop(0, '#2b1a5e');
        skyGrad.addColorStop(0.45, '#4a2d7a');
        skyGrad.addColorStop(0.75, '#8b4a8e');
        skyGrad.addColorStop(1, '#c96b8a');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, W, groundY);

        // ---- stars (far layer) ----
        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        for (let i = 0; i < stars.length; i++) {
            const st = stars[i];
            ctx.globalAlpha = 0.4 + Math.random() * 0.5;
            ctx.beginPath();
            ctx.arc(st.x, st.y, st.s, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;

        // ---- sun/moon (far) ----
        const sunX = W * 0.78 - distance * 0.01 % W;
        ctx.fillStyle = 'rgba(255,225,150,0.9)';
        ctx.beginPath();
        ctx.arc(W * 0.8, H * 0.22, 42, 0, Math.PI * 2);
        ctx.fill();
        const sunGlow = ctx.createRadialGradient(W * 0.8, H * 0.22, 20, W * 0.8, H * 0.22, 90);
        sunGlow.addColorStop(0, 'rgba(255,225,150,0.4)');
        sunGlow.addColorStop(1, 'rgba(255,225,150,0)');
        ctx.fillStyle = sunGlow;
        ctx.beginPath();
        ctx.arc(W * 0.8, H * 0.22, 90, 0, Math.PI * 2);
        ctx.fill();

        // ---- clouds (far layer - slowest) ----
        for (let i = 0; i < clouds.length; i++) {
            const c = clouds[i];
            const cx = ((c.x - distance * 0.1) % (W + 200));
            const drawX = cx <= -150 ? cx + (W + 200) : cx;
            ctx.fillStyle = 'rgba(230,215,245,0.55)';
            cloudShape(drawX, c.y, c.scale);
        }

        // ---- birds (mid layer) ----
        for (let i = 0; i < birds.length; i++) {
            const b = birds[i];
            const bx = ((b.x - distance * 0.35) % (W + 120));
            const drawX = bx <= -60 ? bx + (W + 120) : bx;
            const flap = Math.sin(b.flap) * 5;
            ctx.strokeStyle = 'rgba(30,20,50,0.7)';
            ctx.lineWidth = 2.5;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(drawX - 8, b.y);
            ctx.quadraticCurveTo(drawX, b.y - flap - 4, drawX + 8, b.y);
            ctx.stroke();
        }

        // ---- distant mountains (mid layer) ----
        drawMountains(groundY, distance * 0.25, '#3a2b5e', H * 0.34, 6);
        drawMountains(groundY, distance * 0.4, '#4d3a6e', H * 0.28, 8);

        // ---- ground (near layer) ----
        const gGrad = ctx.createLinearGradient(0, groundY, 0, H);
        gGrad.addColorStop(0, '#5c7a47');
        gGrad.addColorStop(0.15, '#4a6b3a');
        gGrad.addColorStop(1, '#3a522e');
        ctx.fillStyle = gGrad;
        ctx.fillRect(0, groundY, W, H - groundY);

        // ---- dirt strip under grass ----
        const dirtY = groundY + 8;
        ctx.fillStyle = '#7a5c3a';
        ctx.fillRect(0, dirtY, W, H - dirtY);

        // ---- grass blades (parallax near) ----
        drawGrass(distance * 1.0, groundY);

        // ---- ground texture dashes (fastest parallax) ----
        drawGroundDashes(distance * 1.6, groundY + 42);
    }

    function cloudShape(x, y, scale) {
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(scale, scale);
        ctx.beginPath();
        ctx.arc(0, 0, 22, 0, Math.PI * 2);
        ctx.arc(26, 4, 18, 0, Math.PI * 2);
        ctx.arc(-24, 4, 16, 0, Math.PI * 2);
        ctx.arc(4, -14, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    function drawMountains(baseY, offset, color, peakH, seed) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(0, baseY);
        const segW = 160;
        for (let x = -segW; x <= W + segW; x += segW) {
            // deterministic-ish peak using offset and seed
            const phase = Math.floor((x + offset * 3) / segW);
            const peakX = x + ((seed + phase * 7) % 60);
            ctx.lineTo(peakX - 40, baseY - peakH);
            ctx.lineTo(peakX, baseY - peakH - (20 + (phase * 13) % 50));
            ctx.lineTo(peakX + 40, baseY - peakH);
        }
        ctx.lineTo(W, baseY);
        ctx.closePath();
        ctx.fill();
    }

    function drawGrass(offset, groundY) {
        ctx.strokeStyle = '#6ea852';
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        for (let x = -40; x <= W + 40; x += 16) {
            const phase = Math.floor((x + offset * 3) / 16);
            const gx = ((x + offset) % (W + 80)) - 40;
            if (gx < -20 || gx > W + 20) continue;
            const h = 10 + ((phase * 37) % 14);
            ctx.beginPath();
            ctx.moveTo(gx, groundY);
            ctx.lineTo(gx, groundY - h);
            ctx.stroke();
        }
    }

    function drawGroundDashes(offset, y) {
        ctx.fillStyle = 'rgba(90,65,40,0.5)';
        for (let x = 0; x <= W; x += 48) {
            const dx = ((x - offset) % (W + 48));
            if (dx < 0) continue;
            ctx.beginPath();
            ctx.arc(dx, y, 3, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    // ===================== DRAW PARTICLES =====================
    function drawParticles() {
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            const alpha = Math.max(0, p.life / p.maxLife);
            ctx.globalAlpha = alpha;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;
    }

    // ===================== HUD =====================
    const hudEl = document.getElementById('hud');
    const scoreValueEl = document.getElementById('score-value');
    const bestValueEl = document.getElementById('best-value');
    const startScreen = document.getElementById('start-screen');
    const gameOverScreen = document.getElementById('game-over-screen');

    function updateHUD() {
        scoreValueEl.textContent = Math.floor(score);
        bestValueEl.textContent = '★ ' + bestScore;
    }

    // ===================== GAME FLOW =====================
    function startGame() {
        initAudio();
        state = STATE.PLAYING;
        score = 0;
        distance = 0;
        gameSpeed = START_SPEED;
        elapsed = 0;
        spawnTimer = 0;
        nextSpawnIn = 1.2;
        obstacles = [];
        particles = [];
        alpaca.runPhase = 0;
        alpaca.tilt = 0;
        resetAlpaca();
        startScreen.style.display = 'none';
        gameOverScreen.style.display = 'none';
        hudEl.style.display = 'flex';
        updateHUD();
    }

    function gameOver() {
        state = STATE.DEAD;
        sfxCrash();

        // shake alpaca
        alpaca.tilt = -8;

        const isNewRecord = score > bestScore;
        if (isNewRecord) {
            bestScore = Math.floor(score);
            localStorage.setItem('ollama_best', String(bestScore));
        }

        document.getElementById('final-score-value').textContent = Math.floor(score);
        document.getElementById('go-best-value').textContent = bestScore;
        const banner = document.getElementById('record-banner');
        if (isNewRecord) {
            banner.style.display = 'block';
        } else {
            banner.style.display = 'none';
        }

        // hide HUD, show game over after brief moment
        hudEl.style.display = 'none';
        setTimeout(function () {
            gameOverScreen.style.display = 'flex';
        }, 650);
    }

    function restartGame() {
        startGame();
    }

    // ===================== MAIN UPDATE =====================
    let lastTime = performance.now();

    function update(dt) {
        if (state !== STATE.PLAYING && state !== STATE.DEAD) return;

        const running = state === STATE.PLAYING;

        // speed ramp applies even during death animation briefly, but mainly while playing
        if (running) {
            elapsed += dt;
            gameSpeed = Math.min(MAX_SPEED, START_SPEED + SPEED_RAMP * elapsed);
            distance += gameSpeed * dt;
            score = distance / 120; // points per distance

            // spawn obstacles
            spawnTimer += dt;
            if (spawnTimer >= nextSpawnIn) {
                spawnObstacle();
                spawnTimer = 0;
                // gap scales with speed for fairness
                const minGap = 0.9, maxGap = 2.4;
                nextSpawnIn = Math.min(maxGap, minGap + (maxGap - minGap) * (START_SPEED / gameSpeed));
            }

            // alpaca physics
            alpaca.vy += GRAVITY * dt;
            alpaca.y += alpaca.vy * dt;

            const groundY = getGroundY();
            if (alpaca.y >= groundY - 46) {
                alpaca.y = groundY - 46;
                if (!alpaca.onGround) {
                    addDust(alpaca.x + alpaca.w * 0.5, groundY);
                }
                alpaca.onGround = true;
                alpaca.vy = 0;
            } else {
                alpaca.onGround = false;
            }

            // jump height: release early for shorter jumps
            if (alpaca.jumpHeld && alpaca.y < groundY - 46) {
                alpaca.vy += 520 * dt; // extra gravity while holding
            }

            // tilt animation during air
            const targetTilt = alpaca.onGround ? 0 : Math.min(6, alpaca.vy / 180);
            alpaca.tilt += (targetTilt - alpaca.tilt) * Math.min(1, dt * 10);

            // run animation
            if (alpaca.onGround) {
                alpaca.runPhase += dt * 14;
            }

            // score sound every ~150px distance
            const newScore = Math.floor(score);
            if (newScore > lastScoreFloor) {
                sfxScore();
                addSparkles(alpaca.x + alpaca.w, alpaca.y - 20);
                lastScoreFloor = newScore;
            }

            updateHUD();
        }

        // move obstacles regardless of state (so they animate on death frame)
        for (let i = obstacles.length - 1; i >= 0; i--) {
            const o = obstacles[i];
            o.x -= gameSpeed * dt;
            if (!o.passed && o.x + o.w < alpaca.x) {
                o.passed = true;
            }
            if (o.x + o.w < -20) obstacles.splice(i, 1);
        }

        // decorative parallax movement
        for (let i = 0; i < clouds.length; i++) clouds[i].x -= clouds[i].speed * dt;
        for (let i = 0; i < birds.length; i++) {
            birds[i].x -= birds[i].speed * dt;
            birds[i].flap += dt * 6;
        }

        // particles
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.life -= dt;
            if (p.life <= 0) particles.splice(i, 1);
        }

        // tilt back to 0 after death animation
        if (!running && alpaca.tilt !== 0) {
            alpaca.tilt += (0 - alpaca.tilt) * Math.min(1, dt * 6);
        }
    }

    let lastScoreFloor = 0;

    // ===================== COLLISION CHECK (during play) =====================
    function checkCollisions() {
        if (state !== STATE.PLAYING) return;
        const ax = alpaca.x, ay = alpaca.y, aw = alpaca.w, ah = alpaca.h;
        for (let i = 0; i < obstacles.length; i++) {
            const o = obstacles[i];
            if (hitTest(ax, ay, aw, ah, o.x, o.y, o.w, o.h)) {
                gameOver();
                return;
            }
        }
    }

    // ===================== MAIN RENDER =====================
    function render() {
        ctx.clearRect(0, 0, W, H);
        drawBackground();
        drawParticles();
        for (let i = 0; i < obstacles.length; i++) drawObstacle(obstacles[i]);
        drawAlpaca();
    }

    // ===================== GAME LOOP =====================
    function loop(now) {
        let dt = (now - lastTime) / 1000;
        lastTime = now;
        if (dt > 0.05) dt = 0.05; // clamp to avoid huge jumps

        update(dt);
        render();

        requestAnimationFrame(loop);
    }

    // ===================== INPUT HANDLING =====================
    function onJumpInput() {
        initAudio();
        if (state === STATE.PLAYING) {
            jump();
        } else if (state === STATE.DEAD) {
            restartGame();
        }
    }

    window.addEventListener('keydown', function (e) {
        if (e.code === 'Space' || e.code === 'ArrowUp' || e.key === ' ') {
            e.preventDefault();
            onJumpInput();
        }
    });

    canvas.addEventListener('mousedown', function (e) { e.preventDefault(); onJumpInput(); });
    canvas.addEventListener('touchstart', function (e) {
        e.preventDefault();
        onJumpInput();
    }, { passive: false });

    // ===================== BUTTONS =====================
    document.getElementById('play-btn').addEventListener('click', function () {
        startGame();
    });
    document.getElementById('retry-btn').addEventListener('click', function () {
        restartGame();
    });

    // hide tap hint once started
    const tapHint = document.getElementById('tap-hint');
    startScreen.addEventListener('pointerdown', function () { tapHint.style.opacity = '0'; }, { passive: true });

    // ===================== INIT =====================
    initDecor();
    initStars();
    resetAlpaca();
    updateHUD();
    requestAnimationFrame(loop);

})();
</script>
</body>
</html>
```

I've built **Ollama's Adventure** — a complete, self-contained endless runner in a single HTML file. Here's what's included:

## 🦙 The Alpaca (hand-drawn on Canvas)
- Fully procedurally drawn with a fluffy white body, dark face mask/muzzle, big eyes with shine, ears, blush cheeks, and a name tag
- **Animated running legs** that swing in sync while grounded
- **Tilts upward** during jumps for a natural arc feel

## 🎮 Gameplay
- Auto-running alpaca; **Spacebar / click / tap to jump** (hold for variable-height jumps)
- Three obstacle types: **rocks, logs, and cacti** — randomly generated from the right
- Speed ramps up continuously (`START_SPEED` → `MAX_SPEED`) with a fairness-based spawn gap that widens as you go faster
- Score based on distance survived; HUD shows live score + best

## 🌄 Parallax Background (4+ layers)
1. **Stars** (slowest, farthest) — twinkling night sky
2. **Sun glow** with radial gradient
3. **Clouds** — drifting at a slow rate
4. **Birds** — mid-distance with flapping wings
5. **Two mountain ranges** — parallax at different speeds
6. **Grass blades + dirt strip** — near layer, fastest scroll

## 🔊 Web Audio SFX (no libraries)
- **Jump**: rising two-note "boing"
- **Scoring**: happy ascending chime arpeggio with sparkle particles
- **Crash**: low thud + descending buzz
- All use short envelopes to stay lighthearted and click-free

## 💾 Persistence & Flow
- High score saved to `localStorage` under `ollama_best`
- **"New High Score!"** banner pulses on records
- Game-over screen with **Play Again** button (also Space/click restarts)

Just save it as an `.html` file and open in any browser — fully responsive for desktop and mobile.

149 t/s, 12858 tokens, 86s
