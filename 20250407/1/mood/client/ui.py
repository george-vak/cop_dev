"""User interface file."""

import readline
import sys

import cowsay

from .config import JGSBAT_COW


class UIManager:
    """General class."""

    def __init__(self, username):
        """Configs.

        :param username: all clear.
        """
        self.username = username

        self.prompt = f"{self.username}> "

    def _print_error(self, message):
        """Func to write error client's messages.

        :param message: message
        :return: nth.
        """
        print(f"\r{message}")

    def display_server_message(self, message):
        """Func to ...

        :param message:
        :return: 0.
        """
        current_input = readline.get_line_buffer()
        sys.stdout.write("\r\033[K")
        if message.startswith("[Сервер] _meet"):
            sr, m, name, *words = message.split()
            self.encounter(name, " ".join(words))
        else:
            print(f"\r{message}")
        sys.stdout.write(f"\r{self.prompt}{current_input}")
        if current_input:
            sys.stdout.flush()

    def encounter(self, name, word):
        """Drawing monster upon encounter.

        :param name: mon's body
        :param word: mon's word(s)
        :return: 0.
        """
        if name == "jgsbat":
            print(f"\r{cowsay.cowsay(word, cowfile=JGSBAT_COW)}")
        else:
            print(f"\r{cowsay.cowsay(word, cow=name)}")
