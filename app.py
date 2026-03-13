import streamlit as st
import random
import time

# 页面配置
st.set_page_config(page_title="🐍 贪吃蛇游戏", page_icon="🐍", layout="centered")

# 初始化游戏状态
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direction = 'RIGHT'
    st.session_state.food = (10, 10)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.speed = 0.5

# 游戏区域大小
GRID_SIZE = 20

def generate_food(snake):
    """生成不在蛇身上的食物"""
    while True:
        food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if food not in snake:
            return food

def move_snake(snake, direction):
    """移动蛇"""
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
    """检查是否撞到自己"""
    return snake[0] in snake[1:]

# 标题
st.title("🐍 贪吃蛇游戏")
st.markdown("### 经典贪吃蛇 - 网页版")

# 控制说明
st.markdown("""
**控制方法：**
- ⬆️ 上 - `W` 或 `↑`
- ⬇️ 下 - `S` 或 `↓`
- ⬅️ 左 - `A` 或 `←`
- ➡️ 右 - `D` 或 `→`
- 🎮 或使用屏幕按钮
""")

# 游戏控制区域
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 方向控制按钮
    st.markdown("#### 游戏控制")
    
    # 上
    up_col = st.columns([1, 1, 1])
    with up_col[1]:
        if st.button("⬆️", key="up"):
            if st.session_state.direction != 'DOWN':
                st.session_state.direction = 'UP'
    
    # 中排：左、开始/重置、右
    mid_col = st.columns([1, 1, 1])
    with mid_col[0]:
        if st.button("⬅️", key="left"):
            if st.session_state.direction != 'RIGHT':
                st.session_state.direction = 'LEFT'
    
    with mid_col[1]:
        if not st.session_state.game_started:
            if st.button("🎮 开始游戏", key="start"):
                st.session_state.game_started = True
                st.session_state.game_over = False
                st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
                st.session_state.direction = 'RIGHT'
                st.session_state.food = generate_food(st.session_state.snake)
                st.session_state.score = 0
        elif st.session_state.game_over:
            if st.button("🔄 重新开始", key="restart"):
                st.session_state.game_started = True
                st.session_state.game_over = False
                st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
                st.session_state.direction = 'RIGHT'
                st.session_state.food = generate_food(st.session_state.snake)
                st.session_state.score = 0
        else:
            st.button("⏸️ 暂停", key="pause", disabled=True)
    
    with mid_col[2]:
        if st.button("➡️", key="right"):
            if st.session_state.direction != 'LEFT':
                st.session_state.direction = 'RIGHT'
    
    # 下
    down_col = st.columns([1, 1, 1])
    with down_col[1]:
        if st.button("⬇️", key="down"):
            if st.session_state.direction != 'UP':
                st.session_state.direction = 'DOWN'

# 速度控制
speed = st.slider("🐢 速度调节", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
st.session_state.speed = speed

# 显示分数
st.markdown(f"### 🏆 分数：**{st.session_state.score}**")

# 游戏结束提示
if st.session_state.game_over:
    st.error("💀 游戏结束！蛇撞到自己了！")
    st.markdown(f"### 最终分数：{st.session_state.score}")

# 渲染游戏区域
def render_game():
    grid = st.empty()
    
    # 创建游戏网格
    output = "<div style='display: grid; grid-template-columns: repeat(20, 20px); gap: 1px; padding: 10px; background: #1a1a2e; border-radius: 10px;'>"
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell = (row, col)
            if cell == st.session_state.snake[0]:
                # 蛇头 - 绿色
                output += "<div style='width: 20px; height: 20px; background: #00ff00; border-radius: 3px;'></div>"
            elif cell in st.session_state.snake:
                # 蛇身 - 深绿色
                output += "<div style='width: 20px; height: 20px; background: #00cc00; border-radius: 3px;'></div>"
            elif cell == st.session_state.food:
                # 食物 - 红色
                output += "<div style='width: 20px; height: 20px; background: #ff0000; border-radius: 50%;'></div>"
            else:
                # 空白 - 深色
                output += "<div style='width: 20px; height: 20px; background: #16213e; border-radius: 2px;'></div>"
    
    output += "</div>"
    grid.markdown(output, unsafe_allow_html=True)

# 游戏主循环
if st.session_state.game_started and not st.session_state.game_over:
    render_game()
    
    # 自动移动蛇
    placeholder = st.empty()
    
    # 使用 session_state 来追踪时间
    if 'last_move_time' not in st.session_state:
        st.session_state.last_move_time = time.time()
    
    current_time = time.time()
    
    if current_time - st.session_state.last_move_time >= st.session_state.speed:
        # 移动蛇
        new_snake = move_snake(st.session_state.snake, st.session_state.direction)
        
        # 检查是否吃到食物
        if new_snake[0] == st.session_state.food:
            st.session_state.snake = new_snake + [st.session_state.snake[-1]]
            st.session_state.score += 10
            st.session_state.food = generate_food(st.session_state.snake)
        else:
            st.session_state.snake = new_snake
        
        # 检查碰撞
        if check_collision(st.session_state.snake):
            st.session_state.game_over = True
        
        st.session_state.last_move_time = current_time
        st.rerun()
    
    render_game()
    
    # 键盘控制提示
    st.markdown("""
    <style>
    .stTextInput input {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 键盘控制
    key_press = st.text_input("🎹 键盘控制 (W/A/S/D)", max_chars=1, key="keyboard")
    if key_press:
        key = key_press.upper()
        if key == 'W' and st.session_state.direction != 'DOWN':
            st.session_state.direction = 'UP'
        elif key == 'S' and st.session_state.direction != 'UP':
            st.session_state.direction = 'DOWN'
        elif key == 'A' and st.session_state.direction != 'RIGHT':
            st.session_state.direction = 'LEFT'
        elif key == 'D' and st.session_state.direction != 'LEFT':
            st.session_state.direction = 'RIGHT'
        st.rerun()

elif not st.session_state.game_started:
    st.info("👆 点击 **开始游戏** 按钮开始玩！")
    # 显示初始网格
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.food = (10, 10)
    render_game()

# 页脚
st.markdown("---")
st.markdown("🎮 Created with Streamlit | 按 W/A/S/D 或屏幕按钮控制方向")
