import socket
import threading
from queue import Queue
from time import sleep

field = [[0 for j in range(10)] for i in range(10)]


class MUDChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = {}
        print(f"Сервер запущен на {host}:{port}")
        self.arsenal = {"sword": 10, "spear": 15, "axe": 20}

        self.command_queue = Queue()
        self.lock = threading.Lock()
        self.running = False

    def broadcast(self, message, exclude_username=None):
        for name, data in list(self.clients.items()):
            if name != exclude_username:
                threading.Thread(
                    target=data['socket'].send,
                    args=(message.encode(),)
                ).start()

    def remove_client(self, username):
        if username in self.clients:
            self.clients[username]['socket'].close()
            del self.clients[username]
            self.broadcast(f"[bcast] {username} покинул игру")
            print(f"<Клиент {username} отключен.>")

    def handle_comm(self, comm, username, client):
        global field

        parts = comm.split()
        client_data = self.clients[username]
        x, y = client_data['x'], client_data['y']

        if parts[0] == "move":
            dx, dy = int(parts[1]), int(parts[2])
            new_x = (x + dx) % 10
            new_y = (y + dy) % 10

            client_data['x'], client_data['y'] = new_x, new_y

            if field[new_y][new_x] == 0:
                mess = f"Moved to {new_x} {new_y}"
                return f"[Сервер] {mess}"


            else:
                name = field[new_y][new_x]['name']
                word = field[new_y][new_x]['word']
                mess = f"_meet {name} {word}"
                return f"[Сервер] {mess}"


        elif parts[0] == "addmon":
            curr_name = str(parts[1])
            m_x = int(parts[2])
            m_y = int(parts[3])
            curr_word = str(parts[4])
            curr_hp = int(parts[5])

            if field[m_y][m_x] == 0:
                field[m_y][m_x] = {'name': curr_name, 'word': curr_word, 'hp': curr_hp}
                mess = f"Added monster {curr_name} to ({m_x}, {m_y}) saying {curr_word}"
                self.broadcast(f"[bcast] {username} added {curr_name} with {curr_hp} hp", exclude_username=username)
                return f"[Сервер] {mess}"
            else:
                field[m_y][m_x] = {'name': curr_name, 'word': curr_word, 'hp': curr_hp}
                mess = f"Replaced the old monster"
                self.broadcast(f"[bcast] {username} replaced old monst on {curr_name} with {curr_hp} hp", exclude_username=username)
                return f"[Сервер] {mess}"

        elif parts[0] == "attack":
            name = str(parts[1])
            weapon = str(parts[2])
            hit = self.arsenal[weapon]

            if field[y][x] == 0:
                mess = f"No monster here"
                return f"[Сервер] {mess}"

            elif name != field[y][x]["name"]:
                mess = f"No {name} here"
                return f"[Сервер] {mess}"

            elif field[y][x]["hp"] <= hit:
                damag = field[y][x]["hp"]
                field[y][x] = 0
                self.broadcast(f"[bcast] {username} killed {name} by {weapon} ({damag} hp)", exclude_username=username)
                return f"[Сервер] u killed {name} by {weapon} ({damag} hp)"

            else:
                field[y][x]["hp"] -= hit
                self.broadcast(f"[bcast] {username} attacked {name} by {weapon}, now it has {field[y][x]['hp']} hp", exclude_username=username)
                return f"[Сервер] u hit {name} {hit} hp by {weapon} and now it has {field[y][x]['hp']} hp"


        else:
            return "<<<1>>>"

    def handle_client(self, client):
        username = None
        try:
            username = client.recv(1024).decode().strip()

            if username in self.clients:
                client.send(f"ERROR: имя {username} занято. переподключитесь".encode())
                client.close()
                return

            with self.lock:
                self.clients[username] = {'socket': client, 'x': 0, 'y': 0}

            welcome_msg = f"[Сервер] Добро пожаловать, {username}! Ваша позиция: (0, 0)"
            client.send(welcome_msg.encode())

            self.broadcast(f"[bcast] {username} присоединился к игре!", exclude_username=username)

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
                    sleep(1.5)


        except Exception as e:
            print(f"Ошибка с клиентом {username}: {str(e)}")
        finally:
            if username:
                self.remove_client(username)

    def run(self):
        self.running = True
        threading.Thread(target=self.process_commands, daemon=True).start()

        try:
            while self.running:
                client, addr = self.server.accept()
                print(f"Подключен: {addr}")
                threading.Thread(target=self.handle_client, args=(client,)).start()
        except KeyboardInterrupt:
            print("\nСервер завершает работу...")
        finally:
            self.shutdown()

    def process_commands(self):
        while self.running:
            client, username, command = self.command_queue.get()

            with self.lock:
                sleep(1)
                response = self.handle_comm(command, username, client)

            threading.Thread(
                target=client.send,
                args=(f"{response}".encode(),)
            ).start()

    def shutdown(self):
        self.broadcast("[bcast] Сервер завершает работу. Отключение...\n")
        for username in list(self.clients.keys()):
            self.remove_client(username)
        self.server.close()
        print("Сервер остановлен")
        self.running = False


if __name__ == "__main__":
    server = MUDChatServer()
    server.run()