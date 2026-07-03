"""Main loop:
   1. Wait for push-to-talk key (F9 by default).
   2. Record one utterance.
   3. Parse + dispatch.
   4. Repeat until 'exit'."""
import sys
from pynput import keyboard as kb

import config
from speech import Recognizer
from commands import Parser
import actions, apps, browser, office, dictation as dictation_mod

recognizer = Recognizer()
parser = Parser()

def dispatch(cmd):
    a = cmd["action"]; args = cmd["args"]
    print(f"  -> {a} {args}")

    if a == "open_app":            apps.open_app(args[0])
    elif a == "close_app":         apps.close_app(args[0])
    elif a == "browser_back":      browser.back()
    elif a == "browser_forward":   browser.forward()
    elif a == "browser_refresh":   browser.refresh()
    elif a == "browser_new_tab":   browser.new_tab()
    elif a == "browser_close_tab": browser.close_tab()
    elif a == "browser_goto":      browser.goto(args[0])
    elif a == "browser_search":    browser.search(args[0])
    elif a == "enter_dictation":   dictation_mod.run(recognizer)
    elif a == "type_text":         actions.type_text(args[0])
    elif a == "scroll":            actions.scroll(args[0], args[1] or 5)
    elif a == "click_left":        actions.click_left()
    elif a == "click_right":       actions.click_right()
    elif a == "click_double":      actions.click_double()
    elif a == "shortcut_by_name":
        combo = parser.resolve_shortcut(args[0])
        if combo:
            actions.press(combo)
        else:
            print(f"  [!] unknown shortcut: {args[0]}")
    elif a == "exit":
        print("[bye] shutting down.")
        sys.exit(0)
    else:
        print(f"  [!] didn't understand: {cmd['raw']}")

def on_press(key):
    try:
        name = key.char
    except AttributeError:
        name = getattr(key, "name", "")
    if name and name.lower() == config.PUSH_TO_TALK_KEY:
        print("[*] listening...")
        text = recognizer.one_shot()
        if text:
            print(f"[heard] {text}")
            cmd = parser.parse(text)
            dispatch(cmd)
        else:
            print("[...] nothing recognized.")

def main():
    print(f"Voice assistant ready. Hold/press {config.PUSH_TO_TALK_KEY} to speak.")
    print("Say 'exit' to quit.")
    with kb.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()