"""Background wake word detection using Porcupine from GitHub source."""
import sys
import os
import threading
import sounddevice as sd

# Add Porcupine Python binding to path
PORCUPINE_PYTHON_PATH = os.path.join(os.path.dirname(__file__), "porcupine-1.8.1", "binding", "python")
if PORCUPINE_PYTHON_PATH not in sys.path:
    sys.path.insert(0, PORCUPINE_PYTHON_PATH)

import pvporcupine
import config

_wake_word_triggered = False
_thread = None
_porcupine = None

def _listen_loop():
    global _wake_word_triggered, _porcupine
    
    try:
        _porcupine = pvporcupine.create(
            keyword_file_paths=[config.PORCUPINE_KEYWORD_PATH]
        )
        print(f"[*] Porcupine initialized")
    except Exception as e:
        print(f"[error] Failed to initialize Porcupine: {e}")
        return

    frame_length = _porcupine.frame_length
    
    try:
        with sd.InputStream(
            samplerate=_porcupine.sample_rate,
            channels=1,
            dtype='int16',
            blocksize=frame_length
        ) as stream:
            while True:
                audio_frame, _ = stream.read(frame_length)
                keyword_index = _porcupine.process(audio_frame.flatten().tolist())
                
                if keyword_index >= 0:
                    _wake_word_triggered = True
                    print(f"[*] Wake word detected!")
    except Exception as e:
        print(f"[error] Wake word listener crashed: {e}")
    finally:
        if _porcupine:
            _porcupine.delete()

def start():
    global _thread
    if _thread and _thread.is_alive():
        return
    
    _thread = threading.Thread(target=_listen_loop, daemon=True)
    _thread.start()
    print(f"[*] Wake word '{config.WAKE_WORD_NAME}' listening...")

def check_and_reset():
    global _wake_word_triggered
    if _wake_word_triggered:
        _wake_word_triggered = False
        return True
    return False

def stop():
    pass