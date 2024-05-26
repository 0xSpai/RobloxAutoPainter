# Imports
import os
import time
import tkinter as tk
import requests
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from tkinter import filedialog
import modules.functions as functions
import modules.console as console

# Tkinter root widget
root = tk.Tk()
root.withdraw()

# Main menu start
os.system(f'color {"A"}')
console.printMenu()
menuSelection = input("   Main Menu | Choose: ")
customSelection = None

if menuSelection == "1" or menuSelection == "01":
    console.clear()
    console.printCustom()
    customSelection = input("   Custom Image | Choose: ")

    if customSelection == "1" or customSelection == "01":
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")]
        )

        if image_path:
            image = Image.open(image_path)

            if image.size != (32, 32):
                image = image.resize((32, 32), resample=Image.LANCZOS)

            target_directory = "processed_images"
            os.makedirs(target_directory, exist_ok=True)

            image_name = os.path.basename(image_path)
            new_image_path = os.path.join(target_directory, image_name)

            image.save(new_image_path, quality=100)
            image_pixels = image.load()
        else:
            console.clear()
            quit()

    elif customSelection == "2" or customSelection == "02":
        image_url = input("   Enter image address: ")
        response = requests.get(image_url)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))

            if image.size != (32, 32):
                image = image.resize((32, 32), resample=Image.LANCZOS)

            target_directory = "processed_images"
            os.makedirs(target_directory, exist_ok=True)

            image_name = os.path.basename(image_url)
            new_image_path = os.path.join(target_directory, image_name)

            image.save(new_image_path, quality=100)
            image_pixels = image.load()
    else:
        console.clear()
        quit()

    console.printAscii()
    startInput = input("   Begin painting? (y/n) ")

    if startInput == "y":
        console.printAscii()
        print("   Painting progress:")

        coords = functions.setup_window()

        if coords is not None:
            pixels = {}
            for x in range(32):
                for y in range(32):
                    pixels.setdefault(image_pixels[x, y], []).append((x, y))
            image.close()

            time.sleep(1)

            for _ in range(2):
                functions.click(coords["closeButtonX"], coords["closeButtonY"])
            functions.click(coords["firstX"] + 270, coords["firstY"] + 590)
            time.sleep(0.5)
            functions.click(coords["openButtonX"], coords["openButtonY"] - 205)
            time.sleep(0.5)

            for color in tqdm(pixels):
                functions.selectColor(coords, color)
                for pixel in pixels[color]:
                    functions.click_pixel(coords, *pixel)
                    click_x = round(coords["firstX"] + pixel[0] * (coords["lastX"] - coords["firstX"]) / 31)
                    click_y = round(coords["firstY"] + pixel[1] * (coords["lastY"] - coords["firstY"]) / 31)
                    if not functions.verify_color(click_x, click_y, color):
                        functions.selectColor(coords, color)
                        functions.click_pixel(coords, *pixel)
            print("")
            print("Painting completed, enjoy!")
    else:
        console.clear()
        quit()

elif menuSelection == "2" or menuSelection == "02":
    console.printAscii()
else:
    console.clear()
    quit()