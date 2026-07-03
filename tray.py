"""System tray icon for background operation.
Right-click the tray icon to pause/resume/exit the assistant."""
import threading
from PIL import Image, ImageDraw
import pystray

import config

_icon = None
_thread = None
_paused = False


def _create_image():
    """Create a simple microphone icon."""
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    # Microphone body
    d.rectangle([24, 10, 40, 40], fill=(0, 200, 100))
    d.ellipse([24, 6, 40, 22], fill=(0, 200, 100))
    # Stand
    d.rectangle([30, 40, 34, 52], fill=(0, 200, 100))
    d.rectangle([22, 50, 42, 54], fill=(0, 200, 100))
    return img


def _on_pause(icon, item):
    global _paused
    _paused = not _paused
    item.text = "Resume" if _paused else "Pause"
    print(f"[tray] {'Paused' if _paused else 'Resumed'}")


def _on_exit(icon, item):
    print("[tray] Exit requested")
    icon.stop()
    import sys
    sys.exit(0)


def _run_tray():
    global _icon
    menu = pystray.Menu(
        pystray.MenuItem("Pause", _on_pause, default=True),
        pystray.MenuItem("Exit", _on_exit),
    )
    _icon = pystray.Icon("voice-assistant", _create_image(), "Voice Assistant", menu)
    _icon.run()


def start():
    """Start the tray icon in a background thread."""
    global _thread
    _thread = threading.Thread(target=_run_tray, daemon=True)
    _thread.start()


def stop():
    """Stop the tray icon."""
    if _icon:
        try:
            _icon.stop()
        except:
            pass


def is_paused():
    return _paused