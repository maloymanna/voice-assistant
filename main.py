"""
main.py

Entry point for Local Voice Assistant.
"""

import config

from speech import SpeechRecognizer
from commands import execute


def main():

    print(config.WELCOME)

    recognizer = SpeechRecognizer()

    while True:

        print("-" * 50)

        print("Press ENTER to record.")
        print("Type 'quit' to exit.")

        cmd = input("> ")

        if cmd.lower() == "quit":
            break

        from commands import execute

        text = recognizer.listen()

        if text.strip():

            execute(text)


if __name__ == "__main__":

    main()