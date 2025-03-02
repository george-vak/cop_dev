import sys
import cowsay

# Инициализация игрового поля
field_size = 10
field = [[None for _ in range(field_size)] for _ in range(field_size)]
player_pos = [0, 0]

def move_player(direction):
    global player_pos
    x, y = player_pos
    if direction == 'up':
        y = (y - 1) % field_size
    elif direction == 'down':
        y = (y + 1) % field_size
    elif direction == 'left':
        x = (x - 1) % field_size
    elif direction == 'right':
        x = (x + 1) % field_size
    player_pos = [x, y]
    print(f"Moved to ({x}, {y})")
    encounter(x, y)

def add_monster(name, x, y, hello):
<<<<<<< HEAD
=======
    # Проверка, что имя монстра есть в списке доступных существ
    if name not in cowsay.list_cows():
        print("Cannot add unknown monster")
        return
>>>>>>> b33ee56 (добавление в обработку команды addmon проверки того, что <name> - имя штатного существа)

def encounter(x, y):
    if field[x][y] is not None:
        monster = field[x][y]
        cowsay.cow(monster['hello'])

def process_command(command):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0]
    if cmd in ['up', 'down', 'left', 'right']:
        if len(parts) != 1:
            print("Invalid arguments")
            return
        move_player(cmd)
    elif cmd == 'addmon':
        if len(parts) != 5:
            print("Invalid arguments")
            return
        try:
            name = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            hello = parts[4]
            if not (0 <= x < field_size and 0 <= y < field_size):
                print("Invalid arguments")
                return
            add_monster(name, x, y, hello)
        except ValueError:
            print("Invalid arguments")
    else:
        print("Invalid command")

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            for line in file:
                process_command(line.strip())
    else:
        while True:
            try:
                command = input("> ")
                process_command(command)
            except EOFError:
                break

if __name__ == "__main__":
    main()
