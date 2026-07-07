"""Speech recognition using openai-whisper.
Records audio from microphone, saves to temp file, transcribes with Whisper."""
import os
import tempfile
import numpy as np
import sounddevice as sd
import whisper
import config

class Recognizer:
    def __init__(self):
        print("[*] Loading Whisper model (this may take a moment on first run)...")
        self.model = whisper.load_model("small.en")
        print("[*] Whisper model loaded.")

    def one_shot(self, timeout=None):
        """Record audio for timeout seconds, then transcribe with Whisper.
        Returns (text, confidence). Whisper doesn't provide confidence, so we return 1.0."""
        timeout = timeout or config.LISTEN_TIMEOUT_SEC
        
        # Record audio
        print("[*] Recording...")
        audio_data = sd.rec(
            int(timeout * config.SAMPLE_RATE),
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype='float32'
        )
        sd.wait()  # Wait until recording is finished
        
        # Flatten to 1D array
        audio = audio_data.flatten()
        
        # Check if there's actual speech (simple RMS check)
        rms = np.sqrt(np.mean(audio**2))
        if rms < 0.01:  # Very quiet, probably silence
            return "", 0.0
        
        # Transcribe with Whisper
        print("[*] Transcribing...")
        result = self.model.transcribe(audio, language="en", fp16=False)
        text = result["text"].strip()
        
        # Whisper doesn't provide confidence, so we return 1.0
        return text, 1.0