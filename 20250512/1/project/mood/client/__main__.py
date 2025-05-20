"""File launcher."""

import sys
from .client import MUDClient

def main():
    if len(sys.argv) < 2:
        print("Usage: client USERNAME [FILENAME]")
        sys.exit(1)

    username = sys.argv[1]
    command_file = sys.argv[3] if len(sys.argv) > 2 else None

    client = MUDClient(username)

    if command_file:
        client.connect(comm_file=command_file)
    else:
        client.connect()
        
if __name__ == "__main__":
    main()