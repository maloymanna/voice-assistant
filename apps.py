"""
apps.py

Application launcher / closer.
"""

import os
import subprocess

import psutil

import config


def normalize(name: str) -> str:
    """
    Normalize spoken application names.
    """

    name = name.lower().strip()

    aliases = {
        "microsoft edge": "edge",
        "edge browser": "edge",
        "edge": "edge",

        "excel": "excel",
        "microsoft excel": "excel",

        "powerpoint": "powerpoint",
        "power point": "powerpoint",

        "outlook": "outlook",

        "notepad": "notepad",

        "notepad plus plus": "notepad++",
        "notepad plus": "notepad++",
        "notepad++": "notepad++",

        "calculator": "calculator",

        "paint": "paint",

        "file explorer": "explorer",
        "explorer": "explorer",
    }

    return aliases.get(name, name)


def open_application(name: str):

    name = normalize(name)

    exe = config.APPLICATIONS.get(name)

    if exe is None:
        print(f"Unknown application: {name}")
        return False

    try:
        subprocess.Popen(exe)
        print(f"Opened {name}")
        return True

    except Exception as e:
        print(e)
        return False


def close_application(name: str):

    name = normalize(name)

    exe = config.APPLICATIONS.get(name)

    if exe is None:
        return False

    exe = exe.lower()

    for proc in psutil.process_iter(["pid", "name"]):

        try:

            pname = proc.info["name"]

            if pname is None:
                continue

            if pname.lower() == exe:

                proc.terminate()

                print(f"Closed {name}")

                return True

        except Exception:
            pass

    return False


def open_folder(name: str):

    folder = config.FOLDERS.get(name.lower())

    if folder is None:
        return False

    os.startfile(folder)

    print(f"Opened {folder}")

    return True