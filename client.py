from protocol import decoder
import asyncio
import conf


class Client:
    def __init__(self, host: str, port: int):
        self.reader = None
        self.client = None

        self.host = host
        self.port = port

    async def handle(self, reader, writer):
        self.reader = reader
        self.client = writer

        # connect 101xp server
        loop = asyncio.get_event_loop()
        loop.create_task(self.connect_server())
        
        while True:
            await asyncio.sleep(0.2)
            
            try:
                data = await reader.read(conf.BUFFER)
            except:
                break

            try:
                print(decoder.process(data))
            except:
                print(data)

            self.server.write(data)
            await self.server.drain()


    async def connect_server(self):
        reader, server = await asyncio.open_connection(self.host, self.port)
        self.server = server

        while True:
            await asyncio.sleep(0.2)
            
            try:
                data = await reader.read(conf.BUFFER)
            except:
                break

            try:
                print(decoder.process(data))
            except:
                print(data)

            self.client.write(data)
            await self.client.drain()
