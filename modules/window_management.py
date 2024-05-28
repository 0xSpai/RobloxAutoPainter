import pygetwindow as gw
import psutil
import win32gui
import win32process
import modules.output as output
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
        output.printError("Roblox window not found. Open Roblox and try again!")

    roblox_window = roblox_windows[0]
    if roblox_window.isMinimized:
        roblox_window.restore()

    roblox_window.resizeTo(width, height)
    roblox_window.moveTo(center_x - round(width / 2), center_y - round(height / 2))
    hwnd = roblox_window._hWnd
    win32gui.SetForegroundWindow(hwnd)

    if roblox_window.size != (width, height):
        output.printError("Failed to resize the Roblox window.")

    # Get Roblox window dimensions
    roblox_rect = win32gui.GetWindowRect(hwnd)
    roblox_middle_x = (roblox_rect[0] + roblox_rect[2]) // 2
    roblox_middle_y = (roblox_rect[1] + roblox_rect[3]) // 2

    coordinates = {
        "hwnd": hwnd,
        "firstX": roblox_middle_x - 270,
        "firstY": roblox_middle_y - 310,
        "lastX": roblox_middle_x + 267,
        "lastY": roblox_middle_y + 228,
        "openButtonX": roblox_middle_x + 110,
        "openButtonY": roblox_middle_y + 285,
        "inputX": roblox_middle_x + 110,
        "inputY": roblox_middle_y + 200,
        "closeButtonX": roblox_middle_x + 310,
        "closeButtonY": roblox_middle_y - 45
    }

    return coordinates
