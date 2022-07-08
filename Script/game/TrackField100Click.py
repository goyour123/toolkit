import win32api, win32con
import time

left_pos = 655, 605
right_pos = 755, 580
time_delay = 0.03

def running ():
    win32api.SetCursorPos(left_pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, left_pos[0], left_pos[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, left_pos[0], left_pos[1], 0, 0)
    time.sleep(time_delay)
    win32api.SetCursorPos(right_pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, right_pos[0], right_pos[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, right_pos[0], right_pos[1], 0, 0)
    time.sleep(time_delay)

for times in range(0, 135):
    running()
