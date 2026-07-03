import subprocess, os
import pyautogui, pyperclip
import keyboard_actions as kb

def type_text(text: str):
    """Type arbitrary text via clipboard to handle Unicode safely."""
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")

def scroll(direction: str, clicks: int = 5):
    clicks = int(clicks)
    pyautogui.scroll(clicks if direction == "up" else -clicks)

def click_left():    pyautogui.click()
def click_right():   pyautogui.click(button="right")
def click_double():  pyautogui.doubleClick()

def run_shell(cmd: str):
    subprocess.Popen(cmd, shell=True)

def press(combo: str):
    kb.press_combo(combo)