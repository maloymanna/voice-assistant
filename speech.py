"""Grammar-constrained Vosk recognizer.
Instead of free-form dictation, we constrain the decoder to only recognize
known commands. This dramatically improves accuracy for a fixed command set."""
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

import config

SetLogLevel(-1)

# Build the grammar dynamically from commands + shortcuts
def build_grammar():
    """Build list of expected phrases for grammar-constrained recognition."""
    phrases = set()
    
    # App commands
    app_names = ["edge", "excel", "word", "powerpoint", "outlook", "notepad",
                 "calculator", "file explorer", "task manager", "settings",
                 "cmd", "powershell", "git bash", "browser"]
    for app in app_names:
        phrases.update([
            f"open {app}", f"launch {app}", f"start {app}",
            f"close {app}", f"quit {app}", f"exit {app}",
        ])
    
    # Browser commands
    phrases.update([
        "back", "go back", "forward", "refresh",
        "new tab", "open tab", "close tab", "close this tab",
    ])
    
    # Dictation
    phrases.update(["dictation", "start dictation", "dictation mode"])
    
    # Mouse
    phrases.update([
        "click", "left click", "right click", "double click",
        "scroll up", "scroll down",
        "scroll up five", "scroll down five",
    ])
    
    # Shortcuts from shortcuts.json
    try:
        with open(config.SHORTCUTS_FILE, encoding="utf-8") as f:
            shortcuts = json.load(f)
        for name in shortcuts:
            phrases.update([
                f"press {name}", f"hit {name}", f"do {name}",
            ])
    except FileNotFoundError:
        pass
    
    # Exit
    phrases.update(["exit", "stop", "quit assistant", "exit assistant"])
    
    return list(phrases)


class Recognizer:
    def __init__(self):
        import os
        if not os.path.isdir(config.MODEL_PATH):
            raise RuntimeError(
                f"Model missing at {config.MODEL_PATH}. Run setup_models.py first."
            )
        self.model = Model(config.MODEL_PATH)
        self.grammar = build_grammar()
        # Grammar JSON format for Vosk
        self.grammar_json = json.dumps(self.grammar)
        self._make_rec()

    def _make_rec(self):
        # Pass grammar to constrain recognition
        self.rec = KaldiRecognizer(self.model, config.SAMPLE_RATE, self.grammar_json)
        self.q = queue.Queue()

    def _cb(self, indata, frames, time_info, status):
        self.q.put(bytes(indata))

    def one_shot(self, timeout=None):
        """Return a single transcript string, or '' on timeout / silence."""
        timeout = timeout or config.LISTEN_TIMEOUT_SEC
        self._make_rec()
        final_text = ""
        import time
        deadline = time.time() + timeout
        with sd.RawInputStream(
            samplerate=config.SAMPLE_RATE,
            blocksize=config.BLOCK_SIZE,
            dtype="int16",
            channels=1,
            callback=self._cb,
        ):
            while time.time() < deadline:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    text = json.loads(self.rec.Result()).get("text", "").strip()
                    if text:
                        final_text = text
                        break
            if not final_text:
                final_text = json.loads(self.rec.FinalResult()).get("text", "").strip()
        return final_text