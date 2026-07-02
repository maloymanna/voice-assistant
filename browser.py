"""
browser.py

Browser automation helpers (Edge-focused).
"""

import webbrowser
import subprocess
import time

import pyautogui
import keyboard

import config


def open_browser():

    """
    Opens Microsoft Edge.
    """

    try:
        subprocess.Popen(config.APPLICATIONS["edge"])
        print("Opened Edge")
        return True

    except Exception as e:
        print(f"Failed to open Edge: {e}")
        return False


def go_to_url(url: str):

    """
    Opens a URL in the default browser.
    """

    url = url.strip()

    if not url.startswith("http"):
        url = "https://" + url

    webbrowser.open(url)

    print(f"Opening {url}")


def focus_address_bar():

    """
    Focus Edge address bar (Ctrl+L).
    """

    keyboard.press_and_release("ctrl+l")


def refresh_page():

    keyboard.press_and_release("f5")


def new_tab():

    keyboard.press_and_release("ctrl+t")


def close_tab():

    keyboard.press_and_release("ctrl+w")


def search_in_google(query: str):

    """
    Opens Google search in browser.
    """

    url = config.DEFAULT_SEARCH_ENGINE.format(query.replace(" ", "+"))

    webbrowser.open(url)

    print(f"Searching Google: {query}")


def go_back():

    keyboard.press_and_release("alt+left")


def go_forward():

    keyboard.press_and_release("alt+right")


def scroll_down():

    pyautogui.scroll(-config.SCROLL_AMOUNT)


def scroll_up():

    pyautogui.scroll(config.SCROLL_AMOUNT)