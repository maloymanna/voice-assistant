"""Download Vosk model from alphacephei.com"""
import io, os, sys, zipfile, urllib.request

# Small English model - good balance of size and accuracy
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
TARGET_DIR = "models"
MODEL_NAME = "vosk-model-small-en-us-0.15"

def main():
    model_path = os.path.join(TARGET_DIR, MODEL_NAME)
    if os.path.isdir(model_path):
        print(f"[ok] Model already present at {model_path}")
        return

    os.makedirs(TARGET_DIR, exist_ok=True)
    print(f"[*] Downloading Vosk model (~40 MB) from alphacephei.com...")
    req = urllib.request.Request(MODEL_URL, headers={"User-Agent": "voice-assistant/1.0"})
    with urllib.request.urlopen(req) as r:
        data = r.read()

    print("[*] Extracting...")
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(TARGET_DIR)
    print(f"[ok] Model ready at {model_path}")

if __name__ == "__main__":
    main()