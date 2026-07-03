"""Central configuration. Tweak to taste."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Speech
MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-small-en-us-0.15")
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
LISTEN_TIMEOUT_SEC = 6          # max seconds to wait for one command
SILENCE_THRESHOLD = 300         # rough RMS cutoff for "is user talking"

# Text-to-speech
TTS_BACKEND = "pyttsx3"  # "pyttsx3" (offline) or "edge-tts" (online, better quality)
TTS_VOICE = ""  # Empty for default, or specify voice name
TTS_RATE = 180  # Speech rate (words per minute)
TTS_VOLUME = 0.9  # Volume 0.0 to 1.0

# Hotkey (pynput key name). Press this to start listening.
PUSH_TO_TALK_KEY = "f9"

# Dictation
DICTATION_STOP_PHRASES = {"stop dictation", "stop typing", "end dictation"}

# Browser
DEFAULT_BROWSER = "msedge"

# Shortcuts map
SHORTCUTS_FILE = os.path.join(BASE_DIR, "shortcuts.json")