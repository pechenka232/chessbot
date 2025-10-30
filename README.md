# Chess Bot 

> **Attention!**  
> All programs in this repository are intended **solely for educational purposes**, to explore computer vision, automation technologies, and for personal learning.  
> **I do not encourage using these bots for cheating or bypassing the rules on chess platforms such as Lichess or Chess.com!**  
> Use these tools only for self-development, experimentation, and playing against yourself.


## 1. `chess_screen_bot.py` — Auto-playing Bot

**Description:**  
A bot that plays online chess for the user directly via the screen.  
It recognizes the chessboard, detects the opponent's moves, and automatically makes moves using Stockfish by controlling the mouse with pyautogui.

**Features:**
- Works with any site (chess.com, lichess.org, etc.) as long as the whole board is visible.
- No API or site integration required.
- Board visualization, move highlighting.
- Flexible coordinate setup.

---

## 2. `chess_trainer_gui.py` — Chess Board Trainer

**Description:**  
A virtual chessboard with two modes:
- **Training mode:** You play against Stockfish, making moves manually, and the bot responds with the best move.
- **Opponent analysis mode:** You replay opponent's moves on the board, and Stockfish instantly selects the strongest reply—perfect for analyzing real games or simulating "bot vs. opponent" on two boards.

**Features:**
- Interactive Python GUI
- Fast move analysis and Stockfish replies
- Great for training, analysis, or simulating games

---

## 3. `stockfish_auto.py` — Stockfish vs Stockfish on the Board

**Description:**  
A fully automated mode where Stockfish plays against itself directly on an online board (e.g., on Lichess), using computer vision and interface automation technologies.  
The bot "watches" the game on the screen and makes moves for both sides, simulating a game between two engines.

**Features:**
- Plays without any API—just via the screen and mouse
- Fully automated "engine vs engine" games
- Useful for analysis, engine testing, and studying chess strategies

---

## Board Coordinates Setup

**Before using any of the bots, be sure to set the correct chessboard coordinates!**

Open the file [`chess_board_coords.py`](chess_board_coords.py)  
At the very top of the file you'll see a line like:
```python
BOARD_COORDS = (X0, Y0, X1, Y1)  # ← Specify here the coordinates of the top-left and bottom-right corners of your board
```
- Point your mouse at the relevant corners of the chessboard on your site and enter those values.
- Save the file.
- These coordinates are used by all the main scripts!

---

## Installation & Launch

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/pechenka232/chess-screen-bot.git
   cd chess-screen-bot
   ```

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Stockfish:**  
   - [Official Stockfish Page](https://stockfishchess.org/download/)

4. **Set up board coordinates** in `chess_board_coords.py` as described above.

5. **Run the desired script:**  
   ```bash
   python chess_screen_bot.py         # auto-playing bot
   python chess_trainer_gui.py        # chess board trainer
   python stockfish_auto.py           # Stockfish vs Stockfish on the board
   ```

---

## FAQ

- **What are these bots for?**  
  For studying computer vision, automation, chess learning, creating your own chess tools, and personal training.

- **Can I use them on chess sites?**  
  Only for personal learning! Not recommended for unfair play.

- **The bot doesn't see pieces or the board?**  
  Check the coordinates in `chess_board_coords.py`, try changing the site theme, or increase your screen brightness.

- **Where can I get Stockfish?**  
  [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
