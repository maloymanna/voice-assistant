"""Background wake word detection using Porcupine v1.9 (Direct from GitHub Source).
Uses the raw Python binding and explicit paths to .dll, .pv, and .ppn files."""
import sys
import os
import platform
import threading
import sounddevice as sd

# 1. Setup paths to the extracted GitHub source
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORCUPINE_DIR = os.path.join(BASE_DIR, "porcupine-1.9")
BINDING_PATH = os.path.join(PORCUPINE_DIR, "binding", "python")

# Inject the binding directory into sys.path so 'porcupine.py' can be imported
if BINDING_PATH not in sys.path:
    sys.path.insert(0, BINDING_PATH)

# Import the Porcupine class directly from porcupine.py
from porcupine import Porcupine

import config

_wake_word_triggered = False
_thread = None
_porcupine = None


def _listen_loop():
    global _wake_word_triggered, _porcupine
    
    # 2. Build explicit paths to all required v1.9 files
    # Detect architecture (amd64 vs x86)
    arch = "amd64" if platform.machine().endswith("64") else "x86"
    
    library_path = os.path.join(
        PORCUPINE_DIR, "lib", "windows", arch, "libpv_porcupine.dll"
    )
    model_path = os.path.join(
        PORCUPINE_DIR, "lib", "common", "porcupine_params.pv"
    )
    keyword_path = os.path.join(
        PORCUPINE_DIR, "resources", "keyword_files", "windows", "computer_windows.ppn"
    )
    
    # Verify all files exist
    for name, path in [("library", library_path), ("model", model_path), ("keyword", keyword_path)]:
        if not os.path.exists(path):
            print(f"[error] {name} not found at: {path}")
            return
    
    try:
        # v1.9 API: requires exact parameter names and a 'sensitivities' list
        _porcupine = Porcupine(
            library_path=library_path,
            model_path=model_path,
            keyword_paths=[keyword_path],
            sensitivities=[0.5]  # 0.5 is the default sensitivity (range 0.0 to 1.0)
        )
        print(f"[*] Porcupine v1.9 initialized successfully.")
        print(f"    Library: {library_path}")
        print(f"    Model:   {model_path}")
        print(f"    Keyword: {keyword_path}")
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
                # v1.9 process() expects a list of integers
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
    """Start the wake word listener in a background thread."""
    global _thread
    if _thread and _thread.is_alive():
        return
    
    _thread = threading.Thread(target=_listen_loop, daemon=True)
    _thread.start()
    print(f"[*] Wake word '{config.WAKE_WORD_NAME}' listening in background...")


def check_and_reset():
    """Check if wake word was triggered, and reset the flag."""
    global _wake_word_triggered
    if _wake_word_triggered:
        _wake_word_triggered = False
        return True
    return False


def stop():
    """Stop the thread (daemon, dies with main process)."""
    pass