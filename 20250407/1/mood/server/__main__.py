"""Launch file."""

from .network import MUDChatServer


if __name__ == "__main__":
    server = MUDChatServer(host="0.0.0.0", port=5555)
    try:
        print("Запуск MUD-сервера...")
        server.start()

        while True:
            pass

    except KeyboardInterrupt:
        server.shutdown()
    except Exception as e:
        print(f"Ошибка сервера: {str(e)}")
        server.shutdown()
