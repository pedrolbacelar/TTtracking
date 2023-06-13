import pyautogui
import time

def move_mouse():
    while True:
        pyautogui.moveRel(0, 1, duration=1)  # Move the cursor 1 pixel down
        time.sleep(1)
        pyautogui.moveRel(0, -1, duration=1)  # Move the cursor back up
        time.sleep(5)  # Wait for 5 minutes

move_mouse()
