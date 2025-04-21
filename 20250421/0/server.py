import asyncio
from Root import sqroots


async def echo(reader, writer):
    while data := await reader.readline():
        res = data.strip().decode()
        try:
            result = sqroots(res)
        except Exception:
            result = ""
        writer.write(f"{result}\n".encode())
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
