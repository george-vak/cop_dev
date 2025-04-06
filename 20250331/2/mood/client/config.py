"""Configurations."""

from io import StringIO

import cowsay

ALLOWED_COMMANDS = [
    "up",
    "down",
    "left",
    "right",
    "addmon",
    "attack",
    "exit",
    "help",
    "sayall",
]
ARSENAL = {"sword": 10, "spear": 15, "axe": 20}

JGSBAT_COW = cowsay.read_dot_cow(
    StringIO(
        """
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
"""
    )
)


def get_allowed_monsters():
    """Monsters names to use.

    :return: list of names.
    """
    return cowsay.list_cows() + ["jgsbat"]
