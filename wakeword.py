"""Background wake word detection using Porcupine.
Runs in a daemon thread. Sets a flag when the wake word is heard."""
import threading
import sounddevice as sd
import pvporcupine
import config

_wake_word_triggered = False
_thread = None
_porcupine = None

def _listen_loop():
    global _wake_word_triggered, _porcupine
    
    try:
        _porcupine = pvporcupine.create(
            library_path=None,
            model_path=config.PORCUPINE_MODEL_PATH,
            keyword_paths=[config.PORCUPINE_KEYWORD_PATH]
        )
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
                # Porcupine expects a flat list of integers
                keyword_index = _porcupine.process(audio_frame.flatten().tolist())
                
                if keyword_index >= 0:
                    _wake_word_triggered = True
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
    """Stop the thread (it's a daemon, so it dies with the main process)."""
    pass