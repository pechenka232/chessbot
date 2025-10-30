import tkinter as tk
import chess
import chess.engine
import random

ROWS, COLS = 8, 8
CELL_SIZE = 64
WHITE_COLOR = "#EEEED2"
BLACK_COLOR = "#769656"
PIECE_NAMES = {
    "K": "King",
    "Q": "Queen",
    "R": "Rook",
    "B": "Bishop",
    "N": "Knight",
    "P": "Pawn"
}

ENGINE_PATH = r"C:\Users\user\Desktop\chess\stockfish\stockfish-windows-x86-64-avx2.exe"

OPENINGS = {
    "Auto": [],
    "Beaver's Claw (B)": ["h4"],
    "Coffin Opening (G)": ["h4"],
    "Sicilian Defense (S)": ["e4", "c5"],
    "Caro–Kann Defense (K)": ["e4", "c6"],
    "Queen's Gambit (Q)": ["d4", "d5", "c4"],
    "King's Gambit (R)": ["e4", "e5", "f4"],
}

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

BOT_COLOR = chess.BLACK
MODE = "ideal"
chosen_opening_key = "Auto"
opening_moves = []
opening_index = 0

selected_square = None
highlighted_moves = []
move_history = []

root = tk.Tk()
root.title("Chess Trainer (Bot always at the bottom)")

settings_frame = tk.Frame(root, padx=10, pady=10)
settings_frame.pack(side=tk.TOP, fill=tk.X)

