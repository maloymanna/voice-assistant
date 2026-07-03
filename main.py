"""Main loop with TTS feedback."""
import sys
from pynput import keyboard as kb

import config
from speech import Recognizer
from commands import Parser
import actions, apps, browser, office, dictation as dictation_mod
import tts

recognizer = Recognizer()
parser = Parser()

def dispatch(cmd):
    a = cmd["action"]; args = cmd["args"]
    print(f"  -> {a} {args}")

    # Speak the command for feedback
    tts.speak(cmd["raw"])

    if a == "open_app":
        apps.open_app(args[0])
        tts.speak(f"Opening {args[0]}")
    elif a == "close_app":
        apps.close_app(args[0])
        tts.speak(f"Closing {args[0]}")
    elif a == "browser_back":
        browser.back()
        tts.speak("Going back")
    elif a == "browser_forward":
        browser.forward()
        tts.speak("Going forward")
    elif a == "browser_refresh":
        browser.refresh()
        tts.speak("Refreshing")
    elif a == "browser_new_tab":
        browser.new_tab()
        tts.speak("New tab")
    elif a == "browser_close_tab":
        browser.close_tab()
        tts.speak("Closing tab")
    elif a == "browser_goto":
        browser.goto(args[0])
        tts.speak(f"Navigating to {args[0]}")
    elif a == "browser_search":
        browser.search(args[0])
        tts.speak(f"Searching for {args[0]}")
    elif a == "enter_dictation":
        tts.speak_now("Starting dictation")
        dictation_mod.run(recognizer)
        tts.speak("Dictation ended")
    elif a == "type_text":
        actions.type_text(args[0])
        tts.speak(f"Typed {args[0]}")
    elif a == "scroll":
        actions.scroll(args[0], args[1] or 5)
        tts.speak(f"Scrolling {args[0]}")
    elif a == "click_left":
        actions.click_left()
        tts.speak("Click")
    elif a == "click_right":
        actions.click_right()
        tts.speak("Right click")
    elif a == "click_double":
        actions.click_double()
        tts.speak("Double click")
    elif a == "shortcut_by_name":
        combo = parser.resolve_shortcut(args[0])
        if combo:
            actions.press(combo)
            tts.speak(f"Pressed {args[0]}")
        else:
            tts.speak(f"Unknown shortcut {args[0]}")
    elif a == "exit":
        tts.speak_now("Shutting down")
        tts.stop()
        sys.exit(0)
    else:
        tts.speak(f"Didn't understand {cmd['raw']}")

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
    tts.speak_now("Voice assistant ready")
    with kb.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    finally:
        tts.stop()