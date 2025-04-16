"""File launcher."""

import sys
from .client import MUDClient

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m client.main USERNAME [FILENAME]")
        sys.exit(1)

    username = sys.argv[1]
    command_file = sys.argv[3] if len(sys.argv) > 2 else None

    client = MUDClient(username)

    if command_file:
        client.connect(comm_file=command_file)
    else:
        client.connect()