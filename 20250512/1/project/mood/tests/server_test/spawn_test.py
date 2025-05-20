"""from mood: pytest -s -v tests/server_test/spawn_test.py"""


import asyncio
import pytest
import pytest_asyncio
from server.network import MUDChatServer

@pytest_asyncio.fixture(scope="function")
async def running_server():
    server = MUDChatServer(port=5555)
    server.start()
    await asyncio.sleep(0.2)
    yield server
    server.shutdown()
    await asyncio.sleep(0.2)

@pytest.mark.asyncio
@pytest.mark.parametrize("command, expected", [
    ("addmon www 0 1 privet mess 20\n", "Added monster www to (0, 1) saying privet mess"),
    ("addmon jgsbat 1 0 privet mess 20\n", "Added monster jgsbat to (1, 0) saying privet mess"),
    ("addmon tux 1 1 privet mess 34\n", "Added monster tux to (1, 1) saying privet mess"),
])
async def test_addmon_variations(running_server, command, expected):
    reader, writer = await asyncio.open_connection('127.0.0.1', running_server.port)
    writer.write("tester\n".encode())
    await writer.drain()
    await reader.read(1024)

    writer.write(command.encode())
    await writer.drain()
    resp = await asyncio.wait_for(reader.read(1024), timeout=2.0)
    assert expected in resp.decode()

    writer.write("exit\n".encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()
