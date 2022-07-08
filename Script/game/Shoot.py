import time
import win32api, win32con

START_POS = 675, 650
START_TIME_DELAY = 3.5
DOWN_POS = 675, 650
UP_POS = 675, 500
SHOOT_TIME_DALAY = 0.24

win32api.SetCursorPos(START_POS)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, START_POS[0], START_POS[1], 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, START_POS[0], START_POS[1], 0, 0)
time.sleep(START_TIME_DELAY)

def shoot(move_x, move_y, power):
    win32api.SetCursorPos(DOWN_POS)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, DOWN_POS[0], DOWN_POS[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y, 0, 0)
    time.sleep(power)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, UP_POS[0], UP_POS[1], 0, 0)
    time.sleep(SHOOT_TIME_DALAY)

for shooting in range(0, 12):
        shoot(0, -45, 0)