"""Central configuration."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Speech Recognition (Vosk) ---
MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-en-us-0.22")
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
LISTEN_TIMEOUT_SEC = 6
CONFIDENCE_THRESHOLD = 0.65
MAX_RETRIES = 2

# --- Wake Word (Porcupine v1.8.1) ---
PORCUPINE_KEYWORD_PATH = os.path.join(BASE_DIR, "models", "porcupine", "computer_windows.ppn")
WAKE_WORD_NAME = "Computer"

# --- Text-to-Speech ---
TTS_BACKEND = "pyttsx3"
TTS_VOICE = ""
TTS_RATE = 180
TTS_VOLUME = 0.9

# --- Hotkeys ---
PUSH_TO_TALK_KEY = "f9"
QUIT_HOTKEY_COMBINATION = {"ctrl", "q"}

# --- Dictation ---
DICTATION_STOP_PHRASES = {"stop dictation", "stop typing", "end dictation"}

# --- Shortcuts ---
SHORTCUTS_FILE = os.path.join(BASE_DIR, "shortcuts.json")