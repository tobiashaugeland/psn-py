import psn
import time
import socket
import json
import asyncio
import websockets

PSN_DEFAULT_UDP_PORT = 56565
PSN_DEFAULT_UDP_MCAST_ADDRESS = "236.10.10.10"

WS_PORT = 8000
WS_IP = "localhost"

# Global position variable
position = psn.Float3(0, 0, 0)


# Helper functions
def get_time_ms():
    return int(time.time() * 1000)


START_TIME = get_time_ms()


def get_elapsed_time_ms():
    return get_time_ms() - START_TIME


def pic_to_scene_coords(x, y):
    return x / 100, y / 100


async def handle_websocket(websocket):
    global position
    async for message in websocket:
        data = json.loads(message)
        x, y = pic_to_scene_coords(data["x"], data["y"])
        position = psn.Float3(x, y, 0)


async def run_psn_server():
    print("Starting PSN server")
    # Setup a UDP socket to send tracker packets on
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Encoder / Decoder
    encoder = psn.Encoder("Server 1")
    trackers = {}
    trackers[0] = psn.Tracker(0, "Tracker 0")
    trackers[0].set_pos(psn.Float3(0, 0, 0))

    last_sent_info = get_elapsed_time_ms()
    last_sent_data = get_elapsed_time_ms()

    packets = []

    async with websockets.serve(handle_websocket, WS_IP, WS_PORT):
        global position
        while True:
            time_stamp = get_elapsed_time_ms()

            # Approx 30 fps
            if time_stamp - last_sent_data >= 33:
                trackers[0].set_pos(position)
                packets.extend(encoder.encode_data(trackers, time_stamp))
                last_sent_data = time_stamp
                print(position.x, position.y, end="\r")

            if time_stamp - last_sent_info >= 1000:
                packets.extend(encoder.encode_info(trackers, time_stamp))
                last_sent_info = time_stamp

            for p in packets:
                sock.sendto(p, (PSN_DEFAULT_UDP_MCAST_ADDRESS, PSN_DEFAULT_UDP_PORT))

            packets.clear()

            await asyncio.sleep(0.001)


if __name__ == "__main__":
    asyncio.run(run_psn_server())
