"""Translate combo strings like 'ctrl+shift+s' into pyautogui hotkey calls."""
import pyautogui

pyautogui.FAILSAFE = True        # move mouse to corner to abort
pyautogui.PAUSE = 0.05

_MODS = {"ctrl", "control", "alt", "shift", "win", "windows", "cmd", "command"}

def _normalize(key: str) -> str:
    k = key.strip().lower()
    return {"control": "ctrl", "windows": "win", "cmd": "win", "command": "win"}.get(k, k)

def press_combo(combo: str):
    """combo is e.g. 'ctrl+shift+s' or a single key like 'enter'."""
    parts = [_normalize(p) for p in combo.split("+")]
    mods = [p for p in parts if p in _MODS]
    keys = [p for p in parts if p not in _MODS]
    if not keys:
        return
    pyautogui.hotkey(*mods, *keys)