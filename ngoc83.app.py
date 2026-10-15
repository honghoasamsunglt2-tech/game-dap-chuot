import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game đập chuột",
    page_icon="🐭",
    layout="centered"
)

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background: #b5f58d;
    overflow: hidden;
    color: white;
    user-select: none;
}

#game {
    width: 100%;
    max-width: 680px;
    height: 760px;
    max-height: 95vh;
    min-height: 550px;
    margin: auto;
    position: relative;
    overflow: hidden;
    border: 6px solid #c9ff9f;
    border-radius: 25px;
    background:
        radial-gradient(ellipse at center, #91e85d 0%, #54b83d 70%, #318b2b 100%);
    box-shadow: 0 0 24px #83ff68;
}

#menu, #gameover, #pauseScreen {
    position: absolute;
    inset: 0;
    z-index: 20;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 22px;
    background: rgba(39, 132, 35, 0.25);
    backdrop-filter: blur(3px);
}

#menu h1 {
    font-size: clamp(34px, 8vw, 53px);
    font-style: italic;
    font-weight: 1000;
    line-height: 1.2;
    color: #fff;
    text-shadow:
        0 0 5px #65ff47,
        0 0 15px #4dff36,
        3px 4px 0 #258b28;
    margin: 0 0 12px;
}

.subtitle {
    font-size: 17px;
    font-weight: bold;
    margin-bottom: 25px;
}

button, select {
    border: 3px solid #d6ffb5;
    border-radius: 17px;
    padding: 13px 20px;
    font-size: 17px;
    font-weight: bold;
    color: #24762c;
    background: #f3ffe7;
    cursor: pointer;
}

button:active {
    transform: scale(.96);
}

#startBtn {
    background: linear-gradient(#e0ff9a, #9bff6a);
    color: #246a20;
    font-size: 23px;
    padding: 16px 42px;
    box-shadow: 0 0 20px #d4ff9a;
    margin-top: 18px;
}

#hud {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 5px;
    z-index: 5;
}

.hudBox {
    border: 2px solid rgba(255,255,255,.8);
    border-radius: 13px;
    background: rgba(23, 98, 30, .75);
    padding: 9px 10px;
    font-size: 16px;
    font-weight: bold;
    text-shadow: 0 1px 2px #245c22;
}

#menuBtn {
    color: white;
    background: rgba(24, 91, 25, .8);
    border: 2px solid white;
    padding: 7px 12px;
    font-size: 22px;
    border-radius: 12px;
}

#field {
    position: absolute;
    top: 95px;
    bottom: 20px;
    left: 5%;
    right: 5%;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    grid-template-rows: repeat(3, minmax(0, 1fr));
    gap: 12px 8px;
}

.hole {
    position: relative;
    min-width: 0;
    min-height: 0;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    overflow: hidden;
    cursor: pointer;
    touch-action: manipulation;
}

.hole::before {
    content: "";
    position: absolute;
    bottom: 7%;
    left: 4%;
    width: 92%;
    height: 34%;
    border-radius: 50%;
    background: radial-gradient(ellipse, #173719 0%, #2b4e21 62%, #6cbd43 66%, #8de25c 75%);
    border: 3px solid #b7f57e;
    box-shadow: 0 4px 0 rgba(36, 103, 30, .35);
    z-index: 2;
}

.mouse {
    position: absolute;
    z-index: 1;
    bottom: 16%;
    left: 50%;
    transform: translate(-50%, 110%);
    font-size: clamp(45px, 10vw, 68px);
    line-height: 1;
    transition: transform .13s ease-out;
    filter: drop-shadow(0 4px 2px rgba(0,0,0,.18));
    cursor: pointer;
    padding: 5px;
}

.hole.up .mouse {
    transform: translate(-50%, -10%);
}

.hole.hit .mouse {
    transform: translate(-50%, 120%) rotate(20deg) scale(.65);
}

.hole.up::after {
    content: "";
    position: absolute;
    bottom: 8%;
    left: 12%;
    width: 76%;
    height: 25%;
    border-radius: 50%;
    background: rgba(21, 46, 16, .22);
    z-index: 3;
    pointer-events: none;
}

#countdown {
    position: absolute;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    font-size: 100px;
    font-weight: 1000;
    color: white;
    text-shadow: 0 0 25px #54ff34, 3px 4px #267d25;
    z-index: 12;
    pointer-events: none;
}

