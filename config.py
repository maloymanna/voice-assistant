"""
Configuration for Local Voice Assistant
"""

from pathlib import Path

# -------------------------------
# Speech Recognition
# -------------------------------

WHISPER_MODEL = "small"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE_TYPE = "int8"

SAMPLE_RATE = 16000

CHANNELS = 1

RECORD_SECONDS = 5

TEMP_WAV = "speech.wav"

# -------------------------------
# Browser
# -------------------------------

DEFAULT_SEARCH_ENGINE = "https://www.google.com/search?q={}"

# -------------------------------
# Applications
# -------------------------------

APPLICATIONS = {

    "edge": "msedge.exe",

    "excel": "excel.exe",

    "powerpoint": "powerpnt.exe",

    "outlook": "outlook.exe",

    "notepad": "notepad.exe",

    "notepad++": "notepad++.exe",

    "calculator": "calc.exe",

    "paint": "mspaint.exe",

    "explorer": "explorer.exe"

}

# -------------------------------
# Common Windows folders
# -------------------------------

FOLDERS = {

    "downloads": str(Path.home() / "Downloads"),

    "documents": str(Path.home() / "Documents"),

    "desktop": str(Path.home() / "Desktop"),

    "pictures": str(Path.home() / "Pictures")

}

# -------------------------------
# Command timing
# -------------------------------

KEY_DELAY = 0.05

TYPE_DELAY = 0.01

SCROLL_AMOUNT = 600

# -------------------------------
# Logging
# -------------------------------

DEBUG = True

# -------------------------------
# Greeting
# -------------------------------

WELCOME = """
------------------------------------
Local Windows Voice Assistant
Offline Version
Type 'quit' to exit
------------------------------------
"""