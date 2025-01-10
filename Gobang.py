import time
import tkinter as tk
from tkinter import messagebox
import random

# 初始化棋盘
def init_board(size=15):
    # 使用 0 表示空位，1 表示 X，2 表示 O
    return [[0 for _ in range(size)] for _ in range(size)], [[None for _ in range(size)] for _ in range(size)]  # 新增一个二维列表存储落子顺序


# 检查是否获胜
def check_win(board, player):
    size = len(board)
    player_value = 1 if player == 'X' else 2

    # 检查横向、纵向和斜向
    for i in range(size):
        for j in range(size):
            if board[i][j] == player_value:
                # 检查横向
                if j + 4 < size and all(board[i][j + k] == player_value for k in range(5)):
                    return True
                # 检查纵向
                if i + 4 < size and all(board[i + k][j] == player_value for k in range(5)):
                    return True
                # 检查斜向（左上到右下）
                if i + 4 < size and j + 4 < size and all(board[i + k][j + k] == player_value for k in range(5)):
                    return True
                # 检查斜向（右上到左下）
                if i + 4 < size and j - 4 >= 0 and all(board[i + k][j - k] == player_value for k in range(5)):
                    return True
    return False


# 更新图形界面上的棋盘
def draw_board():
    for row in range(board_size):
        for col in range(board_size):
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            if board[row][col] == 1:
                canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill='black')  # X 由黑色表示
            elif board[row][col] == 2:
                canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill='white')  # O 由白色表示

            # 显示落子顺序
            if move_order[row][col] is not None:
                canvas.create_text(x, y, text=str(move_order[row][col]), fill="red", font=("Arial", 10, "bold"))


# 游戏主逻辑
def play_game():
    global root, canvas, board, move_order, turn, board_size, cell_size

    # 游戏设置
    board_size = 15  # 棋盘大小
    cell_size = 30  # 每个格子的大小
    board, move_order = init_board(board_size)  # 初始化棋盘和落子顺序
    turn = 0  # 轮流下棋

    # 创建窗口
    root = tk.Tk()
    root.title("五子棋")

    # 创建画布
    canvas = tk.Canvas(root, width=board_size * cell_size, height=board_size * cell_size)
    canvas.pack()

    # 绘制棋盘网格
    for i in range(board_size + 1):
        canvas.create_line(i * cell_size, 0, i * cell_size, board_size * cell_size)  # 竖线
        canvas.create_line(0, i * cell_size, board_size * cell_size, i * cell_size)  # 横线

    # 更新棋盘的初始状态
    draw_board()

    # 循环进行下棋
    move_number = 1  # 用来标记落子顺序
    while True:
        # 显示当前棋盘状态
        print_board(board)

        # 获取玩家输入
        player = 'X' if turn % 2 == 0 else 'O'
        print(f"玩家 {player} 的回合，系统随机选择位置")

        # 随机生成一个空白的坐标
        row, col = get_move()

        # 打印选择的坐标
        print(f"玩家 {player} 选择坐标：{row} {col}")

        # 更新棋盘
        board[row][col] = 1 if player == 'X' else 2
        move_order[row][col] = move_number  # 记录落子顺序
        move_number += 1  # 增加顺序号

        # 更新图形界面上的棋盘
        draw_board()

        # 检查是否获胜
        if check_win(board, player):
            print_board(board)
            print(f"玩家 {player} 获胜！")
            messagebox.showinfo("游戏结束", f"玩家 {player} 获胜！")
            root.quit()  # 退出游戏
            return

        # 切换玩家
        turn += 1


# 评估分数函数
def evaluate_score(board, player):
    size = len(board)
    score_board = [[0 for _ in range(size)] for _ in range(size)]  # 初始化一个分数矩阵

    player_value = 1 if player == 'X' else 2
    opponent_value = 2 if player == 'X' else 1

    # 四个方向：横向、纵向、左上到右下、右上到左下
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # 对每个空白位置进行评估
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:  # 只评估空白位置
                score = 0
                # 检查四个方向的分数
                for di, dj in directions:
                    for k in range(-4, 5):  # 扫描一个长度为9的范围
                        ni, nj = i + k * di, j + k * dj
                        if 0 <= ni < size and 0 <= nj < size:
                            if board[ni][nj] == player_value:
                                score += 1  # 增加分数
                            elif board[ni][nj] == opponent_value:
                                score -= 1  # 如果是对方棋子，减少分数
                score_board[i][j] = score  # 将计算出的分数放入分数矩阵
    return score_board


# 获取最佳落子位置
def get_move():
    # 获取当前玩家
    player = 'X' if turn % 2 == 0 else 'O'

    # 评估每个空白位置的分数
    score_board = evaluate_score(board, player)

    # 寻找分数最高的空白位置
    max_score = -float('inf')
    best_move = None

    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0 and score_board[i][j] > max_score:
                max_score = score_board[i][j]
                best_move = (i, j)

    return best_move


# 打印棋盘（命令行）
def print_board(board):
    print("  ", end="")
    for i in range(len(board)):
        print(f"{i:2}", end=" ")
    print()

    for i, row in enumerate(board):
        print(f"{i:2}", end=" ")
        for cell in row:
            print(cell, end=" ")
        print()


if __name__ == "__main__":
    play_game()
