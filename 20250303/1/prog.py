from io import StringIO
import cowsay
import shlex

field = [[0 for j in range(10)] for i in range(10)]
allowed_list = cowsay.list_cows()

jgsbat = cowsay.read_dot_cow(StringIO("""
$the_cow = <<EOC;
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\\/o\\/o\\/'.   `(
      ) .' . \\====/ . '. (
       )  / <<    >> \\  (
        '-._/``  ``\\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
"""))

def encounter(x, y):
<<<<<<< HEAD
    name = field[y][x]['name']
    word = field[y][x]['word']

    if name == "jgsbat":
        print(cowsay.cowsay(word, cowfile=jgsbat))
    else:
        print(cowsay.cowsay(word, cow=name))
=======
    cow_function = getattr(cowsay, field[y][x]["name"])
    cow_function(field[y][x]["word"])
>>>>>>> de163f4 (финальная версия)

x, y = 0, 0
while inp := input():
    inp = shlex.split(inp)
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
            if curr_name not in allowed_list and curr_name != "jgsbat":
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

            field[m_y][m_x] = {'name': curr_name, 'word': curr_word, 'hp': curr_hp}

        else:
            print('Invalid command')

# пример команды
<<<<<<< HEAD
# addmon dragon hp 999 coords 0 1 hello "Who goes there?"
=======
# addmon dragon hp 999 coords 0 1 hello "Who goes there?"
>>>>>>> de163f4 (финальная версия)
