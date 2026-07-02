"""
speech.py

Records audio from the microphone and transcribes it
using Faster-Whisper.
"""

import os

import sounddevice as sd
import soundfile as sf

from faster_whisper import WhisperModel

import config


class SpeechRecognizer:

    def __init__(self):

        print("Loading Whisper model...")

        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE_TYPE,
        )

        print("Whisper loaded.\n")

    def record(self):

        print(f"Listening for {config.RECORD_SECONDS} seconds...")

        audio = sd.rec(
            int(config.RECORD_SECONDS * config.SAMPLE_RATE),
            samplerate=config.SAMPLE_RATE,
            channels=config.CHANNELS,
            dtype="float32",
        )

        sd.wait()

        sf.write(
            config.TEMP_WAV,
            audio,
            config.SAMPLE_RATE,
        )

        return config.TEMP_WAV

    def transcribe(self, wav_file):

        segments, info = self.model.transcribe(
            wav_file,
            beam_size=5,
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip()

        return text

    def listen(self):

        wav = self.record()

        text = self.transcribe(wav)

        try:
            os.remove(wav)
        except Exception:
            pass

        return text