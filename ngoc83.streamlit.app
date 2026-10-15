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
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #8bd66b;
}

#game {
    position: relative;
    width: 100%;
    max-width: 520px;
    height: 780px;
    max-height: 95vh;
    margin: auto;
    overflow: hidden;
    border: 4px solid #d5ffc3;
    border-radius: 22px;
    background:
        radial-gradient(ellipse at top, #b9f58b, transparent 60%),
        linear-gradient(#75ca55, #368c35);
    box-shadow: 0 0 25px #d8ffc7;
}

#menu, #over, #countdown, #pauseScreen {
    position: absolute;
    inset: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 18px;
    text-align: center;
    background: #246c36d9;
}

.panel {
    width: 100%;
    padding: 25px 17px;
    border: 3px solid #caffb5;
    border-radius: 25px;
    background: linear-gradient(145deg, #a7ed85, #4ca94c);
    box-shadow: 0 0 25px #caffb5;
}

h1 {
    margin: 0 0 12px;
    color: #155b27;
    font-size: clamp(32px, 8vw, 45px);
    font-weight: 900;
    font-style: italic;
    text-shadow: 2px 3px #caffb5;
}

.sub {
    color: #164e22;
    font-weight: bold;
    margin-bottom: 20px;
}

.btn {
    width: 100%;
    margin: 7px 0;
    padding: 13px 10px;
    border: 2px solid #d5ffc4;
    border-radius: 14px;
    background: #237d39;
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

.btn:active {
    transform: scale(.97);
}

.row {
    display: flex;
    gap: 7px;
}

.row .btn {
    flex: 1;
}

#topbar {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 8;
}

.hud {
    padding: 8px 10px;
    background: #18592c;
    color: white;
    border: 2px solid #caffb5;
    border-radius: 12px;
    font-weight: bold;
    font-size: 15px;
}

#pauseBtn {
    border: 2px solid #caffb5;
    background: #18592c;
    color: white;
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 20px;
}

#field {
    position: absolute;
    inset: 65px 8px 10px;
    overflow: hidden;
    border-radius: 20px;
    background:
        radial-gradient(ellipse, #a4e66c 0%, #62b847 70%, #439d39 100%);
    border: 2px solid #c7fba9;
}

.grass {
    position: absolute;
    width: 7px;
    height: 15px;
    background: #d3ff9c;
    border-radius: 100%;
    opacity: .7;
}

.hole {
    position: absolute;
    width: 27%;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hole::before {
    content: "";
    position: absolute;
    width: 90%;
    height: 42px;
    bottom: 0;
    border-radius: 50%;
    background: #58351d;
    border: 5px solid #93613a;
    box-shadow: inset 0 5px 8px #241509;
}

.mouse {
    position: absolute;
    z-index: 4;
    bottom: 13px;
    width: 82px;
    height: 78px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 60px;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    animation: pop .15s ease-out;
}

@keyframes pop {
    from { transform: translateY(30px) scale(.7); }
    to { transform: translateY(0) scale(1); }
}

.fall {
    animation: fall .65s ease-in forwards, shake .12s linear infinite;
}

@keyframes fall {
    to { transform: translateY(160px) rotate(20deg); opacity: .15; }
}

@keyframes shake {
    0%,100% { margin-left: 0; }
    25% { margin-left: -5px; }
    75% { margin-left: 5px; }
}

#message {
    position: absolute;
    top: 40%;
    left: 0;
    right: 0;
    z-index: 10;
    text-align: center;
    font-size: 35px;
    font-weight: 900;
    color: white;
    text-shadow: 2px 3px #286c2b;
    pointer-events: none;
}

.hidden {
    display: none !important;
}

.big {
    color: #fff;
    font-size: 38px;
    font-weight: 900;
    text-shadow: 2px 3px #286c2b;
}

.small {
    color: #164e22;
    font-size: 14px;
    line-height: 1.5;
}

@media(max-height: 650px) {
    #game { height: 95vh; }
    .panel { padding: 14px; }
    h1 { font-size: 30px; }
    .btn { padding: 9px; }
}
</style>
</head>

