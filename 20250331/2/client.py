import socket
import threading
import sys
import readline
from queue import Queue
import shlex
import cowsay
from io import StringIO


class MUDClient:
    def __init__(self, username, host='127.0.0.1', port=5555):
        self.username = username
        self.host = host
        self.port = port
        self.socket = None
        self.running = True
        self.message_queue = Queue()
        self.input_active = False
        self.allowed_commands = ["up", "down", "left", "right", "addmon", "attack", "exit", "help", "sayall"]

        self.jgsbat = cowsay.read_dot_cow(StringIO("""
        $the_cow = <<EOC;
            ,_                    _,
            ) '-._  ,_    _,  _.-' (
            )  _.-'.|\\--//|.'-._  (
             )'   .'\\/o\\/o\\/'.   `(
              ) .' . \\====/ . '. (
               )  / <<    >> \\  (
                '-._/``  ``\\_.-'
          jgs     __\\'--'//__
                 (((""`  `"")))
        EOC
        """))
        self.allowed_list = cowsay.list_cows() + ["jgsbat"]
        self.arsenal = {"sword": 10, "spear": 15, "axe": 20}

        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(" \t\n")

    def encounter(self, name, word):
        if name == "jgsbat":
            print(cowsay.cowsay(word, cowfile=self.jgsbat))
        else:
            print(cowsay.cowsay(word, cow=name))

    def complete(self, text, state):
        line = readline.get_line_buffer()
        begidx = readline.get_begidx()
        endidx = readline.get_endidx()

        if line.startswith("attack"):
            return self.complete_attack(text, line, begidx, endidx)[state]

        elif line.startswith("addmon"):
            return self.complete_addmon(text, line, begidx, endidx)[state]

        # elif line.startswith(("up", "down", "left", "right", "addmon")):
        #     return []

        else:
            # commands = ["up", "down", "left", "right", "addmon", "attack", "exit", "help"]
            return [cmd for cmd in self.allowed_commands if cmd.startswith(text)][state]

    def complete_attack(self, text, line, begidx, endidx):
        words = shlex.split(line[:endidx])
        if len(words) == 1:
            return self.allowed_list
        elif len(words) == 2:
            return [mons for mons in self.allowed_list if mons.startswith(text)]
        elif len(words) == 3 and words[2] == "with":
            return list(self.arsenal.keys())
        elif len(words) == 4 and words[2] == "with":
            return [weap for weap in self.arsenal if weap.startswith(text)]
        return []

    def complete_addmon(self, text, line, begidx, endidx):
        words = shlex.split(line[:endidx])
        if len(words) == 1:
            return self.allowed_list
        elif len(words) == 2:
            return [mons for mons in self.allowed_list if mons.startswith(text)]

    def send_command(self, cmd):
        if self.socket:
            self.socket.send(f"{cmd}\n".encode())
            return True
        return False

    def recv_message(self):
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.message_queue.put(data.decode('utf-8'))
                self.display_server_message()
            except Exception:
                break

    def _print_error(self, message):
        if self.input_active:
            current_input = readline.get_line_buffer()
            sys.stdout.write("\r" + " " * (len(current_input) + 50) + "\r")
            print(f"\r{message}", flush=True)
            sys.stdout.write(f"\r{self.username}> {current_input}")
            sys.stdout.flush()
        else:
            print(f"\r{message}")

    def display_server_message(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()

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

    def handle_command(self, cmd):
        if not cmd:
            return

        elif cmd == "exit":
            self.send_command("exit")
            self.running = False
            return

        parts = shlex.split(cmd)
        comm = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if comm == "up":
            self.send_command("move 0 -1")
        elif comm == "down":
            self.send_command("move 0 1")
        elif comm == "left":
            self.send_command("move -1 0")
        elif comm == "right":
            self.send_command("move 1 0")
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
            - exit 
            """
            print(help_text)

        elif comm == "sayall":

            if len(args) == 1:
                # print("\n", args)
                self.send_command(f"sayall {" ".join(args)}")
            else:
                print("not correct args")

        else:
            print("invalid command")
            return

    def handle_addmon(self, args):
        if len(args) != 8:
            self._print_error("Invalid arguments <<кол-во>>")
            return

        curr_name = args[0]
        if curr_name not in self.allowed_list and curr_name != "jgsbat":
            self._print_error("Cannot add unknown monster")
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

        self.send_command(f"addmon {curr_name} {m_x} {m_y} {curr_word} {curr_hp}")

    def handle_attack(self, args):
        if not args:
            self._print_error("Укажите имя монстра для атаки")
            return

        weapon = "sword"
        if len(args) >= 3 and args[1] == "with":
            if args[2] in self.arsenal:
                weapon = args[2]
            else:
                self._print_error("Unknown weapon")
                return

        self.send_command(f"attack {args[0]} {weapon}")

    def connect(self):
        try:
            """подкл выводим приветствие"""
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.send(self.username.encode('utf-8'))

            print(self.socket.recv(1024).decode('utf-8'))

            """заускаем отлов сообщений сервера"""
            threading.Thread(target=self.recv_message, daemon=True).start()

            while self.running:
                try:
                    self.input_active = True
                    cmd = input(f"{self.username}> ")
                    self.input_active = False

                    self.handle_command(cmd)

                except KeyboardInterrupt:
                    break

        except Exception as e:
            print(f"ошибка подключения: {e}")
        finally:
            self.running = False
            if self.socket:
                self.socket.close()
            print("отключено")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python prog.py username")
        sys.exit(1)

    client = MUDClient(sys.argv[1])
    client.connect()