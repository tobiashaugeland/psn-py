import psn
import time
import socket
import json
from aiohttp import web
import logging

PSN_DEFAULT_UDP_PORT = 56565
PSN_DEFAULT_UDP_MCAST_ADDRESS = "236.10.10.10"

PORT = 8000
IP = "0.0.0.0"
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def get_time_ms():
    return int(time.time() * 1000)


START_TIME = get_time_ms()


def get_elapsed_time_ms():
    return get_time_ms() - START_TIME


def pic_to_scene_coords(x, y):
    return x / 200, y / 200


def send_position(x: float, y: float, id: int = 0):
    global SOCK

    encoder = psn.Encoder("Server 1")
    tracker = psn.Tracker(id, f"Tracker {id}")
    tracker.set_pos(psn.Float3(x, y, 0))
    packet = encoder.encode_data(tracker, get_elapsed_time_ms())
    SOCK.sendto(packet, (PSN_DEFAULT_UDP_MCAST_ADDRESS, PSN_DEFAULT_UDP_PORT))


async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            logging.debug("Received message: %s" % msg.data)

            # data = json.loads(msg.data)
            # x, y = pic_to_scene_coords(data["x"], data["y"])
            # send_position(x, y)
            # ws.send_str(json.dumps({"x": x, "y": y}))
        elif msg.type == web.WSMsgType.ERROR:
            logging.error("ws connection closed with exception %s" % ws.exception())
            # print("ws connection closed with exception %s" % ws.exception())

    return ws



async def handle_root(request):
    return web.FileResponse("./static/index.html")


def create_app():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_static("/", "./static")
    app.router.add_get("/ws", handle_websocket)
    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(create_app(), host=IP, port=PORT)
