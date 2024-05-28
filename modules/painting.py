import time
import win32api
import win32con
import modules.output as output
import modules.virtualkeystroke as vkey
import modules.utilities as utilities
from tqdm import tqdm
from modules.window_management import setup_window
from modules.utilities import verify_color

# Function to simulate a mouse click at given coordinates
def click(x, y):
    win32api.SetCursorPos((x, y))
    for _ in range(2):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.01)

# Function to simulate a mouse click on a pixel
def click_pixel(coords, add_x, add_y, num_clicks=3):
    click_x = round(coords["firstX"] + add_x * (coords["lastX"] - coords["firstX"]) / 31)
    click_y = round(coords["firstY"] + add_y * (coords["lastY"] - coords["firstY"]) / 31)
    
    for _ in range(num_clicks):
        time.sleep(.001)
        click(click_x, click_y)

# Function to select a color in the game
def select_color(coords, color):
    hexColor = utilities.rgb2hex(color)
    click(coords["openButtonX"], coords["openButtonY"])
    click(coords["inputX"], coords["inputY"])
    vkey.typer(string=hexColor)
    for _ in range(2):
        click(coords["closeButtonX"], coords["closeButtonY"])


def start_painting(image_pixels, image_name):
    output.printAscii()
    print("   Image selected:", image_name)
    startInput = input("   Begin painting? (y/n) ")
    if startInput.lower() != 'y':
        output.clear()
        quit()
    
    output.printAscii()
    print("Painting progress:")
    coords = setup_window()

    if coords is None:
       output.printError("Something went wrong. Try again.")
    
    pixels = {}
    for x in range(32):
        for y in range(32):
            color = image_pixels[x, y]
            if color != (255, 255, 255):
                pixels.setdefault(color, []).append((x, y))
    
    time.sleep(1)
    for _ in range(2):
        click(coords["closeButtonX"], coords["closeButtonY"])
    time.sleep(0.5)
    click(coords["firstX"] + 530, coords["firstY"] + 590)
    time.sleep(0.5)
    click(coords["openButtonX"], coords["openButtonY"] - 205)
    time.sleep(0.5)

    for color in tqdm(pixels):
        select_color(coords, color)
        for pixel in pixels[color]:
            click_pixel(coords, *pixel)
            click_x = round(coords["firstX"] + pixel[0] * (coords["lastX"] - coords["firstX"]) / 31)
            click_y = round(coords["firstY"] + pixel[1] * (coords["lastY"] - coords["firstY"]) / 31)
            if not verify_color(click_x, click_y, color):
                select_color(coords, color)
                click_pixel(coords, *pixel)
    
    print("\nPainting completed, enjoy!")