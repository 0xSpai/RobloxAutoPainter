# Library imports
import os
import pygetwindow as gw
import time
import virtualkeystroke as vkey
import win32api, win32con, win32gui
import tkinter as tk
import psutil
import keyboard
import win32process
from PIL import Image, ImageGrab
from tqdm import tqdm
from screeninfo import get_monitors
from tkinter import filedialog

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
def click_pixel(add_x, add_y, num_clicks=3):
    click_x = round(firstX + add_x * (lastX - firstX) / 31)
    click_y = round(firstY + add_y * (lastY - firstY) / 31)
    
    for _ in range(num_clicks):
        time.sleep(.001)
        click(click_x, click_y)

# Function to select a color in the game
def selectColor(color):
    hexColor = rgb2hex(color)
    click(openButtonX, openButtonY)
    click(inputX, inputY)
    vkey.typer(string=hexColor)
    for _ in range(2):
        click(closeButtonX, closeButtonY)

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

# Check whether space is pressed
def is_space_pressed():
    return keyboard.is_pressed('space')

# Clear the console ¯\_(ツ)_/¯
clear = lambda: os.system('cls')
clear()

# Create a Tkinter root widget
root = tk.Tk()
root.withdraw()

# Intro
print("Welcome to Spai's Auto Painter! 'Space' to force-quit.")
time.sleep(1)

# Open a file dialog and ask the user to select an image file
print("")
print("Selecting image...")
image_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")]
)

# Load and process the image
if image_path:
    image = Image.open(image_path)
    
    # Resize the image to 32x32 with better resampling
    if image.size != (32, 32):
        image = image.resize((32, 32), resample=Image.LANCZOS)
    
    # Ensure the target directory exists
    target_directory = "processed_images"
    os.makedirs(target_directory, exist_ok=True)
    
    # Construct the new file path
    image_name = os.path.basename(image_path)
    new_image_path = os.path.join(target_directory, image_name)
    
    # Save the resized image to the target directory
    image.save(new_image_path, quality=100)
    image_pixels = image.load()

    print("Image selected:", image_name)
    print("")
else:
    print("No image selected.")
    quit()

startInput = input("Begin painting? (y/n) ")

if startInput == "y":
    print("")
    print("Painting progress:")

    # Calculate screen resolution
    for m in get_monitors():
        screen_width, screen_height = m.width, m.height

    center_x, center_y = screen_width // 2, screen_height // 2

    # Get Roblox window
    roblox_windows = []
    for win in gw.getAllWindows():
        if win.title == "Roblox":
            class_name = win32gui.GetClassName(win._hWnd)
            if "Chrome_WidgetWin_1" not in class_name:
                _, pid = win32process.GetWindowThreadProcessId(win._hWnd)
                try:
                    process = psutil.Process(pid)
                    executable_path = process.exe()
                    # Check if the executable path belongs to Roblox
                    if "RobloxPlayerBeta.exe" in executable_path:
                        roblox_windows.append(win)
                except psutil.NoSuchProcess:
                    pass

    if not roblox_windows:
        print("Roblox window not found. Open Roblox and try again!")
        quit()

    roblox_window = roblox_windows[0]
    if roblox_window.isMinimized:
        roblox_window.restore()

    roblox_window.resizeTo(1681, 957)
    roblox_window.moveTo(center_x - round(840.5), center_y - round(478.5))
    hwnd = roblox_window._hWnd
    win32gui.SetForegroundWindow(hwnd)

    if roblox_window.size != (1681, 957):
        print("Something went wrong. Try maximizing the Roblox window.")
        quit()

    # Get Roblox window dimensions
    roblox_rect = win32gui.GetWindowRect(hwnd)
    roblox_middle_x = (roblox_rect[0] + roblox_rect[2]) // 2
    roblox_middle_y = (roblox_rect[1] + roblox_rect[3]) // 2

    # Define action coordinates
    firstX, firstY = roblox_middle_x - 270, roblox_middle_y - 305
    lastX, lastY = roblox_middle_x + 270, roblox_middle_y + 230
    openButtonX, openButtonY = roblox_middle_x + 110, roblox_middle_y + 285
    inputX, inputY = roblox_middle_x + 110, roblox_middle_y + 200
    closeButtonX, closeButtonY = roblox_middle_x + 310, roblox_middle_y - 45

    pixels = {}
    for x in range(32):
        for y in range(32):
            pixels.setdefault(image_pixels[x, y], []).append((x, y))
    image.close()

    # Main execution
    time.sleep(1)

    for _ in range(2):
        click(closeButtonX, closeButtonY)
    click(roblox_middle_x + 270, roblox_middle_y + 285)
    time.sleep(0.5)
    click(roblox_middle_x + 110, roblox_middle_y + 80)
    time.sleep(0.5)

    for color in tqdm(pixels):
        selectColor(color)
        for pixel in pixels[color]:
            if is_space_pressed():
                 clear()
                 quit()
            click_pixel(*pixel)
            click_x = round(firstX + pixel[0] * (lastX - firstX) / 31)
            click_y = round(firstY + pixel[1] * (lastY - firstY) / 31)
            if not verify_color(click_x, click_y, color):
                selectColor(color)
                click_pixel(*pixel)
    print("")
    print("Painting completed, enjoy!")
    time.sleep(1)
    quit()
else:
    clear()
    quit()