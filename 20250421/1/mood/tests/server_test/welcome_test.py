import asyncio
import pytest
from server.network import MUDChatServer

@pytest.mark.asyncio
async def test_welcome_message():
    server = MUDChatServer(port=5555)
    server.async_loop = asyncio.get_running_loop()
    
    try:
        server_task = asyncio.create_task(server._run_async_server())
        await asyncio.sleep(0.2)
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection('127.0.0.1', 5555),
                timeout=2.0
            )
            
            writer.write("tester\n".encode())
            await writer.drain()
            
            welcome = await asyncio.wait_for(reader.read(1024), timeout=2.0)
            welcome_msg = welcome.decode().strip()
            
            assert welcome_msg == "<<< Welcome to Python-MUD 0.1 >>>"
            print(f"Received welc: {welcome_msg}")
            
            if hasattr(server, '_periodic_task'):
                server._periodic_task.cancel()
                try:
                    await asyncio.wait_for(server._periodic_task, timeout=1.0)
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    pass
                
            writer.write("exit\n".encode())
            await writer.drain()
            
        except asyncio.TimeoutError:
            pytest.fail("Test timed out waiting for server response")
        finally:
            if 'writer' in locals() and not writer.is_closing():
                writer.close()
                await writer.wait_closed()

    finally:
        shutdown_task = asyncio.create_task(server._async_shutdown())
        try:
            await asyncio.wait_for(shutdown_task, timeout=2.0)
        except asyncio.TimeoutError:
            shutdown_task.cancel()
            pytest.fail("Server shutdown timed out")

        if not server_task.done():
            server_task.cancel()
