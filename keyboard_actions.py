"""
keyboard_actions.py

Central mapping for keyboard shortcuts.
"""

import keyboard

SHORTCUTS = {

    # File
    "save": "ctrl+s",
    "save file": "ctrl+s",
    "save as": "ctrl+shift+s",
    "new file": "ctrl+n",
    "open file": "ctrl+o",
    "print": "ctrl+p",
    "close file": "ctrl+w",

    # Editing
    "copy": "ctrl+c",
    "paste": "ctrl+v",
    "cut": "ctrl+x",
    "undo": "ctrl+z",
    "redo": "ctrl+y",
    "select all": "ctrl+a",

    "find": "ctrl+f",
    "replace": "ctrl+h",

    # Browser
    "refresh": "f5",
    "reload": "f5",

    "new tab": "ctrl+t",
    "close tab": "ctrl+w",
    "reopen tab": "ctrl+shift+t",

    "next tab": "ctrl+tab",
    "previous tab": "ctrl+shift+tab",

    "address bar": "ctrl+l",

    "back": "alt+left",
    "forward": "alt+right",

    # Windows

    "task manager": "ctrl+shift+esc",

    "desktop": "win+d",

    "run": "win+r",

    "lock computer": "win+l",

    "file explorer": "win+e",

    # Outlook

    "new email": "ctrl+n",

    "reply": "ctrl+r",

    "reply all": "ctrl+shift+r",

    "forward email": "ctrl+f",

    "send email": "alt+s",

    # PowerPoint

    "new slide": "ctrl+m",

    "start slideshow": "f5",

    "next slide": "right",

    "previous slide": "left",

    # Excel

    "insert row": "ctrl+shift+=",

    "insert column": "ctrl+space",

    "format cells": "ctrl+1",

    "filter": "ctrl+shift+l",

    "edit cell": "f2"

}


def perform_shortcut(command: str):

    command = command.lower().strip()

    combo = SHORTCUTS.get(command)

    if combo is None:
        return False

    keyboard.press_and_release(combo)

    print(f"Shortcut: {combo}")

    return True