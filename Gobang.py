import tkinter as tk
from tkinter import messagebox


# 初始化棋盘
def init_board(size=15):
    return [['.' for _ in range(size)] for _ in range(size)]


# 检查是否获胜
def check_win(board, player):
    size = len(board)

    # 检查横向、纵向和斜向
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                # 检查横向
                if j + 4 < size and all(board[i][j + k] == player for k in range(5)):
                    return True
                # 检查纵向
                if i + 4 < size and all(board[i + k][j] == player for k in range(5)):
                    return True
                # 检查斜向（左上到右下）
                if i + 4 < size and j + 4 < size and all(board[i + k][j + k] == player for k in range(5)):
                    return True
                # 检查斜向（右上到左下）
                if i + 4 < size and j - 4 >= 0 and all(board[i + k][j - k] == player for k in range(5)):
                    return True
    return False


# 更新图形界面上的棋盘
def draw_board():
    for row in range(board_size):
        for col in range(board_size):
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            if board[row][col] == 'X':
                canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill='black')
            elif board[row][col] == 'O':
                canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill='white')


# 游戏主逻辑
def play_game():
    global root, canvas, board, turn, board_size, cell_size

    # 游戏设置
    board_size = 15  # 棋盘大小
    cell_size = 30  # 每个格子的大小
    board = init_board(board_size)
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
    while True:
        # 显示当前棋盘状态
        print_board(board)

        # 获取玩家输入
        player = 'X' if turn % 2 == 0 else 'O'
        print(f"玩家 {player} 的回合，请输入坐标（行 列）")

        try:
            row, col = map(int, input("请输入行列（空格分开）: ").split())
        except ValueError:
            print("输入无效，请重新输入。")
            continue

        # 检查坐标是否合法
        if 0 <= row < len(board) and 0 <= col < len(board) and board[row][col] == '.':
            board[row][col] = player
        else:
            print("无效的坐标，请重新输入。")
            continue

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
