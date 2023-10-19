from aiohttp import web
import conf


async def appconfig(request):
    name = request.match_info.get("name", None)
    server = [conf.HOST, str(conf.PORT)]

    match name:

        case "server":
            result = web.json_response({"server": ":".join(server)})

        case _:
            result = web.Response(text="RU")

    return result


async def start():
    app = web.Application()
    app.add_routes(router())

    runner = web.AppRunner(app)

    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 80)
    await site.start()

def router() -> list:

    return [
        web.get( "/appconfig", appconfig),
        web.post("/appconfig/{name}", appconfig)
    ]