tk.Label(settings_frame, text="Select bot color:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
bot_color_var = tk.StringVar(value="b")
tk.Radiobutton(settings_frame, text="Black (bot at bottom)", variable=bot_color_var, value="b").grid(row=0, column=1)
tk.Radiobutton(settings_frame, text="White (bot at bottom)", variable=bot_color_var, value="w").grid(row=0, column=2)

tk.Label(settings_frame, text="Select level:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
mode_var = tk.StringVar(value="ideal")
tk.Radiobutton(settings_frame, text="Ideal (I)", variable=mode_var, value="ideal").grid(row=1, column=1)
tk.Radiobutton(settings_frame, text="Strong (S)", variable=mode_var, value="strong").grid(row=1, column=2)

tk.Label(settings_frame, text="Select opening:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
opening_var = tk.StringVar(value="Auto")
col = 1
for key in OPENINGS.keys():
    tk.Radiobutton(settings_frame, text=key, variable=opening_var, value=key).grid(row=2 + col//4, column=(col-1)%4, sticky="w")
    col += 1

start_button = tk.Button(settings_frame, text="Start", font=("Arial", 12, "bold"), bg="#8fbc8f")
start_button.grid(row=5, column=0, columnspan=3, pady=8)

main_frame = tk.Frame(root)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
canvas.pack(side=tk.LEFT)

right_panel = tk.Frame(main_frame)
right_panel.pack(side=tk.RIGHT, fill=tk.Y)

undo_btn = tk.Button(right_panel, text="↩ Undo", width=12, command=lambda: undo_move())
undo_btn.pack(pady=6)

new_game_btn = tk.Button(right_panel, text="♻ New Game", width=12, command=lambda: new_game())
new_game_btn.pack(pady=6)

status_label = tk.Label(root, text="Status: waiting to start", font=("Arial", 12))
status_label.pack(pady=6)

def coord_to_canvas(file, rank):
    if BOT_COLOR == chess.WHITE:
        x = file * CELL_SIZE + CELL_SIZE//2
        y = (7 - rank) * CELL_SIZE + CELL_SIZE//2
    else:
        x = (7 - file) * CELL_SIZE + CELL_SIZE//2
        y = rank * CELL_SIZE + CELL_SIZE//2
    return x, y

def canvas_to_square(col, row):
    if BOT_COLOR == chess.WHITE:
        file = col
        rank = 7 - row
    else:
        file = 7 - col
        rank = row
    return chess.square(file, rank)

def draw_board():
    canvas.delete("square")
    for r in range(ROWS):
        for c in range(COLS):
            x1 = c*CELL_SIZE; y1 = r*CELL_SIZE
            x2 = x1 + CELL_SIZE; y2 = y1 + CELL_SIZE
            color = WHITE_COLOR if (r+c)%2==0 else BLACK_COLOR
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")
    for m in highlighted_moves:
        x,y = coord_to_canvas(chess.square_file(m.to_square), chess.square_rank(m.to_square))
        canvas.create_rectangle(x-CELL_SIZE//2, y-CELL_SIZE//2, x+CELL_SIZE//2, y+CELL_SIZE//2, outline="#ff3333", width=3, tags="square")

def draw_pieces():
    canvas.delete("piece")
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            x,y = coord_to_canvas(chess.square_file(sq), chess.square_rank(sq))
            color = "white" if piece.color==chess.WHITE else "black"
            canvas.create_oval(x-26, y-26, x+26, y+26, fill=color, tags="piece")
            txt = PIECE_NAMES[piece.symbol().upper()]
            canvas.create_text(x, y, text=txt, fill="black" if color=="white" else "white", font=("Arial", 14, "bold"), tags="piece")

def update_status():
    txt = f"Mode: {MODE.upper()} | Opening: {chosen_opening_key} | Turn: {'White' if board.turn==chess.WHITE else 'Black'}"
    status_label.config(text=txt)

def on_click(event):
    global selected_square, highlighted_moves
    if board.is_game_over():
        return
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    clicked = canvas_to_square(col, row)
    piece = board.piece_at(clicked)
    if board.turn == BOT_COLOR:
        return

    if selected_square is not None:
        chosen = None
        for m in [m for m in board.legal_moves if m.from_square == selected_square]:
            if m.to_square == clicked:
                chosen = m
                break
        if chosen:
            move_history.append(board.fen())
            board.push(chosen)
            selected_square = None
            highlighted_moves.clear()
            draw_board(); draw_pieces(); update_status()
            root.after(200, bot_move)
        else:
            selected_square = None
            highlighted_moves.clear()
            draw_board(); draw_pieces()
    else:
        if piece and piece.color != BOT_COLOR:
            selected_square = clicked
            highlighted_moves[:] = [m for m in board.legal_moves if m.from_square == selected_square]
            draw_board(); draw_pieces()

def bot_move():
    global opening_index, opening_moves
    if board.is_game_over() or board.turn != BOT_COLOR:
        update_status()
        return
    move_history.append(board.fen())

    if opening_moves:
        san = opening_moves.pop(0)
        try:
            m = board.parse_san(san)
            board.push(m)
            draw_board(); draw_pieces(); update_status()
            return
        except:
            opening_moves = []

    try:
        if MODE == "ideal":
            res = engine.play(board, chess.engine.Limit(time=0.35))
            board.push(res.move)
        else:
            info = engine.analyse(board, chess.engine.Limit(depth=12), multipv=3)
            safe_moves = []
            best_eval = info[0]['score'].white().score(mate_score=10000) if BOT_COLOR == chess.WHITE else info[0]['score'].black().score(mate_score=10000)
            for i in info:
                mv = i["pv"][0]
                score = i['score'].white().score(mate_score=10000) if BOT_COLOR == chess.WHITE else i['score'].black().score(mate_score=10000)
                if best_eval - score <= 200:
                    safe_moves.append(mv)
            if safe_moves and random.random() < 0.3:
                mv = random.choice(safe_moves)
            else:
                mv = info[0]["pv"][0]
            board.push(mv)
    except:
        res = engine.play(board, chess.engine.Limit(time=0.35))
        board.push(res.move)

    draw_board(); draw_pieces(); update_status()

def undo_move():
    global move_history
    if not move_history:
        return
    last = move_history.pop()
    try:
        board.set_fen(last)
    except:
        pass
    draw_board(); draw_pieces(); update_status()

def new_game():
    global board, move_history, selected_square, highlighted_moves
    board.reset()
    move_history.clear()
    selected_square = None
    highlighted_moves.clear()
    settings_frame.pack(side=tk.TOP, fill=tk.X)
    draw_board(); draw_pieces(); update_status()

def start_game():
    global BOT_COLOR, MODE, chosen_opening_key, opening_moves, opening_index
    BOT_COLOR = chess.WHITE if bot_color_var.get() == "w" else chess.BLACK
    MODE = mode_var.get()
    chosen_opening_key = opening_var.get()
    opening_moves = OPENINGS.get(chosen_opening_key, []).copy()
    opening_index = 0

    settings_frame.forget()
    draw_board(); draw_pieces(); update_status()
    if board.turn == BOT_COLOR:
        root.after(200, bot_move)

start_button.config(command=start_game)

canvas.bind("<Button-1>", on_click)
root.bind("<Escape>", lambda e: root.quit())

draw_board(); draw_pieces(); update_status()
root.mainloop()
engine.quit()
