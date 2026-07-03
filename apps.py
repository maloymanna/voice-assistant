"""Launch and terminate apps. Uses a small alias table plus PowerShell fallback."""
import subprocess, os

# Common spoken-name -> executable / shell alias
_ALIASES = {
    "edge":          "msedge",
    "microsoft edge":"msedge",
    "browser":       "msedge",
    "excel":         "excel",
    "word":          "winword",
    "powerpoint":    "powerpnt",
    "outlook":       "outlook",
    "notepad":       "notepad",
    "calculator":    "calc",
    "calc":          "calc",
    "file explorer": "explorer",
    "explorer":      "explorer",
    "task manager":  "taskmgr",
    "control panel": "control",
    "cmd":           "cmd",
    "command prompt":"cmd",
    "powershell":    "pwsh",
    "git bash":      r"C:\Program Files\Git\bin\bash.exe",
    "settings":      "ms-settings:",
}

def open_app(name: str):
    key = name.strip().lower()
    target = _ALIASES.get(key, key)
    try:
        os.startfile(target)
    except Exception:
        # Fall back to PowerShell Start-Process (handles UWP / ms- URIs)
        subprocess.Popen(
            ["pwsh", "-NoProfile", "-Command", f"Start-Process '{target}'"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

def close_app(name: str):
    key = name.strip().lower()
    exe = _ALIASES.get(key, key)
    if not exe.endswith(".exe"):
        exe += ".exe"
    subprocess.run(
        ["taskkill", "/IM", exe, "/F"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )