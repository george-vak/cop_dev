import socket

x = 0
y = 0
field = [[0 for j in range(10)] for i in range(10)]

def handle_comm(comm):
    global x, y
    if comm.startswith("move"):
        parts = comm.split()
        dx = int(parts[1])
        dy = int(parts[2])
        x = (x + dx) % 10
        y = (y + dy) % 10

        if field[y][x] == 0:
            return f"{x} {y}"
        else:
            return "aaaa"
    else:
        return "bbbb"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("<Сервер запущен>")

    while True:
        client_socket, addr = server_socket.accept()
        print("Подключен клиент:", addr)

        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print("команда:", data)
                if data.lower() == "exit":
                    exit()
                response = handle_comm(data)
                client_socket.send(response.encode())
        except Exception as e:
            print(f"Ошибка {e}")
        finally:
            client_socket.close()
            print("<Клиент отключен.>")

if __name__ == "__main__":
    start_server()