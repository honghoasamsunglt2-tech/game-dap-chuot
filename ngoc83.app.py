import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game đập chuột",
    page_icon="🐹",
    layout="centered"
)

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: white;
    background: #111827;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}

#game {
    max-width: 600px;
    margin: auto;
    padding: 12px;
    text-align: center;
}

h1 {
    color: #fbbf24;
    font-size: clamp(25px, 6vw, 36px);
    margin: 8px 0;
    text-shadow: 0 0 12px #f59e0b;
}

.subtitle {
    color: #cbd5e1;
    margin-bottom: 15px;
}

.panel {
    background: #1f2937;
    border: 2px solid #374151;
    border-radius: 18px;
    padding: 13px;
    margin-bottom: 12px;
}

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
}

.stat {
    background: #111827;
    border-radius: 12px;
    padding: 10px 3px;
}

.stat-label {
    font-size: 12px;
    color: #9ca3af;
}

.stat-value {
    font-size: 21px;
    font-weight: bold;
    margin-top: 5px;
}

#lives {
    color: #fb7185;
}

#score {
    color: #fbbf24;
}

#time {
    color: #67e8f9;
}

button, select {
    border: 0;
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
}

button:active {
    transform: scale(.96);
}

.primary {
    background: #fbbf24;
    color: #111827;
}

.secondary {
    background: #374151;
    color: white;
}

.danger {
    background: #ef4444;
    color: white;
}

.music-button {
    width: 100%;
    margin-top: 10px;
}

#menu {
    display: block;
}

#playArea {
    display: none;
}

#board {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    padding: 12px;
    background: #14532d;
    border: 3px solid #22c55e;
    border-radius: 20px;
}

.hole {
    aspect-ratio: 1 / 1;
    min-width: 0;
    position: relative;
    overflow: hidden;
    border-radius: 50%;
    background: #422006;
    border: 5px solid #713f12;
    box-shadow: inset 0 5px 12px #0008;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(36px, 10vw, 58px);
    cursor: pointer;
    touch-action: manipulation;
}

.hole::before {
    content: "";
    position: absolute;
    inset: 10%;
    border-radius: 50%;
    background: #1c1917;
    z-index: 0;
}

.character {
    position: relative;
    z-index: 1;
    animation: pop .13s ease-out;
    line-height: 1;
}

@keyframes pop {
    from { transform: translateY(25px) scale(.7); }
    to { transform: translateY(0) scale(1); }
}

#message {
    min-height: 27px;
    margin: 10px 0;
    font-weight: bold;
    color: #fde68a;
}

.controls {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    margin-top: 10px;
}

.controls button {
    width: 100%;
}

select {
    width: 100%;
    background: #111827;
    color: white;
    margin-top: 8px;
    border: 1px solid #4b5563;
}

.small {
    color: #cbd5e1;
    font-size: 13px;
    line-height: 1.6;
}

#result {
    display: none;
    margin-top: 12px;
    padding: 15px;
    border-radius: 15px;
    background: #312e81;
}

#result h2 {
    color: #fde68a;
}

.footer {
    color: #9ca3af;
    font-size: 12px;
    margin-top: 12px;
}

@media (max-width: 360px) {
    #game {
        padding: 6px;
    }

    #board {
        gap: 6px;
        padding: 8px;
    }

    .hole {
        border-width: 3px;
    }
}
</style>
</head>

