import readline
import shlex
from .config import ALLOWED_COMMANDS, ARSENAL, get_allowed_monsters

class CommandCompleter:
    def __init__(self):
        self.allowed_list = get_allowed_monsters()
        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(" \t\n")

    def complete(self, text, state):
        line = readline.get_line_buffer()
        begidx = readline.get_begidx()
        endidx = readline.get_endidx()

        if line.startswith("attack"):
            return self.complete_attack(text, line, begidx, endidx)[state]
        elif line.startswith("addmon"):
            return self.complete_addmon(text, line, begidx, endidx)[state]
        else:
            return [cmd for cmd in ALLOWED_COMMANDS if cmd.startswith(text)][state]

    def complete_attack(self, text, line, begidx, endidx):
        words = shlex.split(line[:endidx])
        if len(words) == 1:
            return self.allowed_list
        elif len(words) == 2:
            return [mons for mons in self.allowed_list if mons.startswith(text)]
        elif len(words) == 3 and words[2] == "with":
            return list(ARSENAL.keys())
        elif len(words) == 4 and words[2] == "with":
            return [weap for weap in ARSENAL if weap.startswith(text)]
        return []

    def complete_addmon(self, text, line, begidx, endidx):
        words = shlex.split(line[:endidx])
        if len(words) == 1:
            return self.allowed_list
        elif len(words) == 2:
            return [mons for mons in self.allowed_list if mons.startswith(text)]