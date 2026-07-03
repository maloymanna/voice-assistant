"""Map spoken phrases to structured commands.
Kept deliberately regex-based so it's easy to extend without an LLM."""
import re, json
import config

# (regex, action_name, group-extractor)
_PATTERNS = [
    # App control
    (r"^(?:open|launch|start|run)\s+(?:the\s+)?(.+)$",          "open_app"),
    (r"^(?:close|quit|exit|kill)\s+(?:the\s+)?(.+)$",           "close_app"),

    # Browser
    (r"^(?:go\s+)?(?:back|go\s+back)$",                         "browser_back"),
    (r"^(?:go\s+)?forward$",                                    "browser_forward"),
    (r"^refresh$",                                              "browser_refresh"),
    (r"^(?:new\s+tab|open\s+tab)$",                             "browser_new_tab"),
    (r"^(?:close\s+tab|close\s+this\s+tab)$",                   "browser_close_tab"),
    (r"^(?:go\s+to|open|navigate\s+to)\s+(https?://\S+)$",      "browser_goto"),
    (r"^(?:search|google|bing)\s+(?:for\s+)?(.+)$",             "browser_search"),

    # Dictation
    (r"^(?:start\s+)?dictation(?:\s+mode)?$",                   "enter_dictation"),
    (r"^(?:stop|exit|quit)(?:\s+assistant)?$",                  "exit"),

    # Shortcuts: "press control c", "hit alt f4", "do save"
    (r"^(?:press|hit|do|execute)\s+(.+)$",                      "shortcut_by_name"),

    # Mouse / scroll
    (r"^scroll\s+(up|down)(?:\s+(\d+))?$",                      "scroll"),
    (r"^(?:left\s+)?click$",                                    "click_left"),
    (r"^right\s+click$",                                        "click_right"),
    (r"^double\s*click$",                                       "click_double"),

    # Free-form typing (fallback)
    (r"^(?:type|write|say|dictate)\s+(.+)$",                    "type_text"),
]

class Parser:
    def __init__(self):
        try:
            with open(config.SHORTCUTS_FILE, encoding="utf-8") as f:
                self.shortcuts = json.load(f)
        except FileNotFoundError:
            self.shortcuts = {}
        # Build a fuzzy name -> shortcut map (lowercased)
        self._shortcut_by_name = {k.lower(): v for k, v in self.shortcuts.items()}

    def parse(self, text: str) -> dict:
        t = text.lower().strip()
        for pat, action in _PATTERNS:
            m = re.match(pat, t)
            if m:
                return {"action": action, "args": m.groups(), "raw": text}
        return {"action": "unknown", "args": (), "raw": text}

    def resolve_shortcut(self, spoken_name: str):
        """Return the keystroke string for a spoken shortcut name, or None."""
        key = spoken_name.lower().strip()
        # direct match
        if key in self._shortcut_by_name:
            return self._shortcut_by_name[key]
        # substring match
        for name, combo in self._shortcut_by_name.items():
            if key in name or name in key:
                return combo
        return None