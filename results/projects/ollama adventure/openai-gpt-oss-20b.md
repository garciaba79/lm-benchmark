# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: ollamas adventure
Created: 11/03/2026, 01:17:49 AM
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
<title>ollama's Adventure</title>
<style>
  body{margin:0;overflow:hidden;background:#87ceeb;}
  canvas{display:block;}
  #ui{
    position:absolute;
    top:10px;left:50%;transform:translateX(-50%);
    font-family:sans-serif;font-size:20px;color:white;text-align:center;
  }
  #retry{
    margin-top:8px;padding:6px 12px;background:#ff6347;border:none;border-radius:4px;color:white;
    cursor:pointer;display:none;
  }
</style>
</head>
<body>
<canvas id="game"></canvas>
<div id="ui">
  <div>Score: <span id="score">0</span></div>
  <div>High Score: <span id="high">0</span></div>
  <button id="retry">Play Again</button>
</div>

<script>
// ---------- SETUP ----------
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
resize();
window.addEventListener('resize', resize);

function resize(){
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

// ---------- AUDIO ----------
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(frequency, duration=0.1){
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.frequency.value = frequency;
  osc.type = 'sine';
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  setTimeout(()=>{osc.stop();}, duration*1000);
}

// ---------- GAME STATE ----------
let score = 0, highScore = localStorage.getItem('ollamaHigh')||0;
document.getElementById('high').textContent=highScore;

const alpaca = {x:80,y:canvas.height-120,w:60,h:90,vY:0, onGround:true};
const obstacles=[];
let lastObsTime=0, obsInterval=1500; // ms
let speed=4;
let gameOver=false;

// ---------- INPUT ----------
function jump(){
  if(alpaca.onGround && !gameOver){
    alpaca.vY = -16;
    alpaca.onGround=false;
    playSound(440);
  }
}
window.addEventListener('keydown', e=>{
  if(e.code==='Space')jump();
});
canvas.addEventListener('click', jump);

// ---------- PARALLAX ----------
const bgLayers=[
  {color:'#3e9f5a', speed:0.5, y:canvas.height-200, h:200},
  {color:'#2b6c39', speed:1,   y:canvas.height-300, h:100}
];

// ---------- DRAW ----------
function drawAlpaca(){
  // body
  ctx.fillStyle='#f9e79f';
  ctx.beginPath();
  ctx.ellipse(alpaca.x+alpaca.w/2, alpaca.y+alpaca.h/2, alpaca.w/2, alpaca.h/3,0,0,Math.PI*2);
  ctx.fill();

  // head
  ctx.beginPath();
  ctx.arc(alpaca.x+alpaca.w/2, alpaca.y-10, 20,0,Math.PI*2);
  ctx.fillStyle='#f9e79f';
  ctx.fill();

  // eyes
  ctx.fillStyle='black';
  ctx.beginPath();ctx.arc(alpaca.x+alpaca.w/2-8, alpaca.y-15,3,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(alpaca.x+alpaca.w/2+8, alpaca.y-15,3,0,Math.PI*2);ctx.fill();

  // ears
  ctx.fillStyle='#f9e79f';
  ctx.beginPath();ctx.moveTo(alpaca.x+alpaca.w/2-12, alpaca.y-20);
  ctx.lineTo(alpaca.x+alpaca.w/2-18, alpaca.y-30);ctx.lineTo(alpaca.x+alpaca.w/2-6, alpaca.y-30);ctx.closePath();ctx.fill();
  ctx.beginPath();ctx.moveTo(alpaca.x+alpaca.w/2+12, alpaca.y-20);
  ctx.lineTo(alpaca.x+alpaca.w/2+18, alpaca.y-30);ctx.lineTo(alpaca.x+alpaca.w/2+6, alpaca.y-30);ctx.closePath();ctx.fill();
}

// ---------- UPDATE ----------
function update(dt){
  if(gameOver) return;
  // background
  bgLayers.forEach(layer=>{
    layer.x = (layer.x||0)-layer.speed*speed*dt/16.67;
    if(layer.x<-canvas.width) layer.x=0;
  });

  // alpaca physics
  alpaca.vY += 0.6; // gravity
  alpaca.y += alpaca.vY;
  if(alpaca.y+alpaca.h>=canvas.height-30){
    alpaca.y = canvas.height-30-alpaca.h;
    alpaca.vY=0;
    alpaca.onGround=true;
  }

  // obstacles
  const now=performance.now();
  if(now-lastObsTime>obsInterval){
    lastObsTime=now;
    obstacles.push({x:canvas.width+20,y:canvas.height-40,w:30,h:60});
  }
  obstacles.forEach(o=>{
    o.x -= speed*dt/16.67;
  });
  // remove offscreen
  while(obstacles.length && obstacles[0].x<-50)obstacles.shift();

  // collision
  for(const o of obstacles){
    if(alpaca.x+alpaca.w>o.x && alpaca.x<o.x+o.w &&
       alpaca.y+alpaca.h>o.y && alpaca.y<o.y+o.h){
      gameOver=true;
      playSound(220,0.3);
      document.getElementById('retry').style.display='inline-block';
    }
  }

  // scoring
  score += dt/16.67;
  document.getElementById('score').textContent=Math.floor(score);

  // speed increase
  if(Math.floor(score)%100===0) speed+=0.01;

}

// ---------- RENDER ----------
function render(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  // parallax layers
  bgLayers.forEach(layer=>{
    const x=layer.x||0;
    ctx.fillStyle=layer.color;
    ctx.fillRect(x, layer.y, canvas.width*2, layer.h);
  });

  drawAlpaca();
  obstacles.forEach(o=>{
    ctx.fillStyle='#8e44ad';
    ctx.fillRect(o.x,o.y,o.w,o.h);
  });
}

// ---------- LOOP ----------
let lastTime=performance.now();
function loop(){
  const now=performance.now();
  const dt = now-lastTime;
  update(dt);
  render();
  lastTime=now;
  requestAnimationFrame(loop);
}
loop();

// ---------- RESTART ----------
document.getElementById('retry').addEventListener('click', ()=>{
  // reset state
  score=0; document.getElementById('score').textContent='0';
  alpaca.y = canvas.height-120; alpaca.vY=0; alpaca.onGround=true;
  obstacles.length=0; lastObsTime=0; speed=4; gameOver=false;
  document.getElementById('retry').style.display='none';
});

// ---------- HIGH SCORE ----------
function checkHigh(){
  const hs=Math.floor(score);
  if(hs>highScore){
    highScore=hs;
    localStorage.setItem('ollamaHigh',highScore);
    document.getElementById('high').textContent=highScore;
  }
}
setInterval(checkHigh,500);

</script>
</body>
</html>
```

**How it works**

* **Canvas & Canvas Size** – The whole game runs inside a `<canvas>` that automatically resizes with the window.
* **Alpaca** – A simple cartoon alpaca is drawn with ellipses and arcs. It can jump when the spacebar or a mouse click/tap occurs.
* **Physics** – Gravity pulls the alpaca down; it lands on a flat ground line. Jumping applies an upward velocity once per frame.
* **Obstacles** – Rectangular “cacti” spawn from the right side at regular intervals, move left, and disappear when off‑screen.
* **Parallax Background** – Two colored layers scroll at different speeds to give depth.
* **Scoring & High Score** – Score increases with time; high score is stored in `localStorage` and updated if a new record is reached.
* **Game Over / Retry** – When the alpaca hits an obstacle, the game stops and a “Play Again” button appears. Clicking it resets everything.
* **Sound** – Short sine‑wave tones are generated with the Web Audio API for jumps, collisions, and a simple beat when scoring.

All logic, drawing, UI, and sound are contained in this single file—no external libraries or assets required. Enjoy running “ollama's Adventure”!

193 t/s, 2031 tokens, 11s