#message {
    position: absolute;
    top: 44%;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 30px;
    font-weight: 1000;
    color: white;
    text-shadow: 0 2px 5px #256c21;
    z-index: 10;
    pointer-events: none;
}

#gameover h2, #pauseScreen h2 {
    font-size: 35px;
    margin: 0 0 12px;
    text-shadow: 0 3px 8px #26752b;
}

#gameover p, #pauseScreen p {
    font-size: 21px;
    font-weight: bold;
}

.hidden {
    display: none !important;
}

#soundBtn {
    position: absolute;
    bottom: 10px;
    right: 10px;
    z-index: 8;
    padding: 7px 11px;
    font-size: 17px;
    background: rgba(29, 100, 31, .8);
    color: white;
    border: 2px solid white;
}

#game.shake {
    animation: shake .22s linear;
}

@keyframes shake {
    0%,100% { transform: translateX(0); }
    25% { transform: translateX(-5px) rotate(-.4deg); }
    50% { transform: translateX(5px) rotate(.4deg); }
    75% { transform: translateX(-3px); }
}

@media(max-height: 650px) {
    #game {
        height: 95vh;
        min-height: 0;
    }
    #field {
        top: 80px;
    }
    .hudBox {
        padding: 6px;
        font-size: 14px;
    }
}
</style>
</head>

<body>
<div id="game">

    <div id="menu">
        <h1>🐭 Game đập chuột 🐭</h1>
        <div class="subtitle">🌿 BÃI CỎ VUI NHỘN 🌿</div>

        <p style="font-weight:bold">Chọn độ khó:</p>
        <select id="difficulty">
            <option value="3000">Dễ - 3 giây</option>
            <option value="2500">Vừa - 2,5 giây</option>
            <option value="1000">Khó - 1 giây</option>
        </select>

        <button id="startBtn">▶ BẮT ĐẦU</button>
        <p>🔨 Đập chuột để ghi điểm!</p>
        <p>❤️ Có 3 mạng - chơi trong 60 giây</p>
    </div>

    <div id="hud" class="hidden">
        <div class="hudBox" id="lives">❤️❤️❤️</div>
        <div class="hudBox">⭐ <span id="score">0</span></div>
        <div class="hudBox">⏱️ <span id="time">60</span>s</div>
        <button id="menuBtn" aria-label="Mở menu">☰</button>
    </div>

    <div id="field" class="hidden"></div>
    <div id="countdown">3</div>
    <div id="message"></div>

    <button id="soundBtn">🔊 Âm thanh: Bật</button>

    <div id="pauseScreen" class="hidden">
        <h2>⏸️ Đang tạm dừng</h2>
        <button id="resumeBtn">▶ Chơi tiếp</button>
        <br>
        <button id="homeBtn">🏠 Về menu</button>
    </div>

    <div id="gameover" class="hidden">
        <h2>⏰ Hết thời gian!</h2>
        <p>Điểm của em: <span id="finalScore">0</span></p>
        <p>🏆 Kỷ lục: <span id="bestScore">0</span></p>
        <button id="retryBtn">🔄 Chơi lại</button>
        <br>
        <button id="backBtn">🏠 Về menu</button>
    </div>
</div>

<script>
const game = document.getElementById('game');
const menu = document.getElementById('menu');
const field = document.getElementById('field');
const hud = document.getElementById('hud');
const countdown = document.getElementById('countdown');
const pauseScreen = document.getElementById('pauseScreen');
const gameover = document.getElementById('gameover');

