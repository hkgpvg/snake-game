import streamlit as st

st.set_page_config(page_title="🐍 贪吃蛇游戏", page_icon="🐍", layout="centered")

st.markdown("""
<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: Arial, sans-serif; text-align: center; background: #0e1117; color: white; margin: 0; padding: 20px; }
h1 { color: #00ff00; }
#game { border: 2px solid #00ff00; border-radius: 10px; margin: 20px auto; display: block; }
.controls { margin: 20px; }
button { font-size: 24px; padding: 10px 20px; margin: 5px; background: #1a1a2e; color: #00ff00; border: 2px solid #00ff00; border-radius: 5px; cursor: pointer; }
button:hover { background: #00ff00; color: #1a1a2e; }
#score { font-size: 24px; color: #00ff00; }
.instructions { color: #888; margin: 10px; }
</style>
</head>
<body>
<h1>🐍 贪吃蛇游戏</h1>
<p class="instructions">控制方法：W/A/S/D 或 箭头键，或使用屏幕按钮</p>
<canvas id="game" width="400" height="400"></canvas>
<div class="controls">
<div><button onclick="setDir('UP')">⬆️</button></div>
<div><button onclick="setDir('LEFT')">⬅️</button> <button onclick="startGame()">🎮 开始/重置</button> <button onclick="setDir('RIGHT')">➡️</button></div>
<div><button onclick="setDir('DOWN')">⬇️</button></div>
</div>
<div id="score">🏆 分数：0</div>

<script>
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const gridSize = 20;
const tileCount = 20;

let snake = [{x: 10, y: 10}];
let food = {x: 15, y: 15};
let dx = 0, dy = 0;
let score = 0;
let gameLoop;
let started = false;
let speed = 200;

document.addEventListener('keydown', (e) => {
    const key = e.key.toUpperCase();
    if (['W','ARROWUP'].includes(key) && dy !== 1) { dx = 0; dy = -1; }
    else if (['S','ARROWDOWN'].includes(key) && dy !== -1) { dx = 0; dy = 1; }
    else if (['A','ARROWLEFT'].includes(key) && dx !== 1) { dx = -1; dy = 0; }
    else if (['D','ARROWRIGHT'].includes(key) && dx !== -1) { dx = 1; dy = 0; }
    if (!started && (dx || dy)) startGame();
    e.preventDefault();
});

function setDir(dir) {
    if (dir === 'UP' && dy !== 1) { dx = 0; dy = -1; }
    else if (dir === 'DOWN' && dy !== -1) { dx = 0; dy = 1; }
    else if (dir === 'LEFT' && dx !== 1) { dx = -1; dy = 0; }
    else if (dir === 'RIGHT' && dx !== -1) { dx = 1; dy = 0; }
    if (!started) startGame();
}

function startGame() {
    snake = [{x: 10, y: 10}];
    food = {x: 15, y: 15};
    dx = 1; dy = 0;
    score = 0;
    started = true;
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, speed);
}

function update() {
    const head = {x: snake[0].x + dx, y: snake[0].y + dy};
    head.x = (head.x + tileCount) % tileCount;
    head.y = (head.y + tileCount) % tileCount;
    
    if (snake.some(s => s.x === head.x && s.y === head.y)) {
        clearInterval(gameLoop);
        started = false;
        alert('💀 游戏结束！分数：' + score);
        return;
    }
    
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        food = {x: Math.floor(Math.random() * tileCount), y: Math.floor(Math.random() * tileCount)};
    } else {
        snake.pop();
    }
    
    document.getElementById('score').textContent = '🏆 分数：' + score;
    draw();
}

function draw() {
    ctx.fillStyle = '#16213e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ff0000';
    ctx.beginPath();
    ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI * 2);
    ctx.fill();
    
    snake.forEach((seg, i) => {
        ctx.fillStyle = i === 0 ? '#00ff00' : '#00cc00';
        ctx.fillRect(seg.x * gridSize + 1, seg.y * gridSize + 1, gridSize - 2, gridSize - 2);
    });
}

draw();
</script>
</body>
</html>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("🎮 Created with Streamlit")
