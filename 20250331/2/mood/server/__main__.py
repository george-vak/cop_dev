"""Launch file."""

from mood.server.network import MUDChatServer

if __name__ == "__main__":
    server = MUDChatServer(host="0.0.0.0", port=5555)
    try:
        print("Запуск MUD-сервера...")
        server.run()
    except KeyboardInterrupt:
        server.shutdown()