let score = 0;
let lives = 3;
let timeLeft = 60;
let best = 0;
let spawnDelay = 3000;
let running = false;
let paused = false;
let soundOn = true;
let activeHole = -1;
let spawnTimer = null;
let clockTimer = null;
let mouseTimer = null;
let countdownTimer = null;
let audioContext = null;
let lastSpawnToken = 0;

try {
    best = Number(localStorage.getItem('dapChuotBest') || 0);
} catch(e) {}

const holes = [];

for (let i = 0; i < 9; i++) {
    const hole = document.createElement('div');
    hole.className = 'hole';
    hole.innerHTML = '<div class="mouse" aria-label="Chuột">🐭</div>';
    hole.dataset.index = i;
    field.appendChild(hole);
    holes.push(hole);

    hole.addEventListener('pointerdown', function(e) {
        if (!running || paused) return;
        if (Number(hole.dataset.token || 0) !== lastSpawnToken) return;
        if (!hole.classList.contains('up')) return;

        e.preventDefault();
        hitMouse(hole);
    });
}

function beep(freq = 500, duration = 0.08, type = 'sine') {
    if (!soundOn) return;

    try {
        audioContext = audioContext || new (window.AudioContext || window.webkitAudioContext)();
        if (audioContext.state === 'suspended') audioContext.resume();

        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.type = type;
        osc.frequency.value = freq;
        gain.gain.value = 0.06;
        osc.connect(gain);
        gain.connect(audioContext.destination);
        osc.start();
        gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
        osc.stop(audioContext.currentTime + duration);
    } catch(e) {}
}

function clearTimers() {
    clearTimeout(spawnTimer);
    clearInterval(clockTimer);
    clearTimeout(mouseTimer);
    clearInterval(countdownTimer);
    spawnTimer = null;
    clockTimer = null;
    mouseTimer = null;
    countdownTimer = null;
}

function clearMice() {
    holes.forEach(h => {
        h.classList.remove('up', 'hit');
        h.dataset.token = '';
    });
    activeHole = -1;
}

function updateHUD() {
    document.getElementById('score').textContent = score;
    document.getElementById('time').textContent = timeLeft;
    document.getElementById('lives').textContent =
        '❤️'.repeat(Math.max(0, lives)) + '🖤'.repeat(3 - Math.max(0, lives));
}

function startGame() {
    clearTimers();
    clearMice();

    score = 0;
    lives = 3;
    timeLeft = 60;
    spawnDelay = Number(document.getElementById('difficulty').value);
    running = false;
    paused = false;

    menu.classList.add('hidden');
    gameover.classList.add('hidden');
    pauseScreen.classList.add('hidden');
    hud.classList.remove('hidden');
    field.classList.remove('hidden');
    countdown.style.display = 'flex';

    updateHUD();

    let count = 3;
    countdown.textContent = count;
    beep(440, 0.1);

    countdownTimer = setInterval(() => {
        count--;

        if (count > 0) {
            countdown.textContent = count;
            beep(440, 0.1);
        } else {
            clearInterval(countdownTimer);
            countdownTimer = null;
            countdown.style.display = 'none';
            beginRound();
        }
    }, 1000);
}

function beginRound() {
    if (paused) return;
    running = true;
    paused = false;
    updateHUD();
    scheduleMouse(300);

    clockTimer = setInterval(() => {
        if (!running || paused) return;

        timeLeft--;
        updateHUD();

        if (timeLeft <= 0) {
            endGame('time');
        }
    }, 1000);
}

