"""Main loop with proper pre/post voice feedback."""
import sys
import time
from pynput import keyboard as kb

import config
from speech import Recognizer
from commands import Parser
import actions, apps, browser, office, dictation as dictation_mod
import tts
import tray

recognizer = Recognizer()
parser = Parser()

def dispatch(cmd):
    a = cmd["action"]; args = cmd["args"]
    print(f"  -> {a} {args}")

    if a == "open_app":
        name = args[0]
        tts.speak(f"Opening {name}")
        apps.open_app(name)
        time.sleep(1.5)  # Wait for app to launch
        tts.speak(f"{name} opened")
        
    elif a == "close_app":
        name = args[0]
        tts.speak(f"Closing {name}")
        apps.close_app(name)
        time.sleep(0.5)
        tts.speak(f"{name} closed")
        
    elif a == "browser_back":
        tts.speak("Going back")
        browser.back()
    elif a == "browser_forward":
        tts.speak("Going forward")
        browser.forward()
    elif a == "browser_refresh":
        tts.speak("Refreshing")
        browser.refresh()
    elif a == "browser_new_tab":
        tts.speak("New tab")
        browser.new_tab()
    elif a == "browser_close_tab":
        tts.speak("Closing tab")
        browser.close_tab()
    elif a == "browser_goto":
        tts.speak(f"Navigating to {args[0]}")
        browser.goto(args[0])
    elif a == "browser_search":
        tts.speak(f"Searching for {args[0]}")
        browser.search(args[0])
        
    elif a == "enter_dictation":
        tts.speak_now("Starting dictation")
        dictation_mod.run(recognizer)
        tts.speak("Dictation ended")
        
    elif a == "type_text":
        tts.speak(f"Typing {args[0]}")
        actions.type_text(args[0])
        
    elif a == "scroll":
        direction = args[0]
        tts.speak(f"Scrolling {direction}")
        actions.scroll(direction, args[1] or 5)
    elif a == "click_left":
        tts.speak("Click")
        actions.click_left()
    elif a == "click_right":
        tts.speak("Right click")
        actions.click_right()
    elif a == "click_double":
        tts.speak("Double click")
        actions.click_double()
        
    elif a == "shortcut_by_name":
        combo = parser.resolve_shortcut(args[0])
        if combo:
            tts.speak(f"Pressing {args[0]}")
            actions.press(combo)
        else:
            tts.speak(f"Unknown shortcut {args[0]}")
            
    elif a == "exit":
        tts.speak_now("Shutting down")
        tray.stop()
        tts.stop()
        sys.exit(0)
        
    else:
        tts.speak(f"Didn't understand: {cmd['raw']}")


def on_press(key):
    try:
        name = key.char
    except AttributeError:
        name = getattr(key, "name", "")
    if name and name.lower() == config.PUSH_TO_TALK_KEY:
        print("[*] listening...")
        tts.speak_now("Listening")
        text = recognizer.one_shot()
        if text:
            print(f"[heard] {text}")
            cmd = parser.parse(text)
            dispatch(cmd)
        else:
            print("[...] nothing recognized.")
            tts.speak("Nothing recognized")


def main():
    print(f"Voice assistant ready. Press {config.PUSH_TO_TALK_KEY} to speak.")
    
    # Start system tray icon
    tray.start()
    
    tts.speak_now("Voice assistant ready")
    
    with kb.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        tray.stop()
        tts.stop()