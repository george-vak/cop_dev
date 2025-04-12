"""Commands handle file."""

class CommandHandler:
    """All commands handle class, no more."""

    def __init__(self, server):
        """Playground, arsenal init.

        Args:
            server: Reference to main server instance.
        """
        self.server = server
        self.field = [[0 for _ in range(10)] for _ in range(10)]
        self.arsenal = {"sword": 10, "spear": 15, "axe": 20}
        self.monsters = {}

    def handle_comm(self, comm, username):
        """Process incoming game command.

        Args:
            comm: Raw command string
            username: Player who sent command

        Returns:
            tuple: (personal_message, broadcast_message)
        """
        parts = comm.split()
        # print("=====")
        # print(parts)
        # print("=====")

        if parts[0] == "CHECK":
            # def move monster
            print(self.monsters)
            return "monster moved", "<where>"

        client_data = self.server.clients[username]
        x, y = client_data["x"], client_data["y"]

        if parts[0] == "move":
            dx, dy = int(parts[1]), int(parts[2])
            new_x = (x + dx) % 10
            new_y = (y + dy) % 10

            client_data["x"], client_data["y"] = new_x, new_y

            if self.field[new_y][new_x] == 0:
                person = f"[Сервер] Moved to {new_x} {new_y}"
                return person, None
            else:
                name = self.field[new_y][new_x]["name"]
                word = self.field[new_y][new_x]["word"]
                person = f"[Сервер] _meet {name} {word}"
                return person, None

        elif parts[0] == "addmon":
            curr_name = str(parts[1])
            m_x = int(parts[2])
            m_y = int(parts[3])
            curr_word = " ".join(parts[4:-1])
            curr_hp = int(parts[-1])

            if self.field[m_y][m_x] == 0:
                self.field[m_y][m_x] = {
                    "name": curr_name,
                    "word": curr_word,
                    "hp": curr_hp,
                }
                person = (
                    f"[Сервер] Added monster {curr_name} "
                    f"to ({m_x}, {m_y}) saying {curr_word}"
                )
                broadcast = (
                    f"[bcast] {username} added "
                    f"{curr_name} with {curr_hp} hp"
                )

            else:
                self.field[m_y][m_x] = {
                    "name": curr_name,
                    "word": curr_word,
                    "hp": curr_hp,
                }

                person = "[Сервер] Replaced the old monster"
                broadcast = (
                    f"[bcast] {username} replaced old monst "
                    f"on {curr_name} with {curr_hp} hp"
                )
            self.add_monster(m_x, m_y, curr_name, curr_hp, curr_word)
            return person, broadcast


        elif parts[0] == "attack":
            name = str(parts[1])
            weapon = str(parts[2])
            hit = self.arsenal[weapon]

            if self.field[y][x] == 0:
                person = "[Сервер] No monster here"
                return person, None

            elif name != self.field[y][x]["name"]:
                person = f"[Сервер] No {name} here"
                return person, None

            elif self.field[y][x]["hp"] <= hit:
                damag = self.field[y][x]["hp"]
                self.field[y][x] = 0
                self.del_monster(x, y)
                person = f"[Сервер] u killed {name} by {weapon} ({damag} hp)"
                broadcast = (
                    f"[bcast] {username} killed "
                    f"{name} by {weapon} ({damag} hp)"
                )
                return person, broadcast

            else:
                self.field[y][x]["hp"] -= hit
                self.monsters[(x, y)]["hp"] -= hit
                person = (
                    f"[Сервер] u hit {name} {hit} hp "
                    f"by {weapon} and now it has "
                    f"{self.field[y][x]['hp']} hp"
                )
                broadcast = (
                    f"[bcast] {username} attacked "
                    f"{name} by {weapon}, now it has "
                    f"{self.field[y][x]['hp']} hp"
                )
                return person, broadcast

        elif parts[0] == "exit":
            return "rem", username

        elif parts[0] == "sayall":
            person = None
            broadcast = f"[bcast] {username}: {' '.join(parts[1:])}"
            return person, broadcast

    def add_monster(self, x, y, name, hp, word):
        """Add monster to dict.

        :param x:
        :param y:
        :param name:
        :param hp:
        :param word:
        :return: 0.
        """
        self.monsters[(x, y)] = {
            "name": name,
            "hp": hp,
            "word": word,

        }
        # print(f"added {name} to ({x}, {y})")
        return

    def del_monster(self, x, y):
        """Delete monster from dict.

        :param x:
        :param y:
        :return: 0.
        """
        del self.monsters[(x, y)]
        # print(f"deleted mons from ({x, y})")
        return
