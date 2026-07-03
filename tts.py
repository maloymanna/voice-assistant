"""Thread-safe TTS with proper engine lifecycle.
Engine is created and used in the same worker thread to avoid
RuntimeError: run loop already started."""
import threading
import queue

import config

class TTSEngine:
    def __init__(self):
        self.backend = config.TTS_BACKEND.lower()
        self._queue = queue.Queue()
        self._engine = None  # Lazy init in worker thread
        self._worker_thread = None
        self._start_worker()
    
    def _ensure_engine(self):
        """Create pyttsx3 engine in the worker thread (thread-safe)."""
        if self._engine is None and self.backend == "pyttsx3":
            import pyttsx3
            self._engine = pyttsx3.init()
            voices = self._engine.getProperty('voices')
            if config.TTS_VOICE:
                for voice in voices:
                    if config.TTS_VOICE.lower() in voice.name.lower():
                        self._engine.setProperty('voice', voice.id)
                        break
            self._engine.setProperty('rate', config.TTS_RATE)
            self._engine.setProperty('volume', config.TTS_VOLUME)
    
    def _start_worker(self):
        """Worker thread owns the pyttsx3 engine."""
        def worker():
            while True:
                item = self._queue.get()
                if item is None:
                    break
                text, blocking = item
                self._ensure_engine()
                if self.backend == "pyttsx3":
                    self._engine.say(text)
                    self._engine.runAndWait()
                elif self.backend == "edge-tts":
                    self._speak_edge(text)
        
        self._worker_thread = threading.Thread(target=worker, daemon=True)
        self._worker_thread.start()
    
    def _speak_edge(self, text):
        """Edge TTS (requires internet)."""
        import asyncio
        import edge_tts
        import tempfile
        import os
        import subprocess
        
        async def _async_speak():
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
            try:
                voice = config.TTS_VOICE or "en-US-AriaNeural"
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(temp_path)
                subprocess.run(
                    ["powershell", "-c",
                     f'(New-Object Media.SoundPlayer "{temp_path}").PlaySync()'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            finally:
                try:
                    os.remove(temp_path)
                except:
                    pass
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_async_speak())
        loop.close()
    
    def speak(self, text, wait=False):
        """Queue text to be spoken. If wait=True, block until done."""
        if not text:
            return
        if wait:
            # Synchronous: speak in current thread (only safe if not worker)
            self._ensure_engine()
            if self.backend == "pyttsx3":
                self._engine.say(text)
                self._engine.runAndWait()
            else:
                self._speak_edge(text)
        else:
            self._queue.put((text, False))
    
    def speak_now(self, text):
        """Speak immediately, blocking. Safe to call from any thread."""
        # Use a separate engine for blocking calls to avoid conflicts with worker
        if self.backend == "pyttsx3":
            import pyttsx3
            eng = pyttsx3.init()
            eng.setProperty('rate', config.TTS_RATE)
            eng.setProperty('volume', config.TTS_VOLUME)
            eng.say(text)
            eng.runAndWait()
            del eng
        else:
            self._speak_edge(text)
    
    def stop(self):
        self._queue.put(None)
        if self._worker_thread:
            self._worker_thread.join(timeout=1)


_tts = None

def init():
    global _tts
    if _tts is None:
        _tts = TTSEngine()
    return _tts

def speak(text, wait=False):
    init().speak(text, wait=wait)

def speak_now(text):
    init().speak_now(text)

def stop():
    if _tts:
        _tts.stop()