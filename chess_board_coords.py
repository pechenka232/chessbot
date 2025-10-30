import pyautogui
import time

# =========================================
# Chess Board Coordinate Finder
# =========================================
# This program helps you find the screen coordinates of your chessboard corners.
# You will use these coordinates later in your bot programs.
#
# Steps:
# 1. Run this script.
# 2. Move your mouse to the top-left square (h8) of your chessboard and wait 3 seconds.
# 3. Move your mouse to the bottom-right square (a1) of your chessboard and wait 3 seconds.
# 4. The program will print the coordinates for both squares.
# =========================================

print("Move your mouse to the top-left corner of the board (h8) and wait 3 seconds...")
time.sleep(3)
x0, y0 = pyautogui.position()
print(f"Coordinates of h8: x={x0}, y={y0}")

print("Now move your mouse to the bottom-right corner of the board (a1) and wait 3 seconds...")
time.sleep(3)
x1, y1 = pyautogui.position()
print(f"Coordinates of a1: x={x1}, y={y1}")

print("\nYou can now use these coordinates in your chess bot code for proper screen capture.")
