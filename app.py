import streamlit as st
import random
import time

st.set_page_config(page_title="🐍 贪吃蛇游戏", page_icon="🐍", layout="centered")

if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food = (10, 10)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.speed = 0.5
    st.session_state.last_move_time = 0

GRID_SIZE = 20

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if food not in snake:
            return food

def move_snake(snake, direction):
    head = snake[0]
    if direction == 'UP':
        new_head = ((head[0] - 1) % GRID_SIZE, head[1])
    elif direction == 'DOWN':
        new_head = ((head[0] + 1) % GRID_SIZE, head[1])
    elif direction == 'LEFT':
        new_head = (head[0], (head[1] - 1) % GRID_SIZE)
    elif direction == 'RIGHT':
        new_head = (head[0], (head[1] + 1) % GRID_SIZE)
    return [new_head] + snake[:-1]

def check_collision(snake):
    return snake[0] in snake[1:]

st.title("🐍 贪吃蛇游戏")
st.markdown("### 经典贪吃蛇 - 网页版")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("#### 游戏控制")
    up_col = st.columns([1, 1, 1])
    with up_col[1]:
        if st.button("⬆️", key="up"):
            if st.session_state.direction != 'DOWN':
                st.session_state.direction = 'UP'
                st.rerun()
    mid_col = st.columns([1, 1, 1])
    with mid_col[0]:
        if st.button("⬅️", key="left"):
            if st.session_state.direction != 'RIGHT':
                st.session_state.direction = 'LEFT'
                st.rerun()
    with mid_col[1]:
        if not st.session_state.game_started:
            if st.button("🎮 开始游戏", key="start"):
                st.session_state.game_started = True
                st.session_state.game_over = False
                st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
                st.session_state.direction = 'RIGHT'
                st.session_state.food = generate_food(st.session_state.snake)
                st.session_state.score = 0
                st.session_state.last_move_time = time.time()
                st.rerun()
        elif st.session_state.game_over:
            if st.button("🔄 重新开始", key="restart"):
                st.session_state.game_started = True
                st.session_state.game_over = False
                st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
                st.session_state.direction = 'RIGHT'
                st.session_state.food = generate_food(st.session_state.snake)
                st.session_state.score = 0
                st.session_state.last_move_time = time.time()
                st.rerun()
    with mid_col[2]:
        if st.button("➡️", key="right"):
            if st.session_state.direction != 'LEFT':
                st.session_state.direction = 'RIGHT'
                st.rerun()
    down_col = st.columns([1, 1, 1])
    with down_col[1]:
        if st.button("⬇️", key="down"):
            if st.session_state.direction != 'UP':
                st.session_state.direction = 'DOWN'
                st.rerun()

speed = st.slider("🐢 速度调节", 0.1, 1.0, 0.5, 0.1)
st.session_state.speed = speed
st.markdown(f"### 🏆 分数：**{st.session_state.score}**")

if st.session_state.game_over:
    st.error("💀 游戏结束！")
    st.markdown(f"### 最终分数：{st.session_state.score}")

def render_game():
    output = "<div style='display:grid;grid-template-columns:repeat(20,20px);gap:1px;padding:10px;background:#1a1a2e;border-radius:10px;'>"
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell = (row, col)
            if cell == st.session_state.snake[0]:
                output += "<div style='width:20px;height:20px;background:#00ff00;border-radius:3px;'></div>"
            elif cell in st.session_state.snake:
                output += "<div style='width:20px;height:20px;background:#00cc00;border-radius:3px;'></div>"
            elif cell == st.session_state.food:
                output += "<div style='width:20px;height:20px;background:#ff0000;border-radius:50%;'></div>"
            else:
                output += "<div style='width:20px;height:20px;background:#16213e;border-radius:2px;'></div>"
    output += "</div>"
    st.markdown(output, unsafe_allow_html=True)

if st.session_state.game_started and not st.session_state.game_over:
    render_game()
    if time.time() - st.session_state.last_move_time >= st.session_state.speed:
        new_snake = move_snake(st.session_state.snake, st.session_state.direction)
        if new_snake[0] == st.session_state.food:
            st.session_state.snake = new_snake + [st.session_state.snake[-1]]
            st.session_state.score += 10
            st.session_state.food = generate_food(st.session_state.snake)
        else:
            st.session_state.snake = new_snake
        if check_collision(st.session_state.snake):
            st.session_state.game_over = True
        st.session_state.last_move_time = time.time()
        st.rerun()
elif not st.session_state.game_started:
    st.info("👆 点击 **开始游戏** 开始！")
    render_game()

st.markdown("---")
st.markdown("🎮 Created with Streamlit | W/A/S/D or buttons to control")
