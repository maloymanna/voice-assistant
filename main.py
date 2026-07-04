"""Main event loop with Wake Word, F9 override, and Ctrl+Q quit."""
import sys
import time
import winsound
from pynput import keyboard as kb

import config
from speech import Recognizer
from commands import Parser
import actions, apps, browser, office, dictation as dictation_mod
import tts
import tray
import wakeword

recognizer = Recognizer()
parser = Parser()

# State flags
f9_pressed = False
quit_requested = False

def play_beep():
    """Subtle confirmation beep using built-in Windows sound."""
    winsound.Beep(1000, 150)  # 1000Hz for 150ms

def on_key_press(key):
    global f9_pressed, quit_requested
    
    # Check for F9 (Push to talk)
    try:
        if hasattr(key, 'char') and key.char and key.char.lower() == config.PUSH_TO_TALK_KEY:
            f9_pressed = True
            return
    except AttributeError:
        pass
        
    if hasattr(key, 'name') and key.name == config.PUSH_TO_TALK_KEY:
        f9_pressed = True
        return

    # Check for Ctrl+Q (Quit)
    if key == kb.Key.ctrl_l or key == kb.Key.ctrl_r:
        # We need to track if 'q' is pressed while ctrl is held. 
        # pynput's GlobalHotKeys is better for combos, but let's keep it simple:
        pass 

# Better approach for Ctrl+Q using pynput's built-in combo listener
def on_ctrl_q():
    global quit_requested
    print("\n[!] Ctrl+Q pressed. Quitting immediately.")
    quit_requested = True

def process_command():
    """Listen for a command, handle retries, and dispatch."""
    global quit_requested
    
    for attempt in range(config.MAX_RETRIES + 1):
        if attempt > 0:
            tts.speak_now("Please repeat.")
            
        text, confidence = recognizer.one_shot()
        print(f"[heard] '{text}' (confidence: {confidence:.2f})")
        
        if not text:
            tts.speak("I didn't hear anything.")
            return
            
        if confidence < config.CONFIDENCE_THRESHOLD and attempt < config.MAX_RETRIES:
            tts.speak(f"I'm not sure I caught that. (Confidence {confidence:.0%})")
            continue
            
        # We have a valid command
        cmd = parser.parse(text)
        dispatch(cmd)
        
        if cmd["action"] == "exit":
            quit_requested = True
            
        return

    tts.speak("I couldn't understand you after multiple tries.")

def dispatch(cmd):
    a = cmd["action"]; args = cmd["args"]
    print(f"  -> {a} {args}")

    if a == "open_app":
        name = args[0]
        tts.speak(f"Opening {name}")
        apps.open_app(name)
        time.sleep(1.5)
        tts.speak(f"{name} opened")
    elif a == "close_app":
        name = args[0]
        tts.speak(f"Closing {name}")
        apps.close_app(name)
        time.sleep(0.5)
        tts.speak(f"{name} closed")
    elif a == "browser_back":
        tts.speak("Going back"); browser.back()
    elif a == "browser_forward":
        tts.speak("Going forward"); browser.forward()
    elif a == "browser_refresh":
        tts.speak("Refreshing"); browser.refresh()
    elif a == "browser_new_tab":
        tts.speak("New tab"); browser.new_tab()
    elif a == "browser_close_tab":
        tts.speak("Closing tab"); browser.close_tab()
    elif a == "browser_goto":
        tts.speak(f"Navigating to {args[0]}"); browser.goto(args[0])
    elif a == "browser_search":
        tts.speak(f"Searching for {args[0]}"); browser.search(args[0])
    elif a == "enter_dictation":
        tts.speak_now("Starting dictation")
        dictation_mod.run(recognizer)
        tts.speak("Dictation ended")
    elif a == "type_text":
        tts.speak(f"Typing {args[0]}"); actions.type_text(args[0])
    elif a == "scroll":
        tts.speak(f"Scrolling {args[0]}"); actions.scroll(args[0], args[1] or 5)
    elif a == "click_left":
        tts.speak("Click"); actions.click_left()
    elif a == "click_right":
        tts.speak("Right click"); actions.click_right()
    elif a == "click_double":
        tts.speak("Double click"); actions.click_double()
    elif a == "shortcut_by_name":
        combo = parser.resolve_shortcut(args[0])
        if combo:
            tts.speak(f"Pressing {args[0]}"); actions.press(combo)
        else:
            tts.speak(f"Unknown shortcut {args[0]}")
    elif a == "exit":
        tts.speak_now("Shutting down")
    elif a == "unknown":
        tts.speak(f"I didn't understand '{cmd['raw']}'.")

def main():
    global f9_pressed, quit_requested
    
    print(f"Voice assistant starting...")
    
    # 1. Start System Tray
    tray.start()
    
    # 2. Start Wake Word Listener (Background Thread)
    wakeword.start()
    
    # 3. Start Global Hotkey Listeners
    # F9 for push-to-talk, Ctrl+Q for instant quit
    hotkey_listener = kb.GlobalHotKeys({
        '<ctrl>+q': on_ctrl_q,
    })
    hotkey_listener.start()
    
    # We still need a standard listener for F9 because GlobalHotKeys 
    # doesn't handle single function keys well across all layouts.
    f9_listener = kb.Listener(on_press=on_key_press)
    f9_listener.start()

    tts.speak_now(f"Voice assistant ready. Say '{config.WAKE_WORD_NAME}' or press F9.")
    
    # 4. Main Event Loop
    try:
        while not quit_requested:
            # Check if triggered by Wake Word or F9
            triggered = wakeword.check_and_reset() or f9_pressed
            f9_pressed = False # Reset flag
            
            if triggered:
                play_beep()
                process_command()
            
            # Small sleep to prevent CPU spinning in the main loop
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        pass
    finally:
        print("[*] Cleaning up...")
        hotkey_listener.stop()
        f9_listener.stop()
        wakeword.stop()
        tray.stop()
        tts.stop()
        print("[*] Goodbye.")

if __name__ == "__main__":
    main()