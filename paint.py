import tkinter as tkinter
import modules.output as output
import modules.image_processing as image_processing
import modules.painting as painting

# Initialize Tkinter root widget
root = tkinter.Tk()
root.withdraw()

# Display main menu
output.printMenu()
menuSelection = input("   Main Menu | Choose: ")

 # Custom image
if menuSelection in ["1", "01"]:
    output.clear()
    output.printCustom()
    customSelection = input("   Custom Image | Choose: ")
    
    if customSelection in ["1", "01"]:
        image_pixels, image_name = image_processing.process_image_from_path()
    elif customSelection in ["2", "02"]:
        image_pixels, image_name = image_processing.process_image_from_url()
    else:
        output.clear()
        quit()
    
    painting.start_painting(image_pixels, image_name)

 # Random Image
elif menuSelection in ["2", "02"]:
    output.printAscii()
else:
    output.clear()
    quit()