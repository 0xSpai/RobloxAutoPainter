import os
import time

def clear():
    print("clearing")
    os.system('cls')

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

def printError(error_msg):
    printAscii()
    print("   ERROR:", error_msg)
    print("   Quitting application..")
    quit()

def printMenu():
    os.system('color A')
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

def printRandom():
    printAscii()
    options = [
        "   [01] Random",
        "   [02] Grayscale",
        "   [03] Blurred",
        ""
    ]
    for option in options:
        print(option)
        time.sleep(0.1)