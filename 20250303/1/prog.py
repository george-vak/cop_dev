import cowsay
import shlex

field = [[0 for j in range(10)] for i in range(10)]
allowed_list = cowsay.char_names

def encounter(x, y):

    cow_function = getattr(cowsay, field[y][x]["name"])
    cow_function(field[y][x]["word"])

x, y = 0, 0
while inp := input():
    inp = shlex.split(inp)
    # print(inp)

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
            if len(inp) != 9:
                print("Invalid arguments <<1>>")
                continue

            curr_name = inp[1]
            if curr_name not in allowed_list:
                print("Cannot add unknown monster")
                continue

            m_x, m_y, curr_hp = 0, 0, 0
            curr_word = ""
            ii = 2
            while ii < 9:
                match inp[ii]:
                    case "hello":
                        curr_word = inp[ii+1]
                        ii += 1

                    case "hp":
                        try:
                            curr_hp = int(inp[ii+1])
                        except Exception:
                            break
                        if curr_hp < 1:
                            break
                        ii += 1

                    case "coords":
                        try:
                            m_x = int(inp[ii+1])
                            m_y = int(inp[ii+2])
                        except Exception:
                            break
                        if m_x < 0 or m_x > 9 or m_y < 0 or m_y > 9:
                            break
                        ii += 2
                ii += 1


            if field[m_y][m_x] == 0:
                print(f'Added monster {curr_name} to ({m_x}, {m_y}) saying {curr_word}')
            else:
                print(f'Replaced the old monster')


        else:
            print('Invalid command')

# addmon tux hello SIUUUU hp 120 coords 0 1
