"""Central configuration."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Speech Recognition (Whisper) ---
WHISPER_MODEL = "small.en"  # or "base.en", "tiny.en" for faster but less accurate
SAMPLE_RATE = 16000
LISTEN_TIMEOUT_SEC = 6
CONFIDENCE_THRESHOLD = 0.5  # Not used by Whisper, but kept for compatibility
MAX_RETRIES = 2

# --- Wake Word (Porcupine v1.9) ---
USE_WAKE_WORD = False  # Disabled for now, use F9 only
WAKE_WORD_NAME = "Computer"

# --- Text-to-Speech ---
TTS_BACKEND = "pyttsx3"
TTS_VOICE = ""
TTS_RATE = 180
TTS_VOLUME = 0.9

# --- Hotkeys ---
PUSH_TO_TALK_KEY = "f9"

# --- Dictation ---
DICTATION_STOP_PHRASES = {"stop dictation", "stop typing", "end dictation"}

# --- Shortcuts ---
SHORTCUTS_FILE = os.path.join(BASE_DIR, "shortcuts.json")