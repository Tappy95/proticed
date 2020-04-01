# import pyautogui as pg
from pyautogui import hotkey, write, PAUSE


def jb():

    hotkey("ctrl", "alt", "w")

    write("hello~!", interval=0.3)

    hotkey("enter")

    hotkey("enter")


if __name__ == '__main__':
    jb()
