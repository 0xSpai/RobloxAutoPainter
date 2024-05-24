# Library imports
import os
import pygetwindow as gw
import time
import virtualkeystroke as vkey
import win32api, win32con, win32gui
import tkinter as tk
from PIL import Image
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
    return '{:02x}{:02x}{:02x}'.format(*pixel)

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
    click(closeButtonX, closeButtonY)
    click(closeButtonX, closeButtonY)
    

# Create a Tkinter root widget
root = tk.Tk()
root.withdraw()

 # Open a file dialog and ask the user to select an image file
print("Select an image:")
image_path = filedialog.askopenfilename(
title="Select an Image",
filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")]
)

# Load and process the image
if image_path:
    image = Image.open(image_path)
    
    # Resize the image if it isn't 32x32
    if image.size != (32, 32):
        image = image.resize((32, 32), resample=Image.BOX)
    
    # Ensure the target directory exists
    target_directory = "processed_images"
    os.makedirs(target_directory, exist_ok=True)
    
    # Construct the new file path
    image_name = os.path.basename(image_path)
    new_image_path = os.path.join(target_directory, image_name)
    
    # Save the resized image to the target directory
    image.save(new_image_path, quality=100)
    image_pixels = image.load()
else:
    print("No image selected.")

# Calculate screen resolution
for m in get_monitors():
    screen_width, screen_height = m.width, m.height

center_x, center_y = screen_width // 2, screen_height // 2

# Get Roblox window
roblox_windows = [win for win in gw.getAllWindows() if win.title == "Roblox" and "Chrome_WidgetWin_1" not in win32gui.GetClassName(win._hWnd)]

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
firstX, firstY = roblox_middle_x - 260, roblox_middle_y - 300
lastX, lastY = roblox_middle_x + 260, roblox_middle_y + 230
openButtonX, openButtonY = roblox_middle_x + 110, roblox_middle_y + 285
inputX, inputY = roblox_middle_x + 110, roblox_middle_y + 200
closeButtonX, closeButtonY = roblox_middle_x + 310, roblox_middle_y - 45

pixels = {}
for x in range(32):
    for y in range(32):
        pixels.setdefault(image_pixels[x, y], []).append((x, y))
image.close()

# Main execution
click(closeButtonX, closeButtonX)
time.sleep(0.5)

for color in tqdm(pixels):
    selectColor(color)
    for pixel in pixels[color]:
        click_pixel(*pixel)
