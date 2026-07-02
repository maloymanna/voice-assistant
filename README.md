# Local Windows Voice Assistant (Offline)

A lightweight offline voice-controlled assistant for Windows 11.

It allows you to control your PC using speech:
- Open/close applications
- Navigate browser (Edge)
- Control Excel / PowerPoint / Outlook
- Type dictated text
- Execute keyboard shortcuts
- Scroll, click, and navigate UI

---

## Features

### Applications
- Open Edge, Excel, Outlook, PowerPoint, Notepad++
- Close running applications
- Open common folders (Downloads, Documents, Desktop)

### Browser
- Open websites
- Google search
- New tab / close tab / refresh
- Back / forward navigation

### System control
- Copy / paste / undo / redo
- Save / save as
- Scroll up/down
- Page navigation
- Mouse clicks

### Dictation
- "Type ..." to dictate text into active window

---

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the assistant

```python main.py```

## Usage
Press ENTER and speak a command.

### Examples
```text
Open Edge
Open Excel
Open Outlook

Go to google dot com
Search for quarterly earnings

Type Hello everyone

Save
Copy
Paste
Undo

Scroll down
Scroll up

New tab
Close tab

Refresh
```

## Notes

- Uses Faster-Whisper for offline speech recognition
- No cloud APIs required
- Runs fully locally on CPU
- Designed for Windows 11

## Architecture
```text
Speech (Whisper)
    ↓
Command Parser
    ↓
Windows Actions
    ↓
Keyboard / Mouse / Apps / Browser
```

## Future upgrades

- Wake word activation
- Continuous dictation mode
- Local LLM fallback (Qwen 3 4B)
- UI automation (pywinauto enhancements)
- TTS feedback (Piper)
