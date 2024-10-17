import random
import tkinter as tk
from tkinter import messagebox, PhotoImage
import time

def create_board(size, mines):
    board = [[("0", False, False) for _ in range(size)] for _ in range(size)]
    mine_positions = set()
    
    while len(mine_positions) < mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        mine_positions.add((row, col))
    
    for (row, col) in mine_positions:
        board[row][col] = ("M", False, False)
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < size and 0 <= c < size and board[r][c][0] != "M":
                    board[r][c] = (str(int(board[r][c][0]) + 1), False, False)
                    
    return board

def reveal_cell(board, row, col):
    if board[row][col][1] or board[row][col][2]:
        return
    
    board[row][col] = (board[row][col][0], True, False)
    if board[row][col][0] == "0":
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < len(board) and 0 <= c < len(board[0]):
                    reveal_cell(board, r, c)

def check_win(board):
    for row in board:
        for cell in row:
            if cell[0] != "M" and not cell[1]:
                return False
    return True

def on_cell_click(row, col, buttons, board, size, mines, mine_count_label, start_time, timer_label, root):
    if board[row][col][2]:
        return
    
    if board[row][col][0] == "M":
        for r in range(size):
            for c in range(size):
                buttons[r][c].config(text=board[r][c][0], state=tk.DISABLED, disabledforeground="red", bg="#ff6666")
        messagebox.showinfo("Game Over", "BOOM! You hit a mine!")
    else:
        reveal_cell(board, row, col)
        for r in range(size):
            for c in range(size):
                if board[r][c][1]:
                    buttons[r][c].config(text=board[r][c][0], state=tk.DISABLED, disabledforeground="black", bg="#d3d3d3")
        if check_win(board):
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            messagebox.showinfo("Congratulations", f"You've cleared the board in {elapsed_time} seconds!")
            for r in range(size):
                for c in range(size):
                    buttons[r][c].config(state=tk.DISABLED)
    update_timer(timer_label, start_time, root)

def on_right_click(event, row, col, buttons, board, mine_count_label, mines_left):
    if not board[row][col][1]:
        if not board[row][col][2]:
            board[row][col] = (board[row][col][0], board[row][col][1], True)
            buttons[row][col].config(text="⚑", fg="#4169e1", font=("Helvetica", 14, "bold"), bg="#f0e68c")
            mines_left[0] -= 1
        else:
            board[row][col] = (board[row][col][0], board[row][col][1], False)
            buttons[row][col].config(text="", bg="#e0e0e0")
            mines_left[0] += 1
        mine_count_label.config(text=f"Mines Left: {mines_left[0]}")

def update_timer(timer_label, start_time, root):
    elapsed_time = int(time.time() - start_time)
    timer_label.config(text=f"Time: {elapsed_time} s")
    root.after(1000, update_timer, timer_label, start_time, root)

def give_hint(board, buttons, size):
    for r in range(size):
        for c in range(size):
            if board[r][c][0] != "M" and not board[r][c][1] and not board[r][c][2]:
                buttons[r][c].config(bg="#32cd32", relief=tk.SUNKEN, font=("Helvetica", 14, "bold"))  # Highlight the cell as a hint
                buttons[r][c].after(1000, lambda r=r, c=c: buttons[r][c].config(bg="#e0e0e0", relief=tk.RAISED, font=("Helvetica", 14)))  # Revert back after 1 second
                return

def start_game(size, mines):
    board = create_board(size, mines)
    mines_left = [mines]
    
    root = tk.Tk()
    root.title("Minesweeper")
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)
    
    start_time = time.time()
    
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(pady=10)
    label = tk.Label(top_frame, text="Minesweeper Game", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333333")
    label.pack()
    
    mine_count_label = tk.Label(top_frame, text=f"Mines Left: {mines_left[0]}", font=("Helvetica", 14), bg="#f0f0f0", fg="#333333")
    mine_count_label.pack()
    
    timer_label = tk.Label(top_frame, text="Time: 0 s", font=("Helvetica", 14), bg="#f0f0f0", fg="#333333")
    timer_label.pack()
    
    board_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
    board_frame.pack()
    
    buttons = [[None for _ in range(size)] for _ in range(size)]
    for r in range(size):
        for c in range(size):
            button = tk.Button(board_frame, text="", width=3, height=1, font=("Helvetica", 14), relief=tk.RAISED, bg="#e0e0e0", 
                               command=lambda r=r, c=c: on_cell_click(r, c, buttons, board, size, mines, mine_count_label, start_time, timer_label, root))
            button.grid(row=r, column=c, padx=2, pady=2)
            button.bind("<Button-3>", lambda event, r=r, c=c: on_right_click(event, r, c, buttons, board, mine_count_label, mines_left))
            buttons[r][c] = button
    
    hint_button = tk.Button(root, text="Give Hint", command=lambda: give_hint(board, buttons, size), font=("Helvetica", 14, "bold"), bg="#ffa07a", fg="white", activebackground="#ff6347", activeforeground="white")
    hint_button.pack(pady=10)
    
    reset_button = tk.Button(root, text="Reset Game", command=lambda: [root.destroy(), play_minesweeper()], font=("Helvetica", 14, "bold"), bg="#87ceeb", fg="white", activebackground="#4682b4", activeforeground="white")
    reset_button.pack(pady=10)
    
    update_timer(timer_label, start_time, root)
    
    root.mainloop()

def play_minesweeper():
    def set_difficulty(level):
        if level == "Easy":
            start_game(size=8, mines=10)
        elif level == "Medium":
            start_game(size=12, mines=25)
        elif level == "Hard":
            start_game(size=16, mines=40)
        root.destroy()
    
    root = tk.Tk()
    root.title("Minesweeper")
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)
    
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(pady=10)
    label = tk.Label(top_frame, text="Select Difficulty", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333333")
    label.pack()
    
    easy_button = tk.Button(top_frame, text="Easy", command=lambda: set_difficulty("Easy"), font=("Helvetica", 14), bg="#98fb98", width=10)
    easy_button.pack(pady=5)
    
    medium_button = tk.Button(top_frame, text="Medium", command=lambda: set_difficulty("Medium"), font=("Helvetica", 14), bg="#ffd700", width=10)
    medium_button.pack(pady=5)
    
    hard_button = tk.Button(top_frame, text="Hard", command=lambda: set_difficulty("Hard"), font=("Helvetica", 14), bg="#ff4500", width=10)
    hard_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    play_minesweeper()