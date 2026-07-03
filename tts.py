"""Text-to-speech with multiple backends:
- pyttsx3: Offline, uses Windows SAPI voices (fast, low latency)
- edge-tts: Online, uses Microsoft Edge voices (high quality, requires internet)

Configure in config.py: TTS_BACKEND = "pyttsx3" or "edge-tts"
"""
import asyncio
import threading
import queue
import tempfile
import os

import config

class TTSEngine:
    def __init__(self):
        self.backend = config.TTS_BACKEND.lower()
        self._queue = queue.Queue()
        self._worker_thread = None
        self._init_backend()
        self._start_worker()
    
    def _init_backend(self):
        if self.backend == "pyttsx3":
            import pyttsx3
            self.engine = pyttsx3.init()
            # Configure voice
            voices = self.engine.getProperty('voices')
            if config.TTS_VOICE:
                # Try to find voice by name
                for voice in voices:
                    if config.TTS_VOICE.lower() in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            self.engine.setProperty('rate', config.TTS_RATE)
            self.engine.setProperty('volume', config.TTS_VOLUME)
            
        elif self.backend == "edge-tts":
            # edge-tts is async, we'll handle it in the worker
            self.voice = config.TTS_VOICE or "en-US-AriaNeural"
            
        else:
            raise ValueError(f"Unknown TTS backend: {self.backend}")
    
    def _start_worker(self):
        """Start background thread for TTS to avoid blocking."""
        def worker():
            while True:
                text = self._queue.get()
                if text is None:  # Shutdown signal
                    break
                self._speak(text)
        
        self._worker_thread = threading.Thread(target=worker, daemon=True)
        self._worker_thread.start()
    
    def _speak(self, text):
        """Actually speak the text."""
        if self.backend == "pyttsx3":
            self.engine.say(text)
            self.engine.runAndWait()
            
        elif self.backend == "edge-tts":
            self._speak_edge(text)
    
    def _speak_edge(self, text):
        """Use Edge TTS (async, requires internet)."""
        import edge_tts
        
        async def _async_speak():
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
            
            try:
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(temp_path)
                
                # Play the audio file
                self._play_audio_file(temp_path)
            finally:
                # Clean up
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass
        
        # Run async function in new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_async_speak())
        loop.close()
    
    def _play_audio_file(self, path):
        """Play audio file using Windows media player."""
        import subprocess
        # Use ffplay if available, otherwise Windows Media Player
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fallback to Windows Media Player
            subprocess.run(
                ["wmplayer", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    
    def speak(self, text):
        """Queue text to be spoken (non-blocking)."""
        if text:
            self._queue.put(text)
    
    def speak_now(self, text):
        """Speak immediately (blocking)."""
        if text:
            self._speak(text)
    
    def stop(self):
        """Stop the TTS worker."""
        self._queue.put(None)
        if self._worker_thread:
            self._worker_thread.join(timeout=1)

# Global instance
_tts = None

def init():
    global _tts
    if _tts is None:
        _tts = TTSEngine()
    return _tts

def speak(text):
    """Speak text using the configured backend."""
    engine = init()
    engine.speak(text)

def speak_now(text):
    """Speak text immediately (blocking)."""
    engine = init()
    engine.speak_now(text)

def stop():
    """Stop the TTS engine."""
    if _tts:
        _tts.stop()