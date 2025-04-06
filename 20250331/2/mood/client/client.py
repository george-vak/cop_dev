import threading
import time

from .network import NetwManager
from .commands import CommandHandler
from .completer import CommandCompleter
from .ui import UIManager
from .config import get_allowed_monsters, ARSENAL


class MUDClient:
    def __init__(self, username, host='127.0.0.1', port=5555):
        self.username = username
        self.ui = UIManager(username)
        self.network = NetwManager(host, port)
        self.completer = CommandCompleter()
        self.handler = CommandHandler(self.network, self.ui)
        self.running = True
        self.input_active = False
        self.allowed_commands = ["up", "down", "left", "right", "addmon", "attack", "exit", "help", "sayall"]
        self.allowed_list = get_allowed_monsters()
        self.arsenal = ARSENAL

    def check_quee(self):
        while True:
            msg = self.network.message_queue.get()
            if msg:
                self.ui.display_server_message(msg)
            time.sleep(0.1)

    def connect(self):
        try:
            if not self.network.connect(self.username):
                return

            print(self.network.socket.recv(1024).decode('utf-8'))

            threading.Thread(target=self.network.recv_message, daemon=True).start()

            threading.Thread(target=self.check_quee, daemon=True).start()


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