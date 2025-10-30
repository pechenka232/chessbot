import chess
import chess.engine
import pyautogui
import numpy as np
import cv2
import time

# Board coordinates on the screen (top-left and bottom-right corners) Go to and measure the coordinates chess_board_coords.py
X0, Y0 = 579, 200  # upper left corner of the board(h8)
X1, Y1 = 1263, 840  # lower right corner of the board (a1)
BOARD_WIDTH = X1 - X0
BOARD_HEIGHT = Y1 - Y0
CELL_WIDTH = BOARD_WIDTH // 8
CELL_HEIGHT = BOARD_HEIGHT // 8

# Path to the Stockfish engine executable
# Replace the path below with the location where you have Stockfish installed on your computer
engine_path = r"C:\Users\user\Desktop\chess\stockfish\stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

BOT_COLOR = input("Choose bot color (w/b): ").strip().lower()
bot_turn = chess.WHITE if BOT_COLOR == "w" else chess.BLACK

board = chess.Board()

def get_board_screenshot():
    img = pyautogui.screenshot(region=(X0, Y0, BOARD_WIDTH, BOARD_HEIGHT))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def draw_grid(img, highlights=None):
    for i in range(9):
        cv2.line(img, (i * CELL_WIDTH, 0), (i * CELL_WIDTH, BOARD_HEIGHT), (0, 255, 0), 1)
        cv2.line(img, (0, i * CELL_HEIGHT), (BOARD_WIDTH, i * CELL_HEIGHT), (0, 255, 0), 1)
    if highlights:
        for color, (r, c) in highlights:
            x, y = c * CELL_WIDTH, r * CELL_HEIGHT
            col = (0, 0, 255) if color == "from" else (255, 0, 0)
            cv2.rectangle(img, (x, y), (x + CELL_WIDTH, y + CELL_HEIGHT), col, 2)
    return img

def get_piece_mask(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.4, beta=10)

    adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 15, 8)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 80])
    mask_dark = cv2.inRange(hsv, lower_dark, upper_dark)

    lower_bright = np.array([0, 0, 190])
    upper_bright = np.array([180, 50, 255])
    mask_bright = cv2.inRange(hsv, lower_bright, upper_bright)

    mask = cv2.bitwise_or(adapt, mask_dark)
    mask = cv2.bitwise_or(mask, mask_bright)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 3)
    return mask

def detect_player_move(prev_img, curr_img, base_threshold=0.008):
    prev_mask = get_piece_mask(prev_img)
    curr_mask = get_piece_mask(curr_img)
    diff = cv2.absdiff(prev_mask, curr_mask)

    total_change = np.sum(diff > 0) / diff.size
    threshold = max(base_threshold * (0.5 + total_change * 10), 0.006)

    changed = []
    for r in range(8):
        for c in range(8):
            y, x = r * CELL_HEIGHT, c * CELL_WIDTH
            cell = diff[y:y + CELL_HEIGHT, x:x + CELL_WIDTH]
            ratio = np.sum(cell > 0) / (CELL_WIDTH * CELL_HEIGHT)
            if ratio > threshold:
                changed.append((r, c))

    if len(changed) >= 2:
        (r1, c1), (r2, c2) = changed[0], changed[-1]
        if BOT_COLOR == "w":
            move_from = chess.square(c1, 7 - r1)
            move_to = chess.square(c2, 7 - r2)
        else:
            move_from = chess.square(7 - c1, r1)
            move_to = chess.square(7 - c2, r2)
        move = chess.Move(move_from, move_to)
        if move in board.legal_moves:
            return move, changed
    return None, changed

def make_move(move):
    start_file = chess.square_file(move.from_square)
    start_rank = chess.square_rank(move.from_square)
    end_file = chess.square_file(move.to_square)
    end_rank = chess.square_rank(move.to_square)

    if BOT_COLOR == "b":
        start_file = 7 - start_file
        start_rank = 7 - start_rank
        end_file = 7 - end_file
        end_rank = 7 - end_rank

    start_x = X0 + start_file * CELL_WIDTH + CELL_WIDTH // 2
    start_y = Y0 + (7 - start_rank) * CELL_HEIGHT + CELL_HEIGHT // 2
    end_x = X0 + end_file * CELL_WIDTH + CELL_WIDTH // 2
    end_y = Y0 + (7 - end_rank) * CELL_HEIGHT + CELL_HEIGHT // 2

    pyautogui.moveTo(start_x, start_y, duration=0.05)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.05)
    pyautogui.mouseUp()

print("Bot started. Preparing for 3 seconds...")
time.sleep(3)

prev_img = get_board_screenshot()
cv2.namedWindow("Board Grid", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Board Grid", 600, 600)
cv2.resizeWindow("Mask", 400, 400)

try:
    while not board.is_game_over():
        curr_img = get_board_screenshot()
        mask = get_piece_mask(curr_img)
        cv2.imshow("Mask", mask)

        move_highlights = []
        if board.turn != bot_turn:
            move, changed = detect_player_move(prev_img, curr_img)
            move_highlights = [("from", c) for c in changed]
            if move:
                san = board.san(move)
                board.push(move)
                print("Player move:", san)

        if board.turn == bot_turn:
            result = engine.play(board, chess.engine.Limit(time=0.2))
            bot_move = result.move
            san_bot = board.san(bot_move)
            board.push(bot_move)
            print("Bot move:", san_bot)
            make_move(bot_move)

        prev_img = curr_img
        cv2.imshow("Board Grid", draw_grid(curr_img.copy(), move_highlights))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.05)

finally:
    engine.quit()
    cv2.destroyAllWindows()