<body>
<div id="game">

    <div id="topbar" class="hidden">
        <div class="hud" id="lives">3❤️</div>
        <div class="hud" id="score">⭐ 0</div>
        <div class="hud" id="timer">⏱ 60</div>
        <button id="pauseBtn">☰</button>
    </div>

    <div id="field" class="hidden">
        <div id="message"></div>
    </div>

    <div id="menu">
        <div class="panel">
            <h1>🐭 Game<br>đập chuột</h1>
            <div class="sub">🌿 ĐỒNG CỎ VUI NHỘN 🌿</div>

            <p style="color:#164e22;font-weight:bold">Chọn độ khó</p>

            <div class="row">
                <button class="btn difficulty" data-delay="3000">DỄ</button>
                <button class="btn difficulty" data-delay="2500">VỪA</button>
                <button class="btn difficulty" data-delay="1000">KHÓ</button>
            </div>

            <button class="btn" id="soundBtn">🔊 ÂM THANH: BẬT</button>
            <button class="btn" id="startBtn">▶ BẮT ĐẦU</button>

            <p class="small">
                🐭 Đập chuột để ghi điểm!<br>
                ❤️ Em có 3 mạng, thời gian chơi 60 giây.<br>
                📱 Chạm chuột hoặc 💻 nhấn chuột trái.
            </p>
        </div>
    </div>

    <div id="countdown" class="hidden">
        <div class="panel">
            <div class="big" id="countNum">3</div>
            <p style="color:#164e22;font-weight:bold">Chuẩn bị đập chuột!</p>
        </div>
    </div>

    <div id="pauseScreen" class="hidden">
        <div class="panel">
            <h1>⏸ Tạm dừng</h1>
            <button class="btn" id="resumeBtn">▶ TIẾP TỤC</button>
            <button class="btn" id="homeBtn">🏠 VỀ MENU CHÍNH</button>
        </div>
    </div>

    <div id="over" class="hidden">
        <div class="panel">
            <h1 id="overTitle">Hết thời gian!</h1>
            <div class="big">⭐ <span id="finalScore">0</span></div>
            <p style="color:#164e22;font-weight:bold">Điểm của em</p>
            <p style="color:#164e22">🏆 Kỷ lục: <span id="best">0</span></p>
            <button class="btn" id="againBtn">🔁 CHƠI LẠI</button>
            <button class="btn" id="overHomeBtn">🏠 VỀ MENU CHÍNH</button>
        </div>
    </div>
</div>

<audio id="music" src="ngoc83.mp3" loop preload="auto"></audio>

