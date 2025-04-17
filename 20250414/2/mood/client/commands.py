"""Controlling commands file."""
import shlex
from .config import ARSENAL, get_allowed_monsters


class CommandHandler:
    """Controlling commands class."""

    def __init__(self, network, ui):
        """Necessary configs.

        :param network:
        :param ui: units.
        """
        self.network = network
        self.ui = ui
        self.allowed_list = get_allowed_monsters()
        self.arsenal = ARSENAL

    def handle_command(self, cmd):
        """General loop.

        :param cmd:
        :return: 0.
        """
        if not cmd:
            return True

        elif cmd == "exit":
            self.network.send_command("exit")
            return False

        parts = shlex.split(cmd)
        comm = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if comm == "up":
            self.network.send_command("move 0 -1")
        elif comm == "down":
            self.network.send_command("move 0 1")
        elif comm == "left":
            self.network.send_command("move -1 0")
        elif comm == "right":
            self.network.send_command("move 1 0")
        elif comm == "addmon":
            self.handle_addmon(args)
        elif comm == "attack":
            self.handle_attack(args)
        elif comm == "help":
            help_text = """
            Доступные команды:
            - up/down/left/right
            - addmon www hello "privet mess" hp 34 coords 0 1
            - attack www [with axe]
            - sayall "bcast message"
            - movemonsters "on/off"
            - exit
            """
            print(help_text)

        elif comm == "movemonsters":
            if args[0] == "on" or args[0] == "off":
                self.network.send_command(f"{comm} {args[0]}")
            else:
                self.ui._print_error("not correct args: use on/off")

        elif comm == "sayall":
            if len(args) == 1:
                self.network.send_command(f"sayall {" ".join(args)}")
            else:
                self.ui._print_error("not correct args")
        else:
            self.ui._print_error("invalid command")
        return True

    def handle_addmon(self, args):
        """Addmon handle.

        :param args:
        :return: 0.
        """
        if len(args) != 8:
            self.ui._print_error("Invalid arguments <<кол-во>>")
            return

        curr_name = args[0]
        if curr_name not in self.allowed_list and curr_name != "jgsbat":
            self.ui._print_error("Cannot add unknown monster")
            return

        m_x, m_y, curr_hp = 0, 0, 0
        curr_word = ""
        ii = 1
        while ii < 8:
            match args[ii]:
                case "hello":
                    curr_word = args[ii + 1]
                    ii += 1
                case "hp":
                    try:
                        curr_hp = int(args[ii + 1])
                        if curr_hp < 1:
                            raise ValueError
                    except ValueError:
                        self._print_error("Invalid hp value")
                        return
                    ii += 1
                case "coords":
                    try:
                        m_x = int(args[ii + 1])
                        m_y = int(args[ii + 2])
                        if not (0 <= m_x <= 9 and 0 <= m_y <= 9):
                            raise ValueError
                    except ValueError:
                        self._print_error("Invalid coordinates")
                        return
                    ii += 2
            ii += 1

        self.network.send_command(
            f"addmon {curr_name} {m_x} {m_y} {curr_word} {curr_hp}"
        )

    def handle_attack(self, args):
        """Attack handle.

        :param args:
        :return: 0.
        """
        if not args:
            self.ui._print_error("Укажите имя монстра для атаки")
            return

        weapon = "sword"
        if len(args) >= 3 and args[1] == "with":
            if args[2] in self.arsenal:
                weapon = args[2]
            else:
                self.ui._print_error("Unknown weapon")
                return

        self.network.send_command(f"attack {args[0]} {weapon}")
