"""File launcher."""

import sys

from .client import MUDClient

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python prog.py username")
        sys.exit(1)

    client = MUDClient(sys.argv[1])
    client.connect()
