import chess
import chess.engine
import pyautogui
import time

# Board coordinates on the screen (top-left and bottom-right corners) Go to and measure the coordinates chess_board_coords.py
X0, Y0 = 579, 200  # верхний левый угол доски (h8)
X1, Y1 = 1263, 840  # нижний правый угол доски (a1)
BOARD_WIDTH = X1 - X0
BOARD_HEIGHT = Y1 - Y0
CELL_WIDTH = BOARD_WIDTH // 8
CELL_HEIGHT = BOARD_HEIGHT // 8
HALF_W = CELL_WIDTH // 2
HALF_H = CELL_HEIGHT // 2

# Path to the Stockfish engine executable
# Replace the path below with the location where you have Stockfish installed on your computer
ENGINE_PATH = r"C:\Users\user\Desktop\шахматы\stockfish\stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


board = chess.Board()
print("♙♟ Stockfish играет сам за черных и белых на Lichess ♙♟")


def square_to_screen(square):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
 
    x = X0 + (7 - file) * CELL_WIDTH + HALF_W
    y = Y0 + rank * CELL_HEIGHT + HALF_H
    return int(x), int(y)


def perform_mouse_move(from_sq, to_sq):
    sx, sy = square_to_screen(from_sq)
    ex, ey = square_to_screen(to_sq)
    pyautogui.moveTo(sx, sy, duration=0.08)
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.moveTo(ex, ey, duration=0.08)
    pyautogui.mouseUp()


try:
    while not board.is_game_over():
        
        current_color = board.turn

       
        result = engine.play(board, chess.engine.Limit(time=0.5))
        move = result.move

        
        if move not in board.legal_moves:
            print("Недопустимый ход, пропускаем")
            break

       
        perform_mouse_move(move.from_square, move.to_square)

        board.push(move)

        
        if current_color == chess.WHITE:
            print(f"♙ Белые ходят: {move}")
        else:
            print(f"♟ Черные ходят: {move}")

        
        time.sleep(0.7)

finally:
    engine.quit()
    print("♟ Игра завершена.")


