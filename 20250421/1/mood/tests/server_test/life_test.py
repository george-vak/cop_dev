import asyncio
import pytest
from server.network import MUDChatServer

@pytest.mark.asyncio
async def test_server_start_and_shutdown():
    server = MUDChatServer(port=0)

    server.async_loop = asyncio.get_running_loop()
    await server._run_async_server()
    assert server.server.sockets is not None
    port = server.server.sockets[0].getsockname()[1]
    assert port > 0

    print(f"[TEST] Сервер успешно запущен на порту: {port}")

    await server._async_shutdown()

    print("[TEST] Сервер успешно остановлен")
