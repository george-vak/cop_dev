import cowsay


field = [[0 for j in range(10)] for i in range(10)]
allowed_list = cowsay.char_names

def encounter(x, y):
    out = field[y][x].split()
    cow_function = getattr(cowsay, out[0])
    cow_function(out[1])

x, y = 0, 0
while inp := input():
    inp = inp.split()

    moved = 0
    if inp[0] == 'up':
        y = (y - 1) % 10
        moved = 1
    elif inp[0] == 'down':
        y = (y + 1) % 10
        moved = 1
    elif inp[0] == 'right':
        x = (x + 1) % 10
        moved = 1
    elif inp[0] == 'left':
        x = (x - 1) % 10
        moved = 1

    if moved == 1:
        print(f'Moved to ({x}, {y})')

        if field[y][x] != 0:
            encounter(x, y)
    else:
        if inp[0] == 'addmon':
            if len(inp) < 5:
                print("Invalid arguments")
                continue

            try:
                m_x = int(inp[2])
                m_y = int(inp[3])

                if m_x < 0 or m_x > 9 or m_y < 0 or m_y > 9:
                    raise Exception
            except Exception:
                print("Invalid arguments")
                continue

            if inp[1] not in allowed_list:
                print("Cannot add unknown monster")
                continue

            if field[m_y][m_x] == 0:
                print(f'Added monster {inp[1]} to ({m_x}, {m_y}) saying {inp[4]}')
            else:
                print(f'Replaced the old monster')

            field[m_y][m_x] = inp[1] + ' ' + inp[4]

        else:
            print('Invalid command')
