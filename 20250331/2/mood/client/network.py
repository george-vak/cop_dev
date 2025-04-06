import socket
from queue import Queue

class NetwManager:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.running = True
        self.message_queue = Queue()

    def connect(self, username):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.send(username.encode('utf-8'))
            return True
        except Exception as e:
            print(f"ошибка подключения: {e}")
            return False

    def recv_message(self):
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.message_queue.put(data.decode('utf-8'))
            except Exception:
                break

    def send_command(self, cmd):
        if self.socket:
            self.socket.send(f"{cmd}\n".encode())
            return True
        return False

    def close(self):
        self.running = False
        if self.socket:
            self.socket.close()