"""Network server file."""

import asyncio
import threading
from queue import Queue
from typing import Dict

from .handlers import CommandHandler
from .app import translate


class MUDChatServer:
    """Main game server class handling network connections and game logic."""

    def __init__(self, host="0.0.0.0", port=5555):
        """Initialize game server with network settings.

        Args:
            host (str) server IP address, default '0.0.0.0'.
            port (int) server port number, default 5555.
        """
        self.host = host
        self.port = port
        self.server = None
        self.clients: Dict[str, Dict] = {}
        self.command_queue = Queue()
        self.lock = threading.Lock()
        self.running = False
        self.handler = CommandHandler(self)
        self.async_loop = asyncio.get_event_loop()

        self.periodic_run = True
        self.periodic_interval = 15
        self.periodic_command = "CHECK"

    async def _periodic_worker(self):
        """Loop for periodic comm"""
        while self.periodic_run:
            await asyncio.sleep(self.periodic_interval)
            if self.periodic_run:
                self.command_queue.put(("SYSTEM", "PERIODIC", self.periodic_command))

    async def start_periodic(self):
        if hasattr(self, '_periodic_task') and not self._periodic_task.done():
            return

        self.periodic_run = True
        self._periodic_task = asyncio.create_task(self._periodic_worker())
        print("[Periodic] Запущено")

    async def stop_periodic(self):
        if not self.periodic_run:
            return
        self.periodic_run = False
        if hasattr(self, '_periodic_task'):
            self._periodic_task.cancel()
            try:
                await self._periodic_task
            except asyncio.CancelledError:
                pass
        print("[Periodic] Остановлено")

    async def broadcast(self, message, exclude_username=None):
        """Broadcasting.

        :param message: mess
        :param exclude_username: initiator, default None.
        """
        async with asyncio.Lock():
            tasks = []
            for username, data in self.clients.items():
                if username == exclude_username:
                    continue

                writer = data["writer"]
                locale = self.clients[username]["loc"]

                if isinstance(message, tuple):
                    template, params = message
                    localized = translate(template, locale, **params)
                else:
                    localized = message

                print(f"[bc] to {username} ({locale}): {localized}")
                tasks.append(self._safe_send(writer, localized))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_send(self, writer, message):
        """Solo send func

        :param writer:
        :param message:
        :return: 0.
        """
        try:
            writer.write(message.encode())
            await writer.drain()
        except Exception:
            pass

    def start(self):
        """Start function 2 threads.

        :return: 0.
        """
        self.running = True

        self.async_loop = asyncio.new_event_loop()
        threading.Thread(
            target=self._run_async_loop,
            name="AsyncLoopThread",
            daemon=True
        ).start()

        self.command_thread = threading.Thread(
            target=self._process_commands_loop,
            name="CommandProcessorThread",
            daemon=True,
        )
        self.command_thread.start()

        asyncio.run_coroutine_threadsafe(
            self._run_async_server(),
            self.async_loop
        )

    async def remove_client(self, username):
        """Disconnect user function.

        :param username: whom to disconnect.
        """
        if username in self.clients:
            writer = self.clients[username]["writer"]
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

            await self.broadcast(
                ("{username} left the game.", {"username": username}),
                exclude_username=username
            )
            print(f"{username} покинул сервер")
            del self.clients[username]

    async def handle_client(self, reader, writer):
        """General handling func.

        :param client: processing client.
        """
        username = None
        try:
            username = (await reader.read(1024)).decode().strip()

            if username in self.clients:
                writer.write(f"ERROR: имя {username} занято. "
                             f"переподключитесь".encode()
                             )
                await writer.drain()
                writer.close()
                return

            self.clients[username] = {"writer": writer, "x": 0, "y": 0, "loc": None}

            welcome_msg = f"<<< Welcome to Python-MUD 0.1 >>>"
            writer.write(welcome_msg.encode())
            await writer.drain()

            await self.broadcast(
                ("{username} joined the game!", {"username": username}),
                exclude_username=username
            )
            print(f"Новый игрок: {username}")

            buffer = ""
            while self.running:
                data = await reader.read(1024)
                if not data:
                    break

                data_str = data.decode()
                print(f"{username} команда: {data_str}")
                buffer += data_str
                while "\n" in buffer:
                    command, buffer = buffer.split("\n", 1)
                    self.command_queue.put((writer, username, command.strip()))

        except Exception as e:
            print(f"Ошибка с клиентом {username}: {str(e)}")
        finally:
            if username:
                if username and username in self.clients:
                    if not writer.is_closing():
                        writer.close()
                        await writer.wait_closed()
                    del self.clients[username]

    def _process_commands_loop(self):
        """Process commands loop.

        :return:
        """
        while self.running:
            try:
                writer, username, command = self.command_queue.get()
                command = str(command)
                if writer == "SYSTEM":
                    with self.lock:
                        res = self.handler.general_move()

                    if res is not None:
                        x, y, person_mess, cast_mess = res

                        print(x, y, person_mess, cast_mess)

                        for client in self.clients.values():
                            writer = client["writer"]
                            if client["x"] == x and client["y"] == y and person_mess:
                                asyncio.run_coroutine_threadsafe(
                                    self._safe_send(writer, person_mess),
                                    self.async_loop
                                )
                            elif cast_mess:
                                asyncio.run_coroutine_threadsafe(
                                    self._safe_send(writer, cast_mess),
                                    self.async_loop
                                )

                else:
                    if command.startswith("movemonsters"):
                        _, turn = command.split()[:2]
                        if turn == "on":
                            asyncio.run_coroutine_threadsafe(
                                self.start_periodic(),
                                self.async_loop
                            )
                        else:
                            asyncio.run_coroutine_threadsafe(
                                self.stop_periodic(),
                                self.async_loop
                            )
                        asyncio.run_coroutine_threadsafe(
                            self._safe_send(writer, f"Moving monsters: {turn}"),
                            self.async_loop
                        )

                    elif command == "exit":
                        asyncio.run_coroutine_threadsafe(
                            self.remove_client(username),
                            self.async_loop
                        )

                    else:
                        with self.lock:
                            person_mess, cast_mess = self.handler.handle_comm(
                                command, username
                            )
                        # print("### ", cast_mess, " ###")

                        if person_mess:
                            asyncio.run_coroutine_threadsafe(
                                self._safe_send(writer, person_mess),
                                self.async_loop
                            )
                        if cast_mess:
                            asyncio.run_coroutine_threadsafe(
                                self.broadcast(
                                    cast_mess,
                                    exclude_username=username
                                ),
                                self.async_loop,
                            )

            except Exception as e:
                print(f"[ERROR] Ошибка обработки команды: {command} :: {str(e)}")

    def _run_async_loop(self):
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_forever()

    async def _run_async_server(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        self.running = True
        print(f"Сервер запущен на {self.host}:{self.port}")
        await self.start_periodic()

    def shutdown(self):
        """Off server func.

        :return:
        """
        self.running = False
        future = asyncio.run_coroutine_threadsafe(
            self._async_shutdown(), self.async_loop
        )
        future.result()
        print("Сервер остановлен")

    async def _async_shutdown(self):
        """Off server func.

        :return:
        """
        await self.broadcast("Сервер завершает работу. "
                             "Отключение...\n")
        for username in list(self.clients.keys()):
            await self.remove_client(username)
        self.server.close()
        await self.server.wait_closed()
