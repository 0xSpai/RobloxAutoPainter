import os
import time

def clear():
    print("clearing")
    os.system('cls')

# Cool ascii text
def printAscii():
    clear()
    print(
        """

        :::::::::::. :::.     :::::::.    :::.:::::::::::::::::::..   
        `;;;```.;;;;;`;;    ;;;`;;;;,  `;;;;;;;;;;;'''';;;;``;;;;  
         `]]nnn]]',[[ '[[,  [[[  [[[[[. '[[     [[      [[[,/[[['  
          $$$""  c$$$cc$$$c $$$  $$$ "Y$c$$     $$      $$$$$$c    
          888o    888   888,888  888    Y88     88,     888b "88bo,
          YMMMb   YMM   ""` MMM  MMM     YM     MMM     MMMM   "W" """
    )
    print("                                        [-] Tool Created by 0xSpai")
    print("         ")

# Main menu printing
def printMenu():
    printAscii()
    options = [
        "   [01] Custom Image",
        "   [02] Random Image",
        "   [99] Exit Auto Painter",
        ""
    ]
    for option in options:
        print(option)
        time.sleep(0.1)

def printCustom():
    printAscii()
    options = [
        "   [01] From computer file",
        "   [02] From image address",
        ""
    ]
    for option in options:
        print(option)
        time.sleep(0.1)