"""Free-form Vosk recognizer with confidence scoring.
No grammar constraints. Vosk listens to everything, commands.py parses it."""
import json
import queue
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

import config

SetLogLevel(-1)

class Recognizer:
    def __init__(self):
        if not os.path.isdir(config.MODEL_PATH):
            raise RuntimeError(
                f"Model missing at {config.MODEL_PATH}. Run setup_models.py first."
            )
        self.model = Model(config.MODEL_PATH)
        self._make_rec()

    def _make_rec(self):
        # NO grammar passed here. Free-form recognition.
        self.rec = KaldiRecognizer(self.model, config.SAMPLE_RATE)
        self.q = queue.Queue()

    def _cb(self, indata, frames, time_info, status):
        self.q.put(bytes(indata))

    def one_shot(self, timeout=None):
        """Listen for one utterance. Returns (text, confidence)."""
        timeout = timeout or config.LISTEN_TIMEOUT_SEC
        self._make_rec()
        
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
                    res = json.loads(self.rec.Result())
                    text = res.get("text", "").strip()
                    if text:
                        conf = res.get("confidence", 1.0)
                        return text, conf
            
            # Timeout reached, get final partial result
            res = json.loads(self.rec.FinalResult())
            text = res.get("text", "").strip()
            conf = res.get("confidence", 0.0)
            return text, conf