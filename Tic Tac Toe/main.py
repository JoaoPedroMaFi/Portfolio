import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import random
import pygame  # Import pygame for sound

# Initialize pygame mixer
pygame.mixer.init()

# Load victory sounds
win_sound = "sound/win_sound.mp3"  # Make sure the file exists in your project directory
los_sound = "sound/lose.wav"
draw_sound = "sound/draw.ogg"

# Create the main window
window = tk.Tk()
window.title("Tic Tac Toe")
window.configure(bg="lightgray")
window.geometry("313x450")  # Fixed window size
window.resizable(False, False)  # Prevent resizing

difficulty = "Easy"  # Default choice

# Font definitions
highlightFont = font.Font(family='Helvetica', size=12, weight='bold')
scoreFont = font.Font(family='Helvetica', size=16, weight='bold')  # Larger font for the score

# Load images
o_img = Image.open("images/o.png").resize((74, 80))
o_photo = ImageTk.PhotoImage(o_img)

x_img = Image.open("images/x.png").resize((74, 80))
x_photo = ImageTk.PhotoImage(x_img)

# Game variables
current_player = "X"
board = [""] * 9
buttons = []
score = {"X": 0, "O": 0}
game_active = True  # Variable to prevent extra moves


# Function to check the winner
def check_winner():
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]
    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a], (a, b, c)
    if "" not in board:
        return "Draw", []
    return None, []


# Highlight winning buttons
def highlight_winner(positions):
    for pos in positions:
        buttons[pos].config(bg="lightgreen")


# Update the score
def update_score():
    score_value_label.config(text=f"{score['X']}  -  {score['O']}")


# Play victory sound
def play_win_sound():
    pygame.mixer.music.load(win_sound)
    pygame.mixer.music.play()


def play_los_sound():
    pygame.mixer.music.load(los_sound)
    pygame.mixer.music.play()


def play_draw_sound():
    pygame.mixer.music.load(draw_sound)
    pygame.mixer.music.play()


# Reset game
def reset_game():
    global board, current_player, game_active
    pygame.mixer.music.stop()
    board = [""] * 9
    current_player = "X"
    game_active = True
    for bttn in buttons:
        bttn.config(image="", bg="white", width=10, height=5)


# Function to set difficulty
def set_difficulty(level):
    global difficulty
    difficulty = level


# Create difficulty selection frame
difficulty_frame = tk.Frame(window, bg="lightgray")
difficulty_frame.grid(row=2, column=0, columnspan=3, pady=10)

# Create difficulty buttons
easy_button = tk.Button(difficulty_frame, text="Easy", font=highlightFont, command=lambda: set_difficulty("Easy"))
easy_button.grid(row=2, column=0, padx=5)

medium_button = tk.Button(difficulty_frame, text="Medium", font=highlightFont, command=lambda: set_difficulty("Medium"))
medium_button.grid(row=2, column=1, padx=5)

hard_button = tk.Button(difficulty_frame, text="Hard", font=highlightFont, command=lambda: set_difficulty("Hard"))
hard_button.grid(row=2, column=2, padx=5)

# Create information panel (score and players)
info_frame = tk.Frame(window, bg="lightgray")
info_frame.grid(row=1, column=0, columnspan=3, pady=10)

# Create player labels
player1_label = tk.Label(info_frame, text="Player 1\nX", font=highlightFont, bg="blue", fg="white", padx=20, pady=5)
player1_label.grid(row=1, column=0, padx=10)

player2_label = tk.Label(info_frame, text="Player 2\nO", font=highlightFont, bg="red", fg="white", padx=20, pady=5)
player2_label.grid(row=1, column=2, padx=10)

# Create "Score" label adjusting the correct position
score_label = tk.Label(info_frame, text="Score", font=highlightFont, bg="lightgray")
score_label.grid(row=1, column=1, pady=(0, 0), rowspan=1, sticky="N")

# Create the highlighted score and position it correctly
score_value_label = tk.Label(info_frame, text=f"{score['X']}  -  {score['O']}", font=scoreFont, bg="lightgray")
score_value_label.grid(row=1, column=1, pady=(0, 0), sticky="S")


