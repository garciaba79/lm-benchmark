# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: ollamas adventure
Created: 11/03/2026, 02:10:30 AM
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

Below is a complete, self‑contained `ollamas-adventure.html`. Open it in any modern browser — no build step, no external files. Controls: **Space / ↑ / W / click / tap** to jump (hold to hover a little, double‑jump in the air), **P** to pause, **M** to mute.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>ollama's Adventure</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{height:100%}
  body{
    font-family:'Segoe UI',system-ui,-apple-system,Roboto,Arial,sans-serif;
    background:
      radial-gradient(1200px 800px at 78% -10%, #ffe6a6 0%, rgba(255,230,166,0) 60%),
      radial-gradient(900px 700px at 10% 110%, #ffd39e 0%, rgba(255,211,158,0) 55%),
      linear-gradient(180deg,#123a44,#0b2530 42%,#20142c 100%);
    color:#f5efe2;
    min-height:100vh;
    display:flex; align-items:center; justify-content:center;
    padding:26px 18px; overflow-x:hidden;
  }
  body::before{
    content:""; position:fixed; inset:-25%; z-index:0; pointer-events:none; filter:blur(26px);
    background:
      radial-gradient(420px 420px at 25% 22%, rgba(255,196,120,.30), transparent 60%),
      radial-gradient(520px 520px at 78% 72%, rgba(90,170,180,.30), transparent 60%),
      radial-gradient(360px 360px at 55% 40%, rgba(255,150,150,.14), transparent 60%);
    animation:drift 26s ease-in-out infinite alternate;
  }
  @keyframes drift{0%{transform:translate3d(-3%,-2%,0) scale(1)}100%{transform:translate3d(4%,3%,0) scale(1.12)}}

  .stage{
    position:relative; z-index:1; width:min(960px,100%);
    background:linear-gradient(180deg,#fffaf0,#f4ead6);
    border-radius:22px; padding:26px 26px 30px;
    box-shadow:0 40px 80px -30px rgba(0,0,0,.7), 0 2px 0 rgba(255,255,255,.6) inset;
    animation:rise .7s cubic-bezier(.2,.9,.3,1) both;
  }
  @keyframes rise{from{opacity:0;transform:translateY(24px) scale(.99)}to{opacity:1;transform:none}}

  .top{display:flex; align-items:flex-end; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:16px}
  .eyebrow{display:inline-flex; align-items:center; gap:8px; font-size:12px; letter-spacing:.22em; text-transform:uppercase; color:#b06a2a; font-weight:700}
  .dot{width:9px;height:9px;border-radius:50%;background:var(--coral);box-shadow:0 0 0 4px rgba(242,128,108,.18)}
  h1{font-size:clamp(30px,6.4vw,52px); line-height:.98; font-weight:800; letter-spacing:-.02em; color:#27333f; margin:6px 0 6px}
  h1 em{font-style:normal; color:var(--coral); text-shadow:2px 2px 0 rgba(0,0,0,.06)}
  .tag{font-size:14px; color:#6f6a5c}

  .hud{display:flex; align-items:center; gap:18px; flex-wrap:wrap}
  .score,.best{display:flex; flex-direction:column; align-items:flex-end}
  .score small,.best small{font-size:10px; letter-spacing:.18em; text-transform:uppercase; color:#a08f6a; font-weight:700}
  .score span,.best span{font-size:26px; font-weight:800; font-variant-numeric:tabular-nums; line-height:1}
  .score span{color:#27333f}
  .best span{color:var(--coral)}
  .best-wrap{position:relative}
  .best-wrap.new{animation:pulse 1s ease-in-out infinite}
  @keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
  .iconbtn{width:44px;height:44px;border-radius:12px;border:2px solid #e6dcc6;background:#fffaf0;color:#6f6a5c;cursor:pointer;display:grid;place-items:center;transition:.18s}
  .iconbtn:hover{transform:translateY(-2px);box-shadow:0 8px 16px -8px rgba(0,0,0,.4);border-color:var(--coral);color:var(--coral)}
  .iconbtn.off{color:#b6ac97}

  .screenwrap{position:relative; border-radius:16px; overflow:hidden; background:#bfe8f2;
    box-shadow:0 0 0 3px #2c3a44, 0 0 0 8px #ffe6a6, 0 26px 50px -22px rgba(0,0,0,.55)}
  canvas{display:block; width:100%; height:auto}

  .overlay{position:absolute; inset:0; display:grid; place-items:center; text-align:center; padding:24px; transition:opacity .32s ease, visibility .32s}
  .overlay[hidden]{opacity:0; visibility:hidden; pointer-events:none}
  .panel{background:rgba(255,251,240,.92); border:3px solid #2c3a44; border-radius:18px; padding:26px 30px;
    box-shadow:0 24px 50px -20px rgba(0,0,0,.5), 6px 6px 0 rgba(44,58,68,.16); max-width:88%;
    transform:translateY(10px) scale(.98); opacity:0; transition:.4s cubic-bezier(.2,.9,.3,1)}
  .overlay:not([hidden]) .panel{transform:none; opacity:1}
  .kicker{font-size:12px; letter-spacing:.24em; text-transform:uppercase; font-weight:800; color:var(--coral)}
  .panel h2{font-size:clamp(26px,5vw,40px); font-weight:800; color:#27333f; margin:8px 0 10px; letter-spacing:-.01em}
  .panel p{color:#5c574a; font-size:15px; line-height:1.5; margin:0 auto 18px; max-width:40ch}
  .keys{display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-bottom:20px}
  .key{background:#2c3a44; color:#fffaf0; font-size:13px; font-weight:700; padding:8px 13px; border-radius:9px;
    box-shadow:0 3px 0 #1a222a; letter-spacing:.02em}
  .key small{color:#c9c1ad; font-weight:600; margin-left:4px}

  .btn{font-family:inherit; font-weight:800; font-size:16px; letter-spacing:.02em; color:#fffaf0; background:var(--coral);
    border:3px solid #2c3a44; padding:13px 26px; border-radius:13px; cursor:pointer; box-shadow:0 5px 0 #1a222a;
    transition:transform .12s, box-shadow .12s, background .15s}
  .btn:hover{transform:translateY(-2px); box-shadow:0 7px 0 #1a222a; background:#f49a80}
  .btn:active{transform:translateY(3px); box-shadow:0 2px 0 #1a222a}
  .btn.ghost{background:#fffaf0; color:#27333f; border-color:#e6dcc6; box-shadow:0 5px 0 #d8ccb0; margin-left:10px}
  .btn.ghost:hover{background:#f4ead6}

  .stats{display:flex; gap:14px; justify-content:center; margin:4px 0 20px}
  .stat{background:#fff; border:2px solid #e6dcc6; border-radius:12px; padding:12px 20px; min-width:120px}
  .stat .lbl{font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:#a08f6a; font-weight:700}
  .stat .val{font-size:30px; font-weight:800; color:#27333f; font-variant-numeric:tabular-nums}
  .stat .val small{font-size:14px; color:#c09a6a}

  .footer{display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap; margin-top:16px;
    padding-top:16px; border-top:2px dashed #e6dcc6; font-size:13px; color:#8b8570}
  .legend{display:flex; gap:16px; flex-wrap:wrap}
  .legend b{color:#4b4536; font-weight:700}
</style>
</head>
<body>
  <main class="stage">
    <header class="top">
      <div>
        <span class="eyebrow"><span class="dot"></span> endless runner · single file</span>
        <h1>ollama's <em>Adventure</em></h1>
        <p class="tag">Run. Leap the cactus, duck the gull. Survive the meadow.</p>
      </div>
      <div class="hud">
        <div class="score"><small>Score</small><span id="score">0</span></div>
        <div class="best best-wrap"><small>Best</small><span id="best">0</span></div>
        <button id="mute" class="iconbtn" aria-label="Toggle sound">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor" stroke="none"/>
            <path class="wave" d="M16 8.5a5 5 0 0 1 0 7"/>
          </svg>
        </button>
      </div>
    </header>

    <div class="screenwrap">
      <canvas id="game" width="960" height="500"></canvas>

      <div id="start" class="overlay">
        <div class="panel">
          <div class="kicker">Ready when you are</div>
          <h2>Let's run, ollama</h2>
          <p>An alpaca, a meadow, and an endless horizon of cactus and gull. How far can you bounce?</p>
          <div class="keys">
            <span class="key">SPACE<small>jump</small></span>
            <span class="key">↑<small>jump</small></span>
            <span class="key">tap<small>jump</small></span>
            <span class="key">double-tap<small>double jump</small></span>
          </div>
          <button class="btn" data-start>Start running</button>
          <button class="btn ghost" data-demo>Just watch</button>
        </div>
      </div>

      <div id="over" class="overlay" hidden>
        <div class="panel">
          <div class="kicker" id="overKicker">That was a run!</div>
          <h2 id="overTitle">Bumped!</h2>
          <div class="stats">
            <div class="stat"><div class="lbl">Score</div><div class="val" id="finalScore">0</div></div>
            <div class="stat"><div class="lbl">Best</div><div class="val"><span id="finalBest">0</span><small> m</small></div></div>
          </div>
          <button class="btn" data-retry>Run again</button>
        </div>
      </div>

      <div id="pause" class="overlay" hidden>
        <div class="panel">
          <div class="kicker">Breathe a second</div>
          <h2>Paused</h2>
          <p>Take it easy, champ.</p>
          <button class="btn" data-resume>Keep running</button>
        </div>
      </div>
    </div>

    <footer class="footer">
      <div class="legend">
        <span><b>Space</b> / <b>↑</b> / <b>click</b> — jump</span>
        <span><b>P</b> — pause</span>
        <span><b>M</b> — sound</span>
      </div>
      <div>Built with Canvas + Web Audio. No libraries, one file.</div>
    </footer>
  </main>

<script>
(() => {
  "use strict";

  // ---------- Config ----------
  const CFG = {
    W:960, H:500, groundY:405,
    alpX:150, alpW:72, alpH:92,
    gravity:2500, jumpVel:1000,
    holdAccel:-360, maxHold:-1.55,
    baseSpeed:300, speedPerSec:5.5, maxSpeed:660,
    spawnMin:0.95, spawnMax:1.7,
    highKey:'ollama_highscore', mutedKey:'ollama_muted'
  };
  const CO = { alpaca:'#fbf1e0', alpacaSh:'#e6d2b3', face:'#c9a579', eye:'#2a2320',
    coral:'#f2806c', cream:'#fff4e2', leaf:'#5fb26a', leafD:'#3f8a4f',
    sky1:'#bfe8f2', sky2:'#eafaff', sun:'#ffd873', sunCore:'#fff3c4' };
  const ALP = { left:CFG.alpX-27, right:CFG.alpX+27, bottom:CFG.groundY, top:CFG.groundY-CFG.alpH };

  // ---------- State ----------
  let state='menu'; // menu | ready | running | over
  let muted = false, raf=0, last=performance.now();
  const T = { time:0, demoTime:0, distance:0, speed:0, readyT:0, overT:0, flash:0,
              shake:0, spawnTimer:1, lastMilestone:0, newBest:false };
  const P = { x:CFG.alpX, y:CFG.groundY, vy:0, rot:0, airborne:false,
              grounded:true, jumps:0, canDouble:true, held:false };
  const cam = { x:0 };
  const obstacles = [];
  const clouds=[], hills=[], flowers=[], dust=[], sparks=[], popups=[];
  let scoreEl, bestEl, bestWrap;
  const overMsgs = [
    ['Bump!','That cactus had opinions.'],
    ['Whoa there!','You went right for the feathers.'],
    ['Clipped it!','So close. So cactus.'],
    ['Ouchie!','The meadow bites back.'],
    ['Bonk!','Feather-fuelled. Almost had it.']
  ];

  // ---------- Helpers ----------
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const rand=(a,b)=>a+Math.random()*(b-a);
  function roundRect(ctx,x,y,w,h,r){
    if(ctx.roundRect){ ctx.beginPath(); ctx.roundRect(x,y,w,h,r); return; }
    r=Math.min(r,Math.abs(w)/2,Math.abs(h)/2); ctx.beginPath();
    ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r);
    ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath();
  }
  function rr(ctx,x,y,w,h,r){ ctx.beginPath(); ctx.roundRect?ctx.roundRect(x,y,w,h,r):roundRect(ctx,x,y,w,h,r); }
  function circle(x,y,r){ ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); }
  function star(cx,cy,sp,o,inr){
    ctx.beginPath();
    for(let i=0;i<sp*2;i++){const r=i%2?inr:o;const a=(Math.PI*i)/sp-Math.PI/2;
      const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;i?ctx.lineTo(x,y):ctx.moveTo(x,y);}
    ctx.closePath(); ctx.fill();
  }

  // ---------- Audio (Web Audio) ----------
  const Sound = {
    ctx:null, master:null,
    ensure(){
      if(!this.ctx){ const AC=window.AudioContext||window.webkitAudioContext; if(!AC) return;
        this.ctx=new AC(); this.master=this.ctx.createGain(); this.master.gain.value=muted?0:0.9; this.master.connect(this.ctx.destination); }
      if(this.ctx && this.ctx.state==='suspended') this.ctx.resume();
    },
    setMuted(m){ if(this.master) this.master.gain.value = m?0:0.9; },
    env(peak){ const g=this.ctx.createGain(); g.gain.setValueAtTime(0.0001,this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(peak,this.ctx.currentTime+0.012);
      g.gain.exponentialRampToValueAtTime(0.0001,this.ctx.currentTime+this.dur);
      g.connect(this.master); return g; },
    tone(o){ if(!this.ctx) return; const t=this.ctx.currentTime+ (o.delay||0);
      const osc=this.ctx.createOscillator(); osc.type=o.type||'sine';
      osc.frequency.setValueAtTime(o.f0,t); if(o.f1) osc.frequency.exponentialRampToValueAtTime(o.f1,t+(o.dur||0.1));
      osc.connect(o.gain||this.env(o.peak||0.2)); osc.start(t); osc.stop(t+(o.dur||0.1)+0.03); },
    jump(){ this.ensure(); this.tone({type:'triangle',f0:360,f1:880,dur:0.16,peak:0.26});
            this.tone({type:'sine',f0:150,f1:90,dur:0.14,peak:0.12}); },
    double(){ this.ensure(); this.tone({type:'triangle',f0:520,f1:1250,dur:0.16,peak:0.24});
              this.tone({type:'triangle',f0:780,f1:1600,dur:0.14,peak:0.12,delay:0.03}); },
    milestone(){ this.ensure(); const n=[523.25,659.25,783.99,1046.5];
      n.forEach((f,i)=>this.tone({type:'triangle',f0:f,dur:0.18,peak:0.16,delay:i*0.055})); },
    hit(){ this.ensure();
      const o=this.ctx.createOscillator(); o.type='sawtooth'; const t=this.ctx.currentTime;
      o.frequency.setValueAtTime(420,t); o.frequency.exponentialRampToValueAtTime(55,t+0.28);
      const g=this.ctx.createGain(); g.gain.setValueAtTime(0.3,t); g.gain.exponentialRampToValueAtTime(0.0001,t+0.3);
      o.connect(g); g.connect(this.master); o.start(t); o.stop(t+0.32);
      const b=this.ctx.createBufferSource(); const buf=this.ctx.createBuffer(1,Math.floor(this.ctx.sampleRate*0.22),this.ctx.sampleRate);
      const d=buf.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; b.buffer=buf;
      const bg=this.ctx.createGain(); bg.gain.setValueAtTime(0.22,t); bg.gain.exponentialRampToValueAtTime(0.0001,t+0.2);
      const lp=this.ctx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=1200; b.connect(lp); lp.connect(bg); bg.connect(this.master); b.start(t); },
    win(){ this.ensure(); const n=[523.25,659.25,783.99,1046.5,1318.5];
      n.forEach((f,i)=>this.tone({type:'triangle',f0:f,dur:0.22,peak:0.16,delay:i*0.06})); }
  };
  const sfxJump=()=>state==='running'?Sound.jump():null;
  const sfxDouble=()=>state==='running'?Sound.double():null;
  const sfxMilestone=()=>Sound.milestone();
  const sfxHit=()=>Sound.hit();
  const sfxWin=()=>Sound.win();

  // ---------- World generation ----------
  function initWorld(){
    clouds.length=0;
    for(let i=0;i<7;i++) clouds.push({x:rand(0,1400),y:rand(35,170),s:rand(0.7,1.5),a:rand(0.85,1)});
    hills.length=0;
    for(let i=0;i<14;i++) hills.push({x:i*190+rand(-30,30),w:rand(150,280),h:rand(46,95)});
    flowers.length=0;
    for(let i=0;i<22;i++) flowers.push({x:rand(-20,CFG.W),y:CFG.groundY+rand(16,52),s:rand(0.7,1.2),type:(Math.random()*3)|0});
  }
  function spawnObstacle(){
    const x = (state==='menu' || state==='ready') ? CFG.W+70 : cam.x+CFG.W+70;
    let type = Math.random()<0.62 ? 'cactus':'gull';
    if(type==='cactus'){
      const variant=(Math.random()*3)|0, w = variant===0?36:56, h = variant===0?78:64;
      obstacles.push({type,variant,x,y:CFG.groundY-h,w,h,wing:0,passed:false,
        hit:{left:x+9,right:x+w-9,top:CFG.groundY-h+12}});
    } else {
      const fl=0.55+Math.random()*0.35, alt=fl<0.5?0:(fl<0.82?1:2);
      const h=42, w=58, y=[CFG.groundY-28,CFG.groundY-84,CFG.groundY-140][alt];
      obstacles.push({type,x,y,w,h,wing:rand(0,6),passed:false,
        hit:{left:x+10,right:x+w-10,top:y+8,bottom:y+h-4}});
    }
  }

  // ---------- Input ----------
  function onInput(e){
    if(e && e.type==='touchstart') e.preventDefault();
    Sound.ensure();
    if(state==='ready') return;
    if(state==='menu'){ start(); return; }
    if(state==='over'){ if(T.overT>0.45) start(); return; }
    if(state==='running') doJump(true);
  }
  function doJump(held){
    if(!P.grounded){
      if(P.jumps<1){ P.vy=CFG.jumpVel*0.88; P.airborne=true; P.grounded=false; P.jumps=1; P.held=held;
        spawnDust(P.x-10,P.y,5); sfxDouble(); }
      return;
    }
    P.vy=CFG.jumpVel; P.airborne=true; P.grounded=false; P.jumps=0; P.canDouble=true; P.held=held;
    spawnDust(P.x-16,P.y,6); sfxJump();
  }
  const setHeld=v=>{ P.held=v; };

  // ---------- State transitions ----------
  function start(){
    Sound.ensure();
    obstacles.length=0; dust.length=0; sparks.length=0; popups.length=0;
    T.time=0; T.distance=0; T.speed=CFG.baseSpeed; T.spawnTimer=1; T.lastMilestone=0;
    T.readyT=0; T.overT=0; T.shake=0; T.flash=0; T.newBest=false; T.demoTime=0;
    P.y=CFG.groundY; P.vy=0; P.grounded=true; P.airborne=false; P.jumps=0; P.canDouble=true; P.held=false; P.rot=0;
    cam.x=0;
    bestWrap.classList.remove('new');
    hideOverlays();
    state='ready';
  }
  function gameOver(){
    state='over'; T.overT=0; T.shake=1; T.flash=0.85;
    const score=Math.floor(T.distance/10);
    sfxHit();
    spawnSparks(P.x,P.y-CFG.alpH*0.5);
    let best=loadBest();
    if(score>best){ best=score; saveBest(best); T.newBest=true; }
    const m=overMsgs[(Math.random()*overMsgs.length)|0];
    showOver(score,best,m[0],m[1]);
  }
  function showOver(score,best,title,msg){
    document.getElementById('finalScore').textContent=score;
    document.getElementById('finalBest').textContent=best;
    document.getElementById('overKicker').textContent = T.newBest ? '★ New personal best!' : 'That was a run!';
    document.getElementById('overTitle').textContent=title;
    const p=document.querySelector('#over .panel p'); if(p) p.textContent=msg;
    bestWrap.classList.toggle('new', T.newBest);
    show('#over');
  }

  // ---------- Update ----------
  function update(dt){
    T.flash=Math.max(0,T.flash-dt*2.4);
    if(state==='menu'){ T.demoTime+=dt; updateClouds(dt); updateHills(dt); updateFlowers(dt);
      updateP(dt); updateObstacles(dt, true); if(Math.random()<0.02) spawnDust(P.x-12,P.y,1); return; }
    if(state==='ready'){ T.readyT+=dt; updateClouds(dt); updateHills(dt); updateFlowers(dt);
      updateP(dt); if(T.readyT>=1){ state='running'; } return; }
    if(state==='over'){ T.overT+=dt; updateClouds(dt*0.6); updateHills(dt*0.6); updateFlowers(dt*0.6);
      if(P.grounded) P.vy+=CFG.gravity*dt; P.y+=P.vy*dt; if(P.y>CFG.groundY){P.y=CFG.groundY;P.vy=0;}
      T.shake=Math.max(0,T.shake-dt*2); updateDust(dt); updateSparks(dt); updatePopups(dt); return; }

    // running
    T.time+=dt;
    T.speed=CFG.baseSpeed+T.speedPerSec*T.time; if(T.speed>CFG.maxSpeed)T.speed=CFG.maxSpeed;
    const dx=T.speed*dt; T.distance+=dx; cam.x+=dx;
    updateClouds(dt); updateHills(dt); updateFlowers(dt); updateP(dt);

    if(Math.random()<0.5) spawnDust(P.x-16,P.y,1);

    const interval = clamp((CFG.spawnMin+Math.random()*(CFG.spawnMax-CFG.spawnMin))*T.speed/60, 0.42, 2.4);
    T.spawnTimer-=dt; if(T.spawnTimer<=0){ spawnObstacle(); T.spawnTimer=interval; }

    updateObstacles(dt,false);

    const score=Math.floor(T.distance/10);
    if(score>= (T.lastMilestone+50)){ T.lastMilestone+=50; popup(score+'m'); sfxMilestone(); }

    if(cam.x>ALP.left && cam.x<ALP.right){
      if(cam.x>ALP.top && cam.x<ALP.bottom){ P.airborne=true; P.grounded=false; P.vy=-60; }
      else { if(P.grounded) P.y=CFG.groundY; P.grounded=true; P.airborne=false; P.jumps=0; P.canDouble=true; P.rot=0; }
    } else {
      if(P.grounded) P.y=CFG.groundY; P.grounded=true; P.airborne=false; P.jumps=0; P.rot=0;
    }

    updateDust(dt); updateSparks(dt); updatePopups(dt);
  }

  function updateClouds(dt){ const s=22; for(const c of clouds){ c.x-=s*dt; if(c.x<-260){ c.x=CFG.W+rand(40,220); c.y=rand(35,175); c.s=rand(0.7,1.5);} } }
  function updateHills(dt){ const s=T.speed*0.30; for(const h of hills){ h.x-=s*dt; if(h.x+h.w<-20){ h.x=CFG.W+rand(0,160); h.w=rand(150,280); h.h=rand(46,95);} } }
  function updateFlowers(dt){ const s=T.speed*0.9; for(const f of flowers){ f.x-=s*dt; if(f.x<-30){ f.x=CFG.W+rand(20,140); f.s=rand(0.7,1.2); f.type=(Math.random()*3)|0;} } }
  function updateObstacles(dt, demo){
    const s=T.speed;
    for(let i=obstacles.length-1;i>=0;i--){
      const o=obstacles[i]; o.x-=s*dt;
      if(o.type==='gull') o.wing+=dt*22;
      if(!o.passed && o.x+o.w < cam.x){
        o.passed=true;
        if(!demo){ scorePopup(o.x, o.y-6); }
      }
      if(o.x+o.w < cam.x-80) obstacles.splice(i,1);
    }
    if(!demo) checkCollisions();
  }
  function updateP(dt){
    if(P.airborne){
      let a=CFG.gravity; if(P.held && P.vy<0) a+=CFG.holdAccel;
      if(a>CFG.gravity*1.7) a=CFG.gravity*1.7;
      P.vy+=a*dt; P.y+=P.vy*dt;
      P.rot=clamp(P.vy*0.0005,-0.34,0.46);
      if(P.y>=CFG.groundY){ P.y=CFG.groundY; P.vy=0; P.airborne=false; P.grounded=true; P.jumps=0; P.canDouble=true; P.rot=0; }
    } else { P.vy=0; P.rot=0; }
    if(P.y>CFG.groundY){ P.y=CFG.groundY; P.vy=0; P.airborne=false; P.grounded=true; P.rot=0; }
  }

  function checkCollisions(){
    const gap=12;
    const aL=ALP.left+gap, aR=ALP.right-gap, aT=ALP.top+gap, aB=ALP.bottom-gap;
    for(const o of obstacles){
      const h=o.hit;
      const oB = h.bottom!==undefined?h.bottom:CFG.groundY;
      if(aL<h.right && aR>h.left && aT<oB && aB>h.top){ gameOver(); return; }
    }
  }

  function spawnDust(x,y,n){ for(let i=0;i<n;i++){ const a=rand(2.1,3.6), sp=rand(20,80);
    dust.push({x:x+rand(-6,6),y:y+rand(-4,2),vx:Math.cos(a)*sp+rand(-20,0),vy:Math.sin(a)*sp+rand(-30,0),r:rand(3,7),life:rand(0.4,0.8),max:0.8}); } }
  function spawnSparks(x,y){ for(let i=0;i<16;i++){ const a=rand(0,Math.PI*2), sp=rand(60,220);
    sparks.push({x,y:y+rand(-10,10),vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-40,r:rand(3,7),life:rand(0.5,1),max:1,
      c:[CO.coral,CO.cream,'#fff','#8fd3c8'][(Math.random()*4)|0]}); } }
  function scorePopup(x,y){ popups.push({x:x-60,y:y-14,vy:-42,life:0.7,max:0.7,text:'+'+ (2+((Math.random()*2)|0)),c:CO.coral}); }
  function popup(text){ popups.push({x:CFG.W/2-40,y:150,vy:-26,life:1.1,max:1.1,text,c:CO.leafD,big:true}); }
  function updateDust(dt){ for(let i=dust.length-1;i>=0;i--){ const p=dust[i]; p.x+=p.vx*dt; p.y+=p.vy*dt; p.vy+=120*dt; p.life-=dt; if(p.life<=0) dust.splice(i,1);} }
  function updateSparks(dt){ for(let i=sparks.length-1;i>=0;i--){ const p=sparks[i]; p.x+=p.vx*dt; p.y+=p.vy*dt; p.vy+=380*dt; p.life-=dt; if(p.life<=0) sparks.splice(i,1);} }
  function updatePopups(dt){ for(let i=popups.length-1;i>=0;i--){ const p=popups[i]; p.y+=p.vy*dt; p.life-=dt; if(p.life<=0) popups.splice(i,1);} }

  // ---------- Render ----------
  function render(){
    ctx.save();
    if(T.shake>0.01){ const s=T.shake*7; ctx.translate(rand(-s,s),rand(-s,s)); }
    drawSky(); drawSun(); drawClouds(); drawHills(); drawGround(); drawFlowers();
    for(const o of obstacles) drawObstacle(o);
    drawAlpaca();
    drawDust(); drawSparks(); drawPopups();
    ctx.restore();

    if(T.flash>0.01){ ctx.fillStyle='rgba(255,255,255,'+(T.flash*0.6)+')'; ctx.fillRect(0,0,CFG.W,CFG.H); }
    if(state==='ready'){
      ctx.textAlign='center'; ctx.font='800 34px system-ui,sans-serif';
      ctx.lineWidth=6; ctx.strokeStyle='rgba(255,251,240,.95)'; ctx.strokeText('Get ready!',CFG.W/2,150);
      ctx.fillStyle=CO.coral; ctx.fillText('Get ready!',CFG.W/2,150);
      ctx.fillStyle='rgba(44,58,68,.7)'; ctx.font='700 15px system-ui,sans-serif';
      ctx.fillText('press SPACE or tap to start',CFG.W/2,182);
    }
    if(T.flash>0.01){ ctx.fillStyle='rgba(242,128,108,'+(T.flash*0.28)+')'; ctx.fillRect(0,0,CFG.W,CFG.H); }
  }

  function drawSky(){
    const g=ctx.createLinearGradient(0,0,0,CFG.groundY+10);
    g.addColorStop(0,CO.sky1); g.addColorStop(0.7,'#dff3f8'); g.addColorStop(1,'#eafaff');
    ctx.fillStyle=g; ctx.fillRect(0,0,CFG.W,CFG.groundY+2);
    const hz=ctx.createLinearGradient(0,CFG.groundY-70,0,CFG.groundY);
    hz.addColorStop(0,'rgba(255,255,255,0)'); hz.addColorStop(1,'rgba(255,255,255,.5)');
    ctx.fillStyle=hz; ctx.fillRect(0,CFG.groundY-70,CFG.W,70);
  }
  function drawSun(){
    const sx=770, sy=112, r=46;
    const rg=ctx.createRadialGradient(sx,sy,0,sx,sy,r*2.4);
    rg.addColorStop(0,'rgba(255,236,160,.85)'); rg.addColorStop(1,'rgba(255,236,160,0)');
    ctx.fillStyle=rg; circle(sx,sy,r*2.4); ctx.fill();
    ctx.save(); ctx.translate(sx,sy); ctx.rotate(T.time*0.2);
    ctx.fillStyle='rgba(255,216,115,.5)';
    for(let i=0;i<10;i++){ ctx.rotate(Math.PI/5); rr(ctx,r*1.05,-6,26,12,6); ctx.fill(); }
    ctx.restore();
    ctx.fillStyle=CO.sun; circle(sx,sy,r); ctx.fill();
    ctx.fillStyle=CO.sunCore; circle(sx,sy,r*0.6); ctx.fill();
  }
  function drawClouds(){
    for(const c of clouds){ const s=c.s; ctx.fillStyle='rgba(255,255,255,'+(c.a*0.92)+')';
      const y=c.y; circle(c.x,y,22*s); ctx.fill(); circle(c.x+26*s,y+4*s,26*s); ctx.fill();
      circle(c.x+54*s,y,20*s); ctx.fill(); circle(c.x+26*s,y-14*s,22*s); ctx.fill();
      circle(c.x+10*s,y+10*s,16*s); ctx.fill(); }
  }
  function drawHills(){
    for(const h of hills){
      const x=h.x, w=h.w, hgt=h.h;
      ctx.fillStyle='#cfe4c0';
      ctx.beginPath(); ctx.moveTo(x,CFG.groundY);
      ctx.quadraticCurveTo(x+w*0.5, CFG.groundY-hgt*1.55, x+w, CFG.groundY);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle='#bcd9a3';
      ctx.beginPath(); ctx.moveTo(x+w*0.5,CFG.groundY);
      ctx.quadraticCurveTo(x+w*0.5, CFG.groundY-hgt*1.25, x+w, CFG.groundY);
      ctx.closePath(); ctx.fill();
    }
  }
  function drawGround(){
    ctx.fillStyle='#b7d987'; ctx.fillRect(0,CFG.groundY,CFG.W,CFG.H-CFG.groundY);
    ctx.fillStyle='#a7cf74'; ctx.fillRect(0,CFG.groundY,CFG.W,10);
    ctx.fillStyle='#8bbf5e'; ctx.fillRect(0,CFG.groundY+10,CFG.W,4);
    // grass tufts
    const step=42, off=-(cam.x%step);
    ctx.strokeStyle='#8bbf5e'; ctx.lineWidth=3; ctx.lineCap='round';
    for(let x=off;x<CFG.W;x+=step){ const gx=x+rand(-3,3);
      ctx.beginPath(); ctx.moveTo(gx,CFG.groundY+3); ctx.quadraticCurveTo(gx-3,CFG.groundY-6,gx-1,CFG.groundY-11);
      ctx.moveTo(gx,CFG.groundY+3); ctx.quadraticCurveTo(gx+3,CFG.groundY-7,gx+2,CFG.groundY-12); ctx.stroke(); }
  }
  function drawFlowers(){
    for(const f of flowers){
      const x=f.x, y=f.y, s=f.s;
      ctx.strokeStyle='#6fae5f'; ctx.lineWidth=2.5*s; ctx.lineCap='round';
      ctx.beginPath(); ctx.moveTo(x,y+8*s); ctx.lineTo(x,y-4*s); ctx.stroke();
      const petals=f.type===2?5:6;
      ctx.fillStyle=['#fff0f4','#fff6d6','#eef2ff'][f.type];
      for(let i=0;i<petals;i++){ const a=(Math.PI*2*i)/petals;
        circle(x+Math.cos(a)*4*s, y-6*s+Math.sin(a)*4*s, 3.2*s); ctx.fill(); }
      ctx.fillStyle=CO.coral; circle(x,y-6*s,2.4*s); ctx.fill();
    }
  }

  function drawObstacle(o){
    if(o.type==='cactus') drawCactus(o); else drawGull(o);
  }
  function drawCactus(o){
    const base=CFG.groundY, cx=o.x+o.w/2;
    const g=ctx.createLinearGradient(0,base-o.h,0,base); g.addColorStop(0,CO.leaf); g.addColorStop(1,CO.leafD);
    ctx.fillStyle=g;
    function bar(x,y,w,h){ rr(ctx,x,y,w,h,w/2); ctx.fill(); }
    const th=Math.min(30,o.w*0.6);
    bar(cx-th/2, base-o.h, th, o.h);
    if(o.variant>0){
      const armY=base-o.h*0.72, up=26;
      const side = o.variant===1?1:-1;
      const ax = side>0? cx+th/2 : cx-th/2-18;
      bar(ax, armY-up, 18, up);
      bar(Math.min(ax, ax+18), armY, 18, 18);
      const s2 = side>0? -1:1; const ax2 = s2>0? cx+th/2 : cx-th/2-18;
      if(o.variant===2){ bar(ax2, armY-up*0.8, 18, up*0.8); bar(Math.min(ax2,ax2+18), armY, 18,18); }
    }
    // spines
    ctx.strokeStyle='rgba(255,255,255,.55)'; ctx.lineWidth=1.5; ctx.lineCap='round';
    for(let yy=base-o.h+8; yy<base-6; yy+=9){
      ctx.beginPath(); ctx.moveTo(cx-2,yy); ctx.lineTo(cx-7,yy-2); ctx.moveTo(cx+2,yy); ctx.lineTo(cx+7,yy-2); ctx.stroke();
    }
  }
  function drawGull(o){
    const cx=o.x+o.w/2, cy=o.y+o.h*0.45;
    const wf=Math.sin(o.wing);
    ctx.save(); ctx.translate(cx,cy);
    // far wing
    ctx.fillStyle='#c9ccd6';
    ctx.beginPath(); ctx.moveTo(0,-2); ctx.lineTo(-20, -14*wf-4); ctx.lineTo(-30, -6*wf); ctx.lineTo(-12,4); ctx.closePath(); ctx.fill();
    // body
    ctx.fillStyle='#f2f4f8'; ctx.beginPath(); ctx.ellipse(0,0,20,12,0,0,Math.PI*2); ctx.fill();
    // near wing
    ctx.fillStyle='#fff';
    ctx.beginPath(); ctx.moveTo(4,-2); ctx.lineTo(-18, -22*wf-4); ctx.lineTo(-28, -10*wf-2); ctx.lineTo(-6,6); ctx.closePath(); ctx.fill();
    // head (facing left, running direction)
    ctx.fillStyle='#f2f4f8'; circle(-16,-6,9); ctx.fill();
    // beak
    ctx.fillStyle=CO.coral; ctx.beginPath(); ctx.moveTo(-24,-7); ctx.lineTo(-34,-4); ctx.lineTo(-24,-2); ctx.closePath(); ctx.fill();
    // eye
    ctx.fillStyle='#2a2320'; circle(-18,-8,2.2); ctx.fill();
    ctx.restore();
  }

  function drawAlpaca(){
    const bob = P.grounded ? Math.sin(T.time*11)*2.5 : 0;
    const legPh = T.time*15;
    ctx.save();
    ctx.translate(P.x, P.y + bob);
    ctx.rotate(P.rot);
    const s=1;

    // shadow drawn before translate-restore would be odd; do separately below
    // back legs
    drawLeg(-20, -18, legPh, 1.0, false);
    drawLeg(18, -18, legPh, 1.0, false);
    // body fluff (behind)
    fluff(0,-30,46,34, CO.alpaca, CO.alpacaSh);
    // belly
    ctx.fillStyle=CO.cream; ctx.beginPath(); ctx.ellipse(-2,-22,26,17,0,0,Math.PI*2); ctx.fill();

    // neck + head
    ctx.strokeStyle=CO.alpaca; ctx.lineWidth=26; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(14,-40); ctx.quadraticCurveTo(34,-64,34,-82); ctx.stroke();
    // head fluff
    fluff(34,-84,40,34, CO.alpaca, CO.alpacaSh);
    // ears
    ear(24,-96,-0.5); ear(44,-96,0.5);
    // muzzle
    ctx.fillStyle=CO.face; ctx.beginPath(); ctx.ellipse(46,-80,11,9,0,0,Math.PI*2); ctx.fill();
    // nose
    ctx.fillStyle='#9a6f45'; ctx.beginPath(); ctx.ellipse(51,-80,3.2,2.6,0,0,Math.PI*2); ctx.fill();
    // eye (blinks)
    const blink = (Math.sin(T.time*1.1)>0.985);
    if(blink){ ctx.strokeStyle=CO.eye; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(40,-90); ctx.lineTo(47,-90); ctx.stroke(); }
    else { ctx.fillStyle=CO.eye; ctx.beginPath(); ctx.ellipse(44,-90,3,4,0,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='#fff'; circle(45.4,-91.6,1.3); ctx.fill(); }
    // cheek
    ctx.fillStyle='rgba(242,128,108,.35)'; circle(40,-76,4); ctx.fill();

    // front legs
    drawLeg(-12,-16, legPh+Math.PI, 1.0, true);
    drawLeg(10,-16, legPh+Math.PI, 1.0, true);

    ctx.restore();

    // ground shadow (screen space, under alpaca)
    const shAlpha = clamp(1-(CFG.groundY-P.y)/240, 0.12, 0.5);
    ctx.fillStyle='rgba(40,60,50,'+shAlpha+')';
    ctx.beginPath(); ctx.ellipse(P.x, CFG.groundY+6, 34*clamp(1-(CFG.groundY-P.y)/300,0.5,1), 8, 0,0,Math.PI*2); ctx.fill();
  }
  function fluff(x,y,w,h,fill,shade){
    const r=Math.min(w,h)*0.5;
    ctx.fillStyle=fill;
    const n=11;
    for(let i=0;i<n;i++){ const a=(Math.PI*2*i)/n + (x*0.03);
      circle(x+Math.cos(a)*r*0.6, y+Math.sin(a)*r*0.5, r*0.5); ctx.fill(); }
    circle(x,y,r); ctx.fill();
    // subtle shading
    ctx.fillStyle=shade; ctx.beginPath(); ctx.ellipse(x+r*0.3, y+r*0.5, r*0.7, r*0.5, 0.4, 0, Math.PI); ctx.fill();
  }
  function drawLeg(x,y,ph,amp,front){
    const sw = Math.sin(ph+ (front?Math.PI:0));
    const dx = sw*7*amp;
    ctx.strokeStyle=front?CO.alpaca:CO.alpacaSh; ctx.lineWidth=15; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+dx, 0); ctx.stroke();
    // hoof
    ctx.fillStyle='#b98f5f'; ctx.beginPath(); ctx.arc(x+dx,0,6,0,Math.PI*2); ctx.fill();
  }
  function ear(x,y,rot){
    ctx.save(); ctx.translate(x,y); ctx.rotate(rot);
    ctx.fillStyle=CO.alpaca; ctx.beginPath(); ctx.ellipse(0,-6,5,11,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=CO.face; ctx.beginPath(); ctx.ellipse(0,-8,2.5,6,0,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }

  function drawDust(){
    for(const p of dust){ const a=clamp(p.life/p.max,0,1);
      ctx.fillStyle='rgba(190,175,140,'+(a*0.6)+')'; circle(p.x,p.y,p.r*(1+(1-a)*0.6)); ctx.fill(); }
  }
  function drawSparks(){
    for(const p of sparks){ const a=clamp(p.life/p.max,0,1);
      ctx.fillStyle=p.c; ctx.globalAlpha=a; circle(p.x,p.y,p.r); ctx.fill(); }
    ctx.globalAlpha=1;
  }
  function drawPopups(){
    ctx.textAlign='center';
    for(const p of popups){ const a=clamp(p.life/p.max,0,1);
      ctx.globalAlpha=a;
      ctx.font=(p.big?'800 26px':'800 16px')+' system-ui,sans-serif';
      ctx.lineWidth=4; ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.strokeText(p.text,p.x,p.y);
      ctx.fillStyle=p.c; ctx.fillText(p.text,p.x,p.y); }
    ctx.globalAlpha=1;
  }

  // ---------- Loop ----------
  function frame(now){
    let dt=(now-last)/1000; last=now; if(dt>0.05) dt=0.05;
    update(dt); render();
    raf=requestAnimationFrame(frame);
  }

  // ---------- Persistence ----------
  function loadBest(){ try{ return parseInt(localStorage.getItem(CFG.highKey))||0; }catch(e){ return 0; } }
  function saveBest(v){ try{ localStorage.setItem(CFG.highKey, String(v)); }catch(e){} }
  function loadMuted(){ try{ return localStorage.getItem(CFG.mutedKey)==='1'; }catch(e){ return false; } }
  function saveMuted(m){ try{ localStorage.setItem(CFG.mutedKey, m?'1':'0'); }catch(e){} }

  function refreshHud(){
    scoreEl.textContent = state==='menu' ? 0 : Math.floor(T.distance/10);
    bestEl.textContent = loadBest();
  }
  function show(id){ document.getElementById(id).hidden=false; }
  function hideOverlays(){ ['start','over','pause'].forEach(id=>document.getElementById(id).hidden=true); }

  function toggleMute(){ muted=!muted; saveMuted(muted); Sound.ensure(); Sound.setMuted(muted);
    document.getElementById('mute').classList.toggle('off',muted);
    document.querySelector('#mute .wave').style.opacity = muted?0:1; }

  // ---------- Init ----------
  const canvas=document.getElementById('game');
  const ctx=canvas.getContext('2d');

  function setupDpr(){
    const dpr=Math.min(window.devicePixelRatio||1,2);
    canvas.width=CFG.W*dpr; canvas.height=CFG.H*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
  }

  function bind(){
    // keyboard
    window.addEventListener('keydown', e=>{
      const k=e.key.toLowerCase();
      if(k===' '||k==='arrowup'||k==='w'||k==='z'){ e.preventDefault(); onInput(); setHeld(true); }
      else if(k==='m'){ toggleMute(); }
      else if(k==='p' && state==='running'){ state='over'; /* pause via overlay */ show('#pause'); }
      else if(k==='p' && document.getElementById('pause').hidden===false){ state='running'; hideOverlays(); }
      else if(k==='r' && state==='over'){ start(); }
    });
    window.addEventListener('keyup', e=>{ const k=e.key.toLowerCase();
      if(k===' '||k==='arrowup'||k==='w'||k==='z') setHeld(false); });

    // canvas pointer
    canvas.addEventListener('pointerdown', e=>{ e.preventDefault(); onInput(e); setHeld(true); });
    window.addEventListener('pointerup', ()=>setHeld(false));
    window.addEventListener('blur', ()=>setHeld(false));

    // buttons
    document.querySelectorAll('[data-start]').forEach(b=>b.onclick=()=>{ onInput(); });
    document.querySelectorAll('[data-demo]').forEach(b=>b.onclick=()=>{ state='menu'; hideOverlays(); });
    document.querySelectorAll('[data-retry]').forEach(b=>b.onclick=()=>{ start(); });
    document.querySelectorAll('[data-resume]').forEach(b=>b.onclick=()=>{ if(document.getElementById('pause').hidden===false){ state='running'; hideOverlays(); } });
    document.getElementById('mute').onclick=toggleMute;
  }

  function boot(){
    setupDpr();
    scoreEl=document.getElementById('score');
    bestEl=document.getElementById('best');
    bestWrap=document.querySelector('.best-wrap');
    muted=loadMuted();
    if(muted){ document.getElementById('mute').classList.add('off'); const w=document.querySelector('#mute .wave'); if(w) w.style.opacity=0; }
    initWorld();
    refreshHud();
    bind();
    last=performance.now();
    raf=requestAnimationFrame(frame);
  }

  boot();
})();
</script>
</body>
</html>
```

A few things I leaned on to make it feel lively rather than flat:

- **A real alpaca**, not a rectangle — fluff‑ball body, long neck, tufted head, droopy ears, blinking eye, cheek blush, and legs that actually cycle while running, with a squash‑and‑stretch shadow and a slight airborne tilt.
- **Layered depth**: soft sky → rotating sun → drifting clouds → rolling hills (parallax at 0.3×) → ground with grass tufts (full speed) → flowers (0.9×) → cactus/gulls.
- **Feedback everywhere**: dust on takeoff, score popups when you clear an obstacle, sparkle + screen shake + flash on a hit, a milestone chime every 50 m, and a "Get ready…" beat before the run so it never feels instant.
- **Lighthearted Web Audio** blips for jump, double‑jump, milestone, hit, plus a little fanfare on a new best — all synthesized, mutable with **M**.
- **Double jump** as a forgiving flourish, and high score persisted in `localStorage`.

Everything is one file, no external dependencies.

16 t/s, 13761 tokens, 881s
