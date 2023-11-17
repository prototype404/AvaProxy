from client import Client
import requests
import asyncio
import conf
import web


# в данный момент не работает
# для работы требуется отправить на балансер
# сообщение Hello client
def get_server():
    """функция делает POST запрос на балансер аватарии для
       получения конфигурации игрового сервера 101xp"""
    
    balanser_url: str = "https://balancer.prod.ava.101xp.com/server"
    headers = {"User-Agent": "phone model"}

    response = requests.post(balanser_url, headers=headers)
    response = response.json()

    return response.get("server", "173.0.146.114:8123").split(":")


class Server:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        # start appconfig
        loop = asyncio.get_event_loop()
        loop.create_task(web.start())

    async def start(self):
        await asyncio.start_server(self.connection, 
                                   conf.HOST,
                                   conf.PORT)
        
    async def connection(self, reader, writer):
        print("New connection")
        loop = asyncio.get_event_loop()
        loop.create_task(Client(self.host, 
                                self.port).handle(reader, 
                                                  writer))


if __name__ == "__main__":
    ava_host, ava_port = get_server()
    ava_port = int(ava_port)

    server = Server(ava_host, ava_port)

    loop = asyncio.get_event_loop()
    loop.create_task(server.start())
    loop.run_forever()