# Minimax function to decide the best move
def minimax(board_, depth, is_maximizing):
    winner, _ = check_winner()

    # Assign scores for each outcome
    if winner == "O":  # Computer wins
        return 10 - depth
    elif winner == "X":  # Player wins
        return depth - 10
    elif "" not in board_:  # Draw
        return 0

    if is_maximizing:  # Computer's turn (maximize score)
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score_ = minimax(board, depth + 1, False)  # Simulate opponent's move
                board[i] = ""  # Undo move
                best_score = max(score_, best_score)
        return best_score
    else:  # Player's turn (minimize score)
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score_ = minimax(board, depth + 1, True)  # Simulate computer's move
                board[i] = ""  # Undo move
                best_score = min(score_, best_score)
        return best_score


# Modify computer move to use Minimax
def computer_play():
    global game_active, current_player
    if not game_active:
        return

    empty_cells = [i for i in range(9) if board[i] == ""]

    if difficulty == "Easy":
        # Choose a random move
        best_move = random.choice(empty_cells)
    elif difficulty == "Medium":
        if random.random() < 0.4:  # 40% chance to make a mistake
            best_move = random.choice(empty_cells)
        else:
            best_move = get_best_move()
    else:  # "Hard" (Perfect Minimax)
        best_move = get_best_move()

    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move].config(image=o_photo, compound="center", width=74, height=80)
        buttons[best_move].image = o_photo

        winner, positions = check_winner()
        if winner:
            game_active = False
            if winner == "Draw":
                play_draw_sound()
                messagebox.showinfo("Game Over", "Draw!")
            else:
                highlight_winner(positions)
                score[winner] += 1
                winner_name = "Player 1" if winner == "X" else "Player 2"
                if winner_name == "Player 1":
                    play_win_sound()
                else:
                    play_los_sound()
                messagebox.showinfo("Game Over", f"{winner_name} won!")
                update_score()
            reset_game()
        else:
            current_player = "X"


def get_best_move():
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score_ = minimax(board, 0, False)
            board[i] = ""
            if score_ > best_score:
                best_score = score_
                best_move = i
    return best_move


# Player move
def play(index):
    global current_player, game_active
    if board[index] == "" and game_active and current_player == "X":
        board[index] = "X"
        buttons[index].config(image=x_photo, compound="center", width=74, height=80)
        buttons[index].image = x_photo

        winner, positions = check_winner()
        if winner:
            game_active = False
            if winner == "Draw":
                play_draw_sound()
                messagebox.showinfo("Game Over", "Draw!")
            else:
                highlight_winner(positions)
                score[winner] += 1
                winner_name = "Player 1" if winner == "X" else "Player 2"
                if winner_name == "Player 1":
                    play_win_sound()  # Play sound on victory
                else:
                    play_los_sound()
                messagebox.showinfo("Game Over", f"{winner_name} won!")
                update_score()
            reset_game()
            return  # If the game is over, do not let the computer play

        # Computer plays if the game is still ongoing
        current_player = "O"
        window.after(500, computer_play)  # Small delay to simulate thinking


# Create board buttons
board_frame = tk.Frame(window, bg="lightgray")
board_frame.grid(row=0, column=0, columnspan=3, pady=20)
for i in range(9):
    button = tk.Button(board_frame, width=10, height=5, bg="white", command=lambda i=i: play(i))
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)

# Create information panel (score and players)
info_frame = tk.Frame(window, bg="lightgray")
info_frame.grid(row=1, column=0, columnspan=3, pady=10)

# Create player labels
player1_label = tk.Label(info_frame, text="Player 1\nX", font=highlightFont, bg="blue", fg="white", padx=20, pady=5)
player1_label.grid(row=1, column=0, padx=10)
player2_label = tk.Label(info_frame, text="Player 2\nO", font=highlightFont, bg="red", fg="white", padx=20, pady=5)
player2_label.grid(row=1, column=2, padx=10)

# Create "Score" label adjusting the correct position
score_label = tk.Label(info_frame, text="Score", font=highlightFont, bg="lightgray")
score_label.grid(row=1, column=1, pady=(0, 0), rowspan=1, sticky="N")

# Create the highlighted score and position it correctly
score_value_label = tk.Label(info_frame, text=f"{score['X']}  -  {score['O']}", font=scoreFont, bg="lightgray")
score_value_label.grid(row=1, column=1, pady=(0, 0), sticky="S")

# Start the GUI
window.mainloop()
