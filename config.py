"""Central configuration. All user-tunable settings live here."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Speech Recognition (Vosk) ---
# Point this to the large 1.8GB model for best accuracy
MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-en-us-0.22")
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
LISTEN_TIMEOUT_SEC = 6

# Confidence scoring (0.0 to 1.0). 
# If Vosk's confidence is below this, it will ask you to repeat.
CONFIDENCE_THRESHOLD = 0.65 
MAX_RETRIES = 2

# --- Wake Word (Porcupine) ---
PORCUPINE_MODEL_PATH = os.path.join(BASE_DIR, "models", "porcupine", "porcupine_params.pv")
PORCUPINE_KEYWORD_PATH = os.path.join(BASE_DIR, "models", "porcupine", "computer_windows.ppn")
WAKE_WORD_NAME = "Computer"  # Used for TTS feedback

# --- Text-to-Speech ---
TTS_BACKEND = "pyttsx3"  # "pyttsx3" (offline) or "edge-tts" (online)
TTS_VOICE = ""           # Empty for default Windows voice
TTS_RATE = 180
TTS_VOLUME = 0.9

# --- Hotkeys ---
PUSH_TO_TALK_KEY = "f9"
QUIT_HOTKEY_COMBINATION = {"ctrl", "q"} # Press Ctrl+Q to instantly exit

# --- Dictation ---
DICTATION_STOP_PHRASES = {"stop dictation", "stop typing", "end dictation"}

# --- Shortcuts ---
SHORTCUTS_FILE = os.path.join(BASE_DIR, "shortcuts.json")