<body>
<div id="game">

    <h1>🐹 GAME ĐẬP CHUỘT 🐭</h1>
    <div class="subtitle">Nhanh tay lẹ mắt — coi chừng bom! 💣</div>

    <div class="panel">
        <div class="stats">
            <div class="stat">
                <div class="stat-label">⭐ ĐIỂM</div>
                <div class="stat-value" id="score">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">❤️ MẠNG</div>
                <div class="stat-value" id="lives">❤️❤️❤️</div>
            </div>
            <div class="stat">
                <div class="stat-label">⏱️ THỜI GIAN</div>
                <div class="stat-value" id="time">30</div>
            </div>
        </div>
    </div>

    <div id="menu" class="panel">
        <h2>🎯 Sẵn sàng chưa?</h2>
        <p>🐭 Chuột thường: +1 điểm</p>
        <p>🐹 Hamster: +3 điểm</p>
        <p>💣 Đập trúng bom: THUA NGAY!</p>
        <p>❤️ Em có 3 mạng và 30 giây để ghi điểm.</p>

        <label for="difficulty">Chọn độ khó:</label>
        <select id="difficulty">
            <option value="3000">Dễ — 3 giây</option>
            <option value="2500" selected>Vừa — 2,5 giây</option>
            <option value="1000">Khó — 1 giây</option>
        </select>

        <button class="primary" id="startBtn"
                style="width:100%;margin-top:12px">
            🎮 BẮT ĐẦU
        </button>

        <button class="secondary music-button" id="musicBtn">
            🔇 Bật nhạc
        </button>

        <p class="small">
            Nhớ né bom nhaaa! Chúc em đạt điểm cao! 🏆
        </p>
    </div>

    <div id="playArea">
        <div class="panel">
            <div id="board">
                <button class="hole" data-index="0" aria-label="Ô 1"></button>
                <button class="hole" data-index="1" aria-label="Ô 2"></button>
                <button class="hole" data-index="2" aria-label="Ô 3"></button>
                <button class="hole" data-index="3" aria-label="Ô 4"></button>
                <button class="hole" data-index="4" aria-label="Ô 5"></button>
                <button class="hole" data-index="5" aria-label="Ô 6"></button>
                <button class="hole" data-index="6" aria-label="Ô 7"></button>
                <button class="hole" data-index="7" aria-label="Ô 8"></button>
                <button class="hole" data-index="8" aria-label="Ô 9"></button>
            </div>

            <div id="message">Bắt đầu đập chuột thôi!</div>

            <div class="controls">
                <button class="secondary" id="pauseBtn">⏸️ Tạm dừng</button>
                <button class="secondary" id="homeBtn">🏠 Trang chủ</button>
            </div>
        </div>
    </div>

    <div id="result">
        <h2 id="resultTitle">🎉 KẾT THÚC!</h2>
        <p id="resultScore"></p>
        <p id="bestScore"></p>
        <button class="primary" id="restartBtn" style="width:100%">
            🔄 Chơi lại
        </button>
        <button class="secondary" id="resultHomeBtn"
                style="width:100%;margin-top:8px">
            🏠 Trang chủ
        </button>
    </div>

    <div class="footer">
        🐭 Chuột thường +1 | 🐹 Hamster +3 | 💣 Bom = thua ngay
    </div>
</div>

<!-- Nhạc được tải từ GitHub -->
<audio id="music" loop preload="none"
src="https://raw.githubusercontent.com/honghoasamsunglt2-tech/game-dap-chuot/main/ngoc83.mp3">
</audio>

