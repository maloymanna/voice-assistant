# voice-assistant

Lightweight, fully offline voice assistant for Windows 11.

## Install

```bash
git clone <this-repo> voice-assistant
cd voice-assistant
python -m pip install --user -r requirements.txt
python setup_models.py        # downloads ~50 MB model from GitHub
```

## Run

```bash
python main.py
```

Press **F9** to speak a command. Say `exit` to quit.

## Commands

| You say                                  | What happens                     |
|------------------------------------------|----------------------------------|
| `open edge` / `open excel` / `open outlook` | Launch app                     |
| `close notepad`                          | Kill process                     |
| `back` / `forward` / `refresh`           | Edge navigation                  |
| `new tab` / `close tab`                  | Edge tabs                        |
| `go to https://example.com`              | Navigate Edge                    |
| `search for python docs`                 | Bing search                      |
| `press control s` / `press alt f4`       | Any shortcut in `shortcuts.json` |
| `scroll up 5` / `scroll down`            | Mouse wheel                      |
| `click` / `right click` / `double click` | Mouse buttons                    |
| `type Hello world`                       | Paste typed text                 |
| `dictation`                              | Free dictation until `stop dictation` |
| `exit`                                   | Quit                             |

## Customising

- Edit **`shortcuts.json`** to add spoken names for any keystroke combo.
- Edit **`commands.py`** `_PATTERNS` list to add new phrases.
- Edit **`apps.py`** `_ALIASES` to add spoken names for your installed apps.
- Edit **`config.py`** to change model path, hotkey, timeouts.

## Architecture notes

- **Speech**: Vosk small English model (offline, ~50 MB).
- **Parsing**: regex-based, deterministic, easy to extend.
- **Actions**: pyautogui + pywin32 COM for Office.
- **Hotkey**: pynput global listener (no admin required).