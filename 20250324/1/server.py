import socket

x = 0
y = 0
field = [[0 for j in range(10)] for i in range(10)]

def handle_comm(comm):
    global x, y, field
    parts = comm.split()

    if parts[0] == "move":
        # move x y
        dx = int(parts[1])
        dy = int(parts[2])
        x = (x + dx) % 10
        y = (y + dy) % 10

        if field[y][x] == 0:
            return f"{x} {y}"
        else:
            name = field[y][x]['name']
            word = field[y][x]['word']
            return f"{name} {word}"
        
        
    elif parts[0] == "add":
        # add name x y word hp
        curr_name = str(parts[1])
        m_x = int(parts[2])
        m_y = int(parts[3])
        curr_word = str(parts[4])
        curr_hp = int(parts[5])
        
        if field[m_y][m_x] == 0:
            field[m_y][m_x] = {'name': curr_name, 'word': curr_word, 'hp': curr_hp}
            return f"Added monster {curr_name} to ({m_x}, {m_y}) saying {curr_word}"
        else:
            field[m_y][m_x] = {'name': curr_name, 'word': curr_word, 'hp': curr_hp}
            return f"Replaced the old monster"
        
        
    elif parts[0] == "attack":
        # attack name hit
        name = str(parts[1])
        hit = int(parts[2])
        
        if field[y][x] == 0:
            return f"No monster here"
        
        elif name != field[y][x]["name"]:
            return f"No {name} here"
        
        elif field[y][x]["hp"] <= hit:
            damag = field[y][x]["hp"]
            field[y][x] = 0
            return f"{name} 0 {damag}"
        
        else:
            field[y][x]["hp"] -= hit
            return f"{name} {field[y][x]['hp']} {hit}"
        
    else:
        return "smth happened write @donballon_b"


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
            print(f"Ошибка::::: {e}")
            
        finally:
            client_socket.close()
            print("<Клиент отключен.>")

if __name__ == "__main__":
    start_server()