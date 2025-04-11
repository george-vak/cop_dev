"""Network server file."""

import socket
import threading
from queue import Queue
from time import sleep

from .handlers import CommandHandler


class MUDChatServer:
    """Main game server class handling network connections and game logic."""

    def __init__(self, host="0.0.0.0", port=5555):
        """Initialize game server with network settings.

        Args:
            host (str) server IP address, default '0.0.0.0'.
            port (int) server port number, default 5555.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = {}
        self.command_queue = Queue()
        self.lock = threading.Lock()
        self.running = False
        self.handler = CommandHandler(self)
        print(f"Сервер запущен на {host}:{port}")

    def broadcast(self, message, exclude_username=None):
        """Broadcasting.

        :param message: mess
        :param exclude_username: initiator, default None.
        """
        with self.lock:
            for name, data in list(self.clients.items()):
                if name != exclude_username:
                    try:
                        threading.Thread(
                            target=data["socket"].send,
                            args=(message.encode(),)
                        ).start()
                    except Exception:
                        self.remove_client(name)

    def remove_client(self, username):
        """Disconnect user function.

        :param username: whom to disconnect.
        """
        if username in self.clients:
            self.clients[username]["socket"].close()
            self.broadcast(
                f"[bcast] {username} покинул игру", exclude_username=username
            )
            del self.clients[username]
            print(f"{username} покинул сервер")

    def handle_client(self, client):
        """General handling func.

        :param client: processing client.
        """
        username = None
        try:
            username = client.recv(1024).decode().strip()

            if username in self.clients:
                client.send(f"ERROR: имя {username} занято. "
                            f"переподключитесь".encode()
                            )
                client.close()
                return

            with self.lock:
                self.clients[username] = {"socket": client, "x": 0, "y": 0}

            welcome_msg = (f"[Сервер] Добро пожаловать, "
                           f"{username}! Ваша позиция: (0, 0)"
                           )
            client.send(welcome_msg.encode())

            self.broadcast(
                f"[bcast] {username} присоединился к игре!",
                exclude_username=username
            )
            print(f"Новый игрок: {username}")

            buffer = ""
            while self.running:
                data = client.recv(1024).decode()
                if not data:
                    break

                print(f"{username} команда: {data}")
                buffer += data
                while "\n" in buffer:
                    command, buffer = buffer.split("\n", 1)
                    self.command_queue.put((client, username, command.strip()))

        except Exception as e:
            print(f"Ошибка с клиентом {username}: {str(e)}")
            if username:
                self.remove_client(username)

    def process_commands(self):
        """Process commands loop.

        :return:
        """
        while self.running:
            client, username, command = self.command_queue.get()

            if command == "exit":
                self.remove_client(username)

            else:

                with self.lock:
                    sleep(1)
                    person_mess, cast_mess = self.handler.handle_comm(
                        command, username
                    )

                if person_mess:
                    threading.Thread(
                        target=client.send, args=(f"{person_mess}".encode(),)
                    ).start()
                if cast_mess:
                    self.broadcast(cast_mess, exclude_username=username)

    def run(self):
        """Run loop.

        :return:
        """
        self.running = True
        threading.Thread(target=self.process_commands, daemon=True).start()

        try:
            while self.running:
                client, addr = self.server.accept()
                print(f"Подключен: {addr}")
                threading.Thread(
                    target=self.handle_client,
                    args=(client,)
                ).start()
        except Exception:
            print("\nСервер завершает работу...")
            exit(1)
        finally:
            self.shutdown()

    def shutdown(self):
        """Off server func.

        :return:
        """
        self.running = False
        self.broadcast("[bcast] Сервер завершает работу. Отключение...\n")
        for username in list(self.clients.keys()):
            self.remove_client(username)
        self.server.close()
        print("Сервер остановлен")
