"""
commands.py

Maps speech to actions.
"""

from apps import (
    open_application,
    close_application,
    open_folder,
)

from actions import *

from keyboard_actions import perform_shortcut


def execute(command: str):

    command = command.lower().strip()

    print(f"\nRecognized: {command}\n")

    # ----------------------------------
    # OPEN APPLICATION
    # ----------------------------------

    if command.startswith("open "):

        target = command.replace("open ", "", 1)

        if open_application(target):
            return

        if open_folder(target):
            return

        print("Unknown application or folder.")
        return

    # ----------------------------------
    # CLOSE APPLICATION
    # ----------------------------------

    if command.startswith("close "):

        target = command.replace("close ", "", 1)

        close_application(target)

        return

    # ----------------------------------
    # GOOGLE SEARCH
    # ----------------------------------

    if command.startswith("search for "):

        query = command.replace("search for ", "", 1)

        google_search(query)

        return

    # ----------------------------------
    # OPEN WEBSITE
    # ----------------------------------

    if command.startswith("go to "):

        site = command.replace("go to ", "", 1)

        site = site.replace(" dot ", ".")

        site = site.replace(" slash ", "/")

        open_url(site)

        return

    # ----------------------------------
    # TYPE TEXT
    # ----------------------------------

    if command.startswith("type "):

        text = command.replace("type ", "", 1)

        type_text(text)

        return

    # ----------------------------------
    # SCROLL
    # ----------------------------------

    if command == "scroll down":

        scroll_down()

        return

    if command == "scroll up":

        scroll_up()

        return

    if command == "page down":

        page_down()

        return

    if command == "page up":

        page_up()

        return

    # ----------------------------------
    # MOUSE
    # ----------------------------------

    if command == "click":

        click()

        return

    if command == "double click":

        double_click()

        return

    if command == "right click":

        right_click()

        return

    # ----------------------------------
    # CLIPBOARD
    # ----------------------------------

    if command == "clipboard":

        read_clipboard()

        return

    # ----------------------------------
    # SHORTCUTS
    # ----------------------------------

    if perform_shortcut(command):
        return

    print("Sorry, I don't know that command yet.")