<script>
(() => {
const $ = id => document.getElementById(id);
const field = $('field');

let delay = 2500;
let soundOn = true;
let running = false;
let paused = false;
let score = 0;
let lives = 3;
let timeLeft = 60;
let best = 0;
let spawnTimer = null;
let clockTimer = null;
let countdownTimer = null;
let mouseTimer = null;
let currentMouse = null;
let gameToken = 0;

try {
    best = Number(localStorage.getItem('dapChuotBest') || 0);
} catch(e) {}

document.querySelectorAll('.difficulty').forEach(btn => {
    btn.onclick = () => {
        delay = Number(btn.dataset.delay);
        document.querySelectorAll('.difficulty').forEach(b => {
            b.style.background = '#237d39';
        });
        btn.style.background = '#174c26';
    };
});

$('soundBtn').onclick = () => {
    soundOn = !soundOn;
    $('soundBtn').textContent =
        soundOn ? '🔊 ÂM THANH: BẬT' : '🔇 ÂM THANH: TẮT';

    if (!soundOn) {
        $('music').pause();
    } else if (running && !paused) {
        $('music').play().catch(() => {});
    }
};

function playMusic() {
    if (soundOn) $('music').play().catch(() => {});
}

function stopTimers() {
    clearInterval(spawnTimer);
    clearInterval(clockTimer);
    clearInterval(countdownTimer);
    clearTimeout(mouseTimer);
    spawnTimer = clockTimer = countdownTimer = mouseTimer = null;
}

function removeMouse() {
    if (currentMouse) currentMouse.remove();
    currentMouse = null;
}

function resetGame() {
    gameToken++;
    stopTimers();
    removeMouse();
    score = 0;
    lives = 3;
    timeLeft = 60;
    running = false;
    paused = false;

    $('score').textContent = '⭐ 0';
    $('lives').textContent = '3❤️';
    $('timer').textContent = '⏱ 60';
    $('menu').classList.add('hidden');
    $('over').classList.add('hidden');
    $('pauseScreen').classList.add('hidden');
    $('topbar').classList.remove('hidden');
    field.classList.remove('hidden');
    $('countdown').classList.remove('hidden');
    $('message').textContent = '';

    let n = 3;
    $('countNum').textContent = n;

    const token = gameToken;
    countdownTimer = setInterval(() => {
        if (token !== gameToken) return;
        n--;
        if (n > 0) {
            $('countNum').textContent = n;
        } else {
            clearInterval(countdownTimer);
            countdownTimer = null;
            $('countdown').classList.add('hidden');
            beginGame();
        }
    }, 1000);
}

function beginGame() {
    running = true;
    paused = false;
    playMusic();

    spawnMouse();
    spawnTimer = setInterval(spawnMouse, delay);

    clockTimer = setInterval(() => {
        if (!running || paused) return;
        timeLeft--;
        $('timer').textContent = '⏱ ' + timeLeft;
        if (timeLeft <= 0) finish('Hết thời gian!');
    }, 1000);
}

function spawnMouse() {
    if (!running || paused) return;
    removeMouse();

    const m = document.createElement('div');
    m.className = 'mouse';
    m.textContent = Math.random() < 0.15 ? '🐹' : '🐭';
    m.setAttribute('role', 'button');
    m.setAttribute('aria-label', 'Đập chuột');

    const maxX = Math.max(0, field.clientWidth - 90);
    const maxY = Math.max(0, field.clientHeight - 120);
    m.style.left = Math.random() * maxX + 'px';
    m.style.top = (20 + Math.random() * maxY) + 'px';
    m.style.bottom = 'auto';

    m.onclick = e => {
        e.stopPropagation();
        if (!running || paused) return;

        score += m.textContent === '🐹' ? 3 : 1;
        $('score').textContent = '⭐ ' + score;

        m.classList.add('fall');
        m.textContent = '🔨';

        currentMouse = null;
        clearTimeout(mouseTimer);
        mouseTimer = setTimeout(() => m.remove(), 600);

        // Thay chuột sau khi đập trúng
        clearInterval(spawnTimer);
        spawnTimer = setInterval(spawnMouse, delay);
        setTimeout(() => {
            if (running && !paused) spawnMouse();
        }, 300);
    };

    field.appendChild(m);
    currentMouse = m;

    clearTimeout(mouseTimer);
    mouseTimer = setTimeout(() => {
        if (currentMouse === m && running && !paused) {
            m.remove();
            currentMouse = null;
            lives--;
            $('lives').textContent = lives + '❤️';
            if (lives <= 0) finish('Hết mạng!');
        }
    }, delay);
}

function finish(title) {
    if (!running) return;
    running = false;
    paused = false;
    stopTimers();
    removeMouse();
    $('music').pause();
    $('countdown').classList.add('hidden');
    $('pauseScreen').classList.add('hidden');
    $('over').classList.remove('hidden');
    $('overTitle').textContent = title;
    $('finalScore').textContent = score;

    if (score > best) {
        best = score;
        try {
            localStorage.setItem('dapChuotBest', String(best));
        } catch(e) {}
    }
    $('best').textContent = best;
}

$('startBtn').onclick = resetGame;
$('againBtn').onclick = resetGame;

$('pauseBtn').onclick = () => {
    if (!running || paused) {
        if (paused) resumeGame();
        return;
    }

    paused = true;
    $('pauseScreen').classList.remove('hidden');
    $('music').pause();
};

function resumeGame() {
    if (!paused) return;
    paused = false;
    $('pauseScreen').classList.add('hidden');
    playMusic();
}

$('resumeBtn').onclick = resumeGame;

function home() {
    gameToken++;
    running = false;
    paused = false;
    stopTimers();
    removeMouse();
    $('music').pause();
    $('music').currentTime = 0;
    $('menu').classList.remove('hidden');
    $('over').classList.add('hidden');
    $('pauseScreen').classList.add('hidden');
    $('countdown').classList.add('hidden');
    $('topbar').classList.add('hidden');
    field.classList.add('hidden');
}

$('homeBtn').onclick = home;
$('overHomeBtn').onclick = home;

document.addEventListener('keydown', e => {
    if (e.code === 'Space' && !$('menu').classList.contains('hidden')) {
        e.preventDefault();
        resetGame();
    }
    if (e.key === 'Escape' && running && !paused) {
        paused = true;
        $('pauseScreen').classList.remove('hidden');
        $('music').pause();
    }
});

})();
</script>
</body>
</html>
"""

components.html(game, height=800, scrolling=False)
