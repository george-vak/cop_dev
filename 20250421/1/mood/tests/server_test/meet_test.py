# tests/server_test/meet_test.py
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
async def test_command_sequence(running_server):
    reader, writer = await asyncio.open_connection('127.0.0.1', running_server.port)
    
    writer.write("tester\n".encode())
    await writer.drain()
    await reader.read(1024)
    
    sequence = [
        ("movemonsters off\n", "Moving monsters: off"),

        ("addmon jgsbat 0 1 SIUUU 34\n", "Added monster jgsbat to (0, 1) saying SIUUU"),
        ("move 0 1\n", "[Сервер] _meet jgsbat SIUUU"),
        
        ("move 0 1\n", "Moved to 0 2"),
        ("addmon www 1 2 SIUUU 34\n", "Added monster www to (1, 2) saying SIUUU"),
        ("move 1 0\n", "[Сервер] _meet www SIUUU"),
        
        ("exit\n", "")
    ]
    
    for cmd, expected in sequence:
        writer.write(cmd.encode())
        await writer.drain()
        
        if cmd.strip() == "exit":
            break
            
        resp_bytes = await asyncio.wait_for(reader.read(1024), timeout=2.0)
        resp = resp_bytes.decode().strip()
        print(f"--> Response: `{resp}`")
        assert expected in resp, f"Команда `{cmd.strip()}` вернула `{resp}`, ожидалось `{expected}`"
        
    writer.close()
    await writer.wait_closed()