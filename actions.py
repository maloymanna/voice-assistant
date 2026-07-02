"""
actions.py

General Windows actions.
"""

import time
import webbrowser

import keyboard
import pyautogui
import pyperclip

import config


keyboard.PAUSE = config.KEY_DELAY


def open_url(url: str):

    if not url.startswith("http"):

        url = "https://" + url

    webbrowser.open(url)

    print(f"Opening {url}")


def google_search(query: str):

    url = config.DEFAULT_SEARCH_ENGINE.format(
        query.replace(" ", "+")
    )

    webbrowser.open(url)

    print(f"Searching Google: {query}")


def type_text(text: str):

    keyboard.write(
        text,
        delay=config.TYPE_DELAY,
    )

    print("Typed text.")


def scroll_down():

    pyautogui.scroll(-config.SCROLL_AMOUNT)


def scroll_up():

    pyautogui.scroll(config.SCROLL_AMOUNT)


def page_down():

    keyboard.press_and_release("pagedown")


def page_up():

    keyboard.press_and_release("pageup")


def press_enter():

    keyboard.press_and_release("enter")


def press_escape():

    keyboard.press_and_release("esc")


def press_tab():

    keyboard.press_and_release("tab")


def shift_tab():

    keyboard.press_and_release("shift+tab")


def click():

    pyautogui.click()


def double_click():

    pyautogui.doubleClick()


def right_click():

    pyautogui.rightClick()


def copy():

    keyboard.press_and_release("ctrl+c")


def paste():

    keyboard.press_and_release("ctrl+v")


def cut():

    keyboard.press_and_release("ctrl+x")


def select_all():

    keyboard.press_and_release("ctrl+a")


def undo():

    keyboard.press_and_release("ctrl+z")


def redo():

    keyboard.press_and_release("ctrl+y")


def alt_tab():

    keyboard.press_and_release("alt+tab")


def read_clipboard():

    text = pyperclip.paste()

    print(text)

    return text