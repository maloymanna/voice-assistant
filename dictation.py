"""Free-form dictation. Streams transcripts and types them out,
until the user says one of the stop phrases."""
import actions
import config

def run(recognizer):
    print("[dictation] speaking... say 'stop dictation' to end.")
    buf = []
    for text in recognizer.stream():
        if text.lower().strip() in config.DICTATION_STOP_PHRASES:
            break
        # Capitalize first word of each chunk for readability
        pretty = text[0].upper() + text[1:] if text else text
        actions.type_text(pretty + " ")
        buf.append(text)
    print(f"[dictation] ended. Typed {len(buf)} chunk(s).")