<script>
(function () {
    const $ = id => document.getElementById(id);

    const menu = $("menu");
    const playArea = $("playArea");
    const result = $("result");
    const board = $("board");
    const holes = Array.from(document.querySelectorAll(".hole"));
    const music = $("music");

    let score = 0;
    let lives = 3;
    let seconds = 30;
    let running = false;
    let paused = false;
    let musicOn = false;

    let spawnTimer = null;
    let clockTimer = null;
    let clearTimer = null;

    let currentIndex = -1;
    let currentType = "";
    let roundId = 0;
    let best = loadBest();

    function loadBest() {
        try {
            return Number(localStorage.getItem("dapChuotBest")) || 0;
        } catch (e) {
            return 0;
        }
    }

    function saveBest(value) {
        try {
            localStorage.setItem("dapChuotBest", String(value));
        } catch (e) {}
    }

    function updateHUD() {
        $("score").textContent = score;
        $("lives").textContent = "❤️".repeat(lives) + "🖤".repeat(3 - lives);
        $("time").textContent = seconds;
    }

    function stopTimers() {
        clearInterval(spawnTimer);
        clearInterval(clockTimer);
        clearTimeout(clearTimer);

        spawnTimer = null;
        clockTimer = null;
        clearTimer = null;
    }

    function clearBoard() {
        holes.forEach(hole => {
            hole.replaceChildren();
        });

        currentIndex = -1;
        currentType = "";
    }

    function playMusic() {
        if (!musicOn || !running || paused) return;

        music.play().catch(() => {
            $("message").textContent =
                "Nhấn nút nhạc rồi bắt đầu để nghe nhạc 🎵";
        });
    }

    function stopMusic() {
        music.pause();
    }

    function updateMusicButton() {
        $("musicBtn").textContent =
            musicOn ? "🔊 Tắt nhạc" : "🔇 Bật nhạc";
    }

    function setMusic(enabled) {
        musicOn = enabled;
        updateMusicButton();

        if (musicOn && running && !paused) {
            playMusic();
        } else {
            stopMusic();
        }
    }

    function showCreature(index, type, thisRound) {
        if (!running || paused || thisRound !== roundId) return;

        clearBoard();

        currentIndex = index;
        currentType = type;

        const character = document.createElement("span");
        character.className = "character";

        if (type === "mouse") {
            character.textContent = "🐭";
        } else if (type === "hamster") {
            character.textContent = "🐹";
        } else {
            character.textContent = "💣";
        }

        holes[index].appendChild(character);

        clearTimer = setTimeout(() => {
            if (thisRound !== roundId || !running || paused) return;

            clearBoard();
            clearTimer = null;
        }, Math.max(650, Number($("difficulty").value) - 150));
    }

    function spawnCreature(thisRound) {
        if (!running || paused || thisRound !== roundId) return;

        const index = Math.floor(Math.random() * holes.length);
        const roll = Math.random();

        let type;

        if (roll < 0.14) {
            type = "bomb";
        } else if (roll < 0.42) {
            type = "hamster";
        } else {
            type = "mouse";
        }

        showCreature(index, type, thisRound);
    }

    function startTimers() {
        const thisRound = roundId;
        const interval = Number($("difficulty").value);

        spawnTimer = setInterval(() => {
            spawnCreature(thisRound);
        }, interval);

        clockTimer = setInterval(() => {
            if (!running || paused || thisRound !== roundId) return;

            seconds--;
            updateHUD();

            if (seconds <= 0) {
                endGame("⏰ HẾT GIỜ!");
            }
        }, 1000);

        spawnCreature(thisRound);
    }

    function startGame() {
        stopTimers();
        roundId++;

        score = 0;
        lives = 3;
        seconds = 30;
        running = true;
        paused = false;

        updateHUD();
        clearBoard();

        menu.style.display = "none";
        result.style.display = "none";
        playArea.style.display = "block";

        $("pauseBtn").textContent = "⏸️ Tạm dừng";
        $("message").textContent = "Nhanh tay lên nào!";

        startTimers();
        playMusic();
    }

    function endGame(title) {
        if (!running) return;

        running = false;
        paused = false;
        roundId++;

        stopTimers();
        clearBoard();
        stopMusic();

        if (score > best) {
            best = score;
            saveBest(best);
        }

        playArea.style.display = "none";
        menu.style.display = "none";
        result.style.display = "block";

        $("resultTitle").textContent = title;
        $("resultScore").textContent = "Điểm của em: " + score;
        $("bestScore").textContent = "🏆 Kỷ lục: " + best;
    }

    function pauseGame() {
        if (!running) return;

        paused = !paused;

        if (paused) {
            stopTimers();
            clearBoard();
            stopMusic();

            $("pauseBtn").textContent = "▶️ Tiếp tục";
            $("message").textContent = "⏸️ Đang tạm dừng";
        } else {
            $("pauseBtn").textContent = "⏸️ Tạm dừng";
            $("message").textContent = "Tiếp tục nào!";

            startTimers();
            playMusic();
        }
    }

    function goHome() {
        running = false;
        paused = false;
        roundId++;

        stopTimers();
        clearBoard();
        stopMusic();

        playArea.style.display = "none";
        result.style.display = "none";
        menu.style.display = "block";

        updateHUD();
    }

    function hitHole(index) {
        if (!running || paused || currentIndex !== index || !currentType) {
            return;
        }

        const type = currentType;

        clearTimeout(clearTimer);
        clearTimer = null;
        clearBoard();

        if (type === "bomb") {
            endGame("💥 DÍNH BOM! THUA RỒI!");
            return;
        }

        if (type === "hamster") {
            score += 3;
            $("message").textContent = "🐹 +3 điểm! Giỏi quá!";
        } else {
            score += 1;
            $("message").textContent = "🐭 +1 điểm!";
        }

        updateHUD();

        // Tăng tốc độ xuất hiện một chút theo tiến trình,
        // nhưng không vượt quá tốc độ đã chọn.
    }

    holes.forEach((hole, index) => {
        hole.addEventListener("click", () => hitHole(index));
    });

    $("startBtn").addEventListener("click", startGame);
    $("restartBtn").addEventListener("click", startGame);
    $("pauseBtn").addEventListener("click", pauseGame);
    $("homeBtn").addEventListener("click", goHome);
    $("resultHomeBtn").addEventListener("click", goHome);

    $("musicBtn").addEventListener("click", () => {
        setMusic(!musicOn);
        if (musicOn) {
            playMusic();
        }
    });

    music.addEventListener("error", () => {
        $("message").textContent =
            "Không tải được nhạc. Kiểm tra file ngoc83.mp3 trên GitHub nhé!";
    });

    updateHUD();
    updateMusicButton();
})();
</script>
</body>
</html>
"""

components.html(game, height=800, scrolling=False)

st.markdown(
    "<div style='text-align:center;color:#9ca3af;font-size:12px'>"
    "🐭 Chúc bạn chơi vui vẻ! 🐹"
    "</div>",
    unsafe_allow_html=True
)
