"""Thin wrapper around Vosk. Exposes two modes:
   - one_shot(): listen until a command is spoken (or timeout)
   - stream(): yield transcripts continuously (used by dictation mode)
"""
import json, queue, time
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel

import config

SetLogLevel(-1)  # quiet

class Recognizer:
    def __init__(self):
        if not __import__("os").path.isdir(config.MODEL_PATH):
            raise RuntimeError(
                f"Model missing at {config.MODEL_PATH}. Run setup_models.py first."
            )
        self.model = Model(config.MODEL_PATH)
        self._make_rec()

    def _make_rec(self):
        self.rec = KaldiRecognizer(self.model, config.SAMPLE_RATE)
        self.q = queue.Queue()

    def _cb(self, indata, frames, time_info, status):
        if status:
            pass  # ignore xruns etc.
        self.q.put(bytes(indata))

    def one_shot(self, timeout=None):
        """Return a single transcript string, or '' on timeout / silence."""
        timeout = timeout or config.LISTEN_TIMEOUT_SEC
        self._make_rec()
        final_text = ""
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
            # grab any trailing partial
            if not final_text:
                final_text = json.loads(self.rec.FinalResult()).get("text", "").strip()
        return final_text

    def stream(self):
        """Yield transcript strings as the user speaks, indefinitely."""
        self._make_rec()
        with sd.RawInputStream(
            samplerate=config.SAMPLE_RATE,
            blocksize=config.BLOCK_SIZE,
            dtype="int16",
            channels=1,
            callback=self._cb,
        ):
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    text = json.loads(self.rec.Result()).get("text", "").strip()
                    if text:
                        yield text