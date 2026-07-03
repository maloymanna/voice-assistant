"""Edge control via keyboard shortcuts + pyautogui.
Kept simple and robust — no Selenium / CDP dependency."""
import pyautogui, pyperclip
import actions

def back():        pyautogui.hotkey("alt", "left")
def forward():     pyautogui.hotkey("alt", "right")
def refresh():     pyautogui.press("f5")
def new_tab():     pyautogui.hotkey("ctrl", "t")
def close_tab():   pyautogui.hotkey("ctrl", "w")

def goto(url: str):
    pyautogui.hotkey("ctrl", "l")     # focus address bar
    pyautogui.sleep(0.1)
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

def search(query: str):
    goto(f"https://www.bing.com/search?q={query.replace(' ', '+')}")