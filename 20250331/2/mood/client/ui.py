import sys
import readline

import cowsay
from .config import JGSBAT_COW

class UIManager:
    def __init__(self, username):
        self.username = username
        self.input_active = False

    def _print_error(self, message):
        if self.input_active:
            current_input = readline.get_line_buffer()
            sys.stdout.write("\r" + " " * (len(current_input) + 50) + "\r")
            print(f"\r{message}", flush=True)
            sys.stdout.write(f"\r{self.username}> {current_input}")
            sys.stdout.flush()
        else:
            print(f"\r{message}")

    def display_server_message(self, message):
        if self.input_active:
            current_input = readline.get_line_buffer()
            sys.stdout.write("\r" + " " * (len(current_input) + 50) + "\r")
            '''обработать встречу с монстром - отрисовка'''
            if message.split()[1] == "_meet":
                slovo = " ".join(message.split()[3:])
                name = message.split()[2]
                self.encounter(name, slovo)
            else: print(f"\r{message}")
            sys.stdout.write(f"\r{self.username}> {current_input}")
            sys.stdout.flush()
        else:
            if message.split()[1] == "_meet":
                slovo = " ".join(message.split()[3:])
                name = message.split()[2]
                self.encounter(name, slovo)
            else: print(f"\r{message}")
            sys.stdout.write(f"\r{self.username}> ")
            sys.stdout.flush()

    def encounter(self, name, word):
        if name == "jgsbat":
            print(cowsay.cowsay(word, cowfile=JGSBAT_COW))
        else:
            print(cowsay.cowsay(word, cow=name))