function scheduleMouse(delay) {
    clearTimeout(spawnTimer);

    spawnTimer = setTimeout(() => {
        if (!running || paused) return;

        if (activeHole !== -1) {
            const oldHole = holes[activeHole];
            oldHole.classList.remove('up');
            activeHole = -1;
        }

        const available = holes
            .map((h, i) => i)
            .filter(i => i !== activeHole);

        const index = available[Math.floor(Math.random() * available.length)];
        const hole = holes[index];

        activeHole = index;
        lastSpawnToken++;
        hole.dataset.token = lastSpawnToken;
        hole.classList.remove('hit');
        hole.classList.add('up');

        // Thỉnh thoảng xuất hiện chuột vàng thưởng điểm.
        const special = Math.random() < 0.12;
        hole.querySelector('.mouse').textContent = special ? '🐹' : '🐭';
        hole.dataset.points = special ? '3' : '1';

        mouseTimer = setTimeout(() => {
            if (!running || paused) return;
            if (activeHole !== index) return;

            hole.classList.remove('up');
            activeHole = -1;

            lives--;
            updateHUD();
            beep(180, 0.13, 'triangle');

            if (lives <= 0) {
                endGame('lives');
                return;
            }

            scheduleMouse(250);
        }, spawnDelay);
    }, delay);
}

function hitMouse(hole) {
    if (!running || paused || activeHole === -1) return;

    clearTimeout(mouseTimer);
    mouseTimer = null;

    const points = Number(hole.dataset.points || 1);
    score += points;
    activeHole = -1;

    hole.classList.remove('up');
    hole.classList.add('hit');

    beep(points === 3 ? 850 : 620, 0.08);
    game.classList.remove('shake');
    void game.offsetWidth;
    game.classList.add('shake');

    document.getElementById('message').textContent =
        points === 3 ? '+3 ĐIỂM! ✨' : '+1 ĐIỂM!';

    setTimeout(() => {
        document.getElementById('message').textContent = '';
        hole.classList.remove('hit');
        hole.querySelector('.mouse').textContent = '🐭';
    }, 300);

    updateHUD();
    scheduleMouse(280);
}

function endGame(reason) {
    if (!running) return;

    running = false;
    paused = false;
    clearTimers();
    clearMice();

    countdown.style.display = 'none';
    pauseScreen.classList.add('hidden');
    gameover.classList.remove('hidden');

    document.getElementById('finalScore').textContent = score;

    if (score > best) {
        best = score;
        try {
            localStorage.setItem('dapChuotBest', String(best));
        } catch(e) {}
    }

    document.getElementById('bestScore').textContent = best;
    document.querySelector('#gameover h2').textContent =
        reason === 'lives' ? '💔 Hết mạng!' : '⏰ Hết thời gian!';

    beep(240, 0.25, 'triangle');
}

function togglePause() {
    if (!running && !paused) return;

    if (paused) {
        paused = false;
        pauseScreen.classList.add('hidden');

        // Tiếp tục lượt chơi với một con chuột mới.
        scheduleMouse(300);
        return;
    }

    paused = true;
    clearTimeout(spawnTimer);
    clearTimeout(mouseTimer);
    pauseScreen.classList.remove('hidden');
}

function goHome() {
    running = false;
    paused = false;
    clearTimers();
    clearMice();

    countdown.style.display = 'none';
    menu.classList.remove('hidden');
    hud.classList.add('hidden');
    field.classList.add('hidden');
    gameover.classList.add('hidden');
    pauseScreen.classList.add('hidden');
    document.getElementById('message').textContent = '';
}

document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('retryBtn').addEventListener('click', startGame);
document.getElementById('backBtn').addEventListener('click', goHome);
document.getElementById('homeBtn').addEventListener('click', goHome);
document.getElementById('menuBtn').addEventListener('click', togglePause);
document.getElementById('resumeBtn').addEventListener('click', togglePause);

document.getElementById('soundBtn').addEventListener('click', () => {
    soundOn = !soundOn;
    document.getElementById('soundBtn').textContent =
        soundOn ? '🔊 Âm thanh: Bật' : '🔇 Âm thanh: Tắt';
    if (soundOn) beep(550, 0.08);
});

document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
        if (running || paused) togglePause();
    }
});

updateHUD();
</script>
</body>
</html>
"""

components.html(game, height=780, scrolling=False)
"""

st.components.v1.html(game, height=780, scrolling=False)
