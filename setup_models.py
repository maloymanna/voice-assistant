"""Download the large 1.8GB Vosk model."""
import io, os, zipfile, urllib.request

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
TARGET_DIR = "models"
MODEL_NAME = "vosk-model-en-us-0.22"

def main():
    model_path = os.path.join(TARGET_DIR, MODEL_NAME)
    if os.path.isdir(model_path):
        print(f"[ok] Model already present at {model_path}")
        return

    os.makedirs(TARGET_DIR, exist_ok=True)
    print(f"[*] Downloading large Vosk model (~1.8 GB). This may take a while...")
    req = urllib.request.Request(MODEL_URL, headers={"User-Agent": "voice-assistant/1.0"})
    
    # Download with progress
    with urllib.request.urlopen(req) as r:
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        data_chunks = []
        while True:
            chunk = r.read(8192)
            if not chunk:
                break
            data_chunks.append(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\r[*] Downloading: {percent:.1f}%", end="", flush=True)
    
    print("\n[*] Extracting (this will take a minute)...")
    data = b"".join(data_chunks)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(TARGET_DIR)
    print(f"[ok] Model ready at {model_path}")

if __name__ == "__main__":
    main()