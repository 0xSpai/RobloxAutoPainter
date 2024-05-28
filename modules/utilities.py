from PIL import ImageGrab

# Function to convert RGB to HEX
def rgb2hex(pixel):
    return '{:02x}{:02x}{:02x}'.format(*pixel).upper()

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
