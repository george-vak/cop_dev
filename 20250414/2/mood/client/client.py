"""Client process main file."""

import threading
import time
from pathlib import Path

from .network import NetwManager
from .commands import CommandHandler
from .completer import CommandCompleter
from .ui import UIManager
from .config import get_allowed_monsters, ARSENAL


class MUDClient:
    """Cl class."""

    def __init__(self, username, host="127.0.0.1", port=5555):
        """Necessary configs.

        :param username:
        :param host: default 127.0.0.1
        :param port: 5555.
        """
        self.username = username
        self.ui = UIManager(username)
        self.network = NetwManager(host, port)
        self.completer = CommandCompleter()
        self.handler = CommandHandler(self.network, self.ui)
        self.running = True
        self.input_active = False
        self.allowed_commands = [
            "up",
            "down",
            "left",
            "right",
            "addmon",
            "attack",
            "exit",
            "help",
            "sayall",
        ]
        self.allowed_list = get_allowed_monsters()
        self.arsenal = ARSENAL

    def check_quee(self):
        """Queue loop checker.

        :return: 0.
        """
        while True:
            msg = self.network.message_queue.get()
            if msg:
                self.ui.display_server_message(msg)
            time.sleep(0.1)

    def connect(self, comm_file = None):
        """Allocating thread to a client.

        :return: 0.
        """
        try:
            if not self.network.connect(self.username):
                return

            print(self.network.socket.recv(1024).decode("utf-8"))

            threading.Thread(
                target=self.network.recv_message,
                daemon=True
            ).start()

            threading.Thread(
                target=self.check_quee,
                daemon=True
            ).start()

            if comm_file:
                try:
                    with open(comm_file, 'r') as f:
                        commands = [line.strip() for line in f if line.strip()]
                        for cmd in commands:
                            if not self.running:
                                break

                            print(f"{cmd}", end='\r\n')
                            if not self.handler.handle_command(cmd):
                                self.running = False
                            time.sleep(1.0)
                except FileNotFoundError:
                    print(f"Файл не найден: {comm_file}")
                    return
                finally:
                    self.running = False

            else:
                while self.running:
                    try:
                        self.input_active = True
                        cmd = input(f"{self.username}> ")
                        self.input_active = False

                        if not self.handler.handle_command(cmd):
                            self.running = False

                    except KeyboardInterrupt:
                        break

        except Exception as e:
            print(f"ошибка подключения: {e}")
        finally:
            self.running = False
            self.network.close()
            print("отключено")
