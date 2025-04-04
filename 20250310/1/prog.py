import cmd
from io import StringIO

import cowsay
import shlex


class MUD(cmd.Cmd):
    prompt = ">> "
    def __init__(self):
        super().__init__()
        self.x, self.y = 0, 0
        self.field = [[0 for j in range(10)] for i in range(10)]
        self.arsenal = {"sword": 10, "spear": 15, "axe": 20}

        self.jgsbat = cowsay.read_dot_cow(StringIO("""
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
        self.allowed_list = cowsay.list_cows() + ["jgsbat"]

    def encounter(self):
        if self.field[self.y][self.x] == 0:
            print(f'Moved to ({self.x}, {self.y})')
            return

        name = self.field[self.y][self.x]['name']
        word = self.field[self.y][self.x]['word']

        if name == "jgsbat":
            print(cowsay.cowsay(word, cowfile=self.jgsbat))
        else:
            print(cowsay.cowsay(word, cow=name))

    def do_up(self, arg):
        self.y = (self.y - 1) % 10
        self.encounter()

    def do_down(self, arg):
        self.y = (self.y + 1) % 10
        self.encounter()

    def do_right(self, arg):
        self.x = (self.x + 1) % 10
        self.encounter()

    def do_left(self, arg):
        self.x = (self.x - 1) % 10
        self.encounter()

    def do_addmon(self, arg):
        inp = shlex.split(arg)
        # print(inp)
        if len(inp) != 8:
            print("Invalid arguments <<кол-во>>")
            return

        curr_name = inp[0]
        if curr_name not in self.allowed_list and curr_name != "jgsbat":
            print("Cannot add unknown monster")
            return

        m_x, m_y, curr_hp = 0, 0, 0
        curr_word = ""
        ii = 1
        while ii < 8:
            # print(inp[ii])
            match inp[ii]:
                case "hello":
                    curr_word = inp[ii+1]
                    ii += 1

                case "hp":
                    try:
                        curr_hp = int(inp[ii+1])
                    except Exception:
                        print("Invalid command")
                        return
                    if curr_hp < 1:
                        print("Invalid command")
                        return
                    ii += 1

                case "coords":
                    try:
                        m_x = int(inp[ii+1])
                        m_y = int(inp[ii+2])
                    except Exception:
                        print("Invalid command")
                        return
                    if m_x < 0 or m_x > 9 or m_y < 0 or m_y > 9:
                        print("Invalid command")
                        return
                    ii += 2


            ii += 1


        if self.field[m_y][m_x] == 0:
            print(f'Added monster {curr_name} to ({m_x}, {m_y}) saying {curr_word}')
        else:
            print(f'Replaced the old monster')

        self.field[m_y][m_x] = {'name': curr_name, 'word': curr_word, 'hp': curr_hp}

    def do_attack(self, arg=""):
        if self.field[self.y][self.x] == 0:
            print(f"No monster here")
            return

        if not arg:
            print("Укажите имя монстра для атаки")
            return
        else:
            arg = shlex.split(arg)
        arg.append("sword")

        if arg[0] != self.field[self.y][self.x]["name"]:
            print(f"No {arg[0]} here")
            return

        if arg[1] == "with":
            if arg[2] in self.arsenal:
                weap = arg[2]
            else:
                print("Unknown weapon")
                return
        elif arg[1] == "sword":
            weap = arg[1]
        else:
            print("ожидается: attack <mons_name> with <weap_name>")
            return


        if self.field[self.y][self.x]["hp"] <= self.arsenal[weap]:
            print(f"{self.field[self.y][self.x]['name']} died")
            self.field[self.y][self.x] = 0
            return

        else:
            self.field[self.y][self.x]["hp"] -= self.arsenal[weap]
            print(f"{self.field[self.y][self.x]['name']} now has {
            self.field[self.y][self.x]['hp']}")

    def complete_attack(self, text, line, begidx, endidx):
        words = shlex.split(line[:endidx])
        if len(words) == 1:
            return self.allowed_list
        elif len(words) == 2:
            return [mons for mons in self.allowed_list if mons.startswith(text)]

        elif len(words) == 3 and words[2] == "with":
            return list(self.arsenal)
        elif len(words) == 4 and words[2] == "with":
            return [weap for weap in self.arsenal if weap.startswith(text)]
        return []


# пример команды
# addmon www hp 14 coords 0 0 hello "Who goes there?"

if __name__ == "__main__":
    MUD().cmdloop()
