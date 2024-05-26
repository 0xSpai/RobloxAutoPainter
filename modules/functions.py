import os
import time
import pygetwindow as gw
import psutil
import keyboard
import win32api
import win32con
import win32gui
import win32process
import modules.virtualkeystroke as vkey
from PIL import ImageGrab
from screeninfo import get_monitors

def setup_window(window_title="Roblox", exe_name="RobloxPlayerBeta.exe", width=1681, height=957):
    # Calculate screen resolution
    for m in get_monitors():
        screen_width, screen_height = m.width, m.height

    center_x, center_y = screen_width // 2, screen_height // 2

    roblox_windows = []
    # Get Roblox window
    for win in gw.getAllWindows():
        if win.title == window_title:
            class_name = win32gui.GetClassName(win._hWnd)
            if "Chrome_WidgetWin_1" not in class_name:
                _, pid = win32process.GetWindowThreadProcessId(win._hWnd)
                try:
                    process = psutil.Process(pid)
                    executable_path = process.exe()
                    # Check if the executable path belongs to Roblox
                    if exe_name in executable_path:
                        roblox_windows.append(win)
                except psutil.NoSuchProcess:
                    pass

    if not roblox_windows:
        print("Roblox window not found. Open Roblox and try again!")
        return None, None, None

    roblox_window = roblox_windows[0]
    if roblox_window.isMinimized:
        roblox_window.restore()

    roblox_window.resizeTo(width, height)
    roblox_window.moveTo(center_x - round(width / 2), center_y - round(height / 2))
    hwnd = roblox_window._hWnd
    win32gui.SetForegroundWindow(hwnd)

    if roblox_window.size != (width, height):
        print("Something went wrong. Try maximizing the Roblox window.")
        return None, None, None

    # Get Roblox window dimensions
    roblox_rect = win32gui.GetWindowRect(hwnd)
    roblox_middle_x = (roblox_rect[0] + roblox_rect[2]) // 2
    roblox_middle_y = (roblox_rect[1] + roblox_rect[3]) // 2

    coordinates = {
        "hwnd": hwnd,
        "firstX": roblox_middle_x - 270,
        "firstY": roblox_middle_y - 305,
        "lastX": roblox_middle_x + 270,
        "lastY": roblox_middle_y + 230,
        "openButtonX": roblox_middle_x + 110,
        "openButtonY": roblox_middle_y + 285,
        "inputX": roblox_middle_x + 110,
        "inputY": roblox_middle_y + 200,
        "closeButtonX": roblox_middle_x + 310,
        "closeButtonY": roblox_middle_y - 45
    }

    return coordinates

# Function to simulate a mouse click at given coordinates
def click(x, y):
    win32api.SetCursorPos((x, y))
    for _ in range(2):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.01)

# Function to convert RGB to HEX
def rgb2hex(pixel):
    return '{:02x}{:02x}{:02x}'.format(*pixel).upper()

# Function to simulate a mouse click on a pixel
def click_pixel(coords, add_x, add_y, num_clicks=3):
    click_x = round(coords["firstX"] + add_x * (coords["lastX"] - coords["firstX"]) / 31)
    click_y = round(coords["firstY"] + add_y * (coords["lastY"] - coords["firstY"]) / 31)
    
    for _ in range(num_clicks):
        time.sleep(.001)
        click(click_x, click_y)

# Function to select a color in the game
def selectColor(coords, color):
    hexColor = rgb2hex(color)
    click(coords["openButtonX"], coords["openButtonY"])
    click(coords["inputX"], coords["inputY"])
    vkey.typer(string=hexColor)
    for _ in range(2):
        click(coords["closeButtonX"], coords["closeButtonY"])

# Function to capture the screen at a specific region
def capture_screen(x, y, width, height):
    bbox = (x, y, x + width, y + height)
    screenshot = ImageGrab.grab(bbox)
    return screenshot

# Function to verify the color at a specific pixel
def verify_color(x, y, target_color):
    screenshot = capture_screen(x, y, 1, 1)
    pixel_color = screenshot.getpixel((0, 0))
    return pixel_color == target_color
