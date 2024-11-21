import psn
import time
import socket
import requests
import json

PSN_DEFAULT_UDP_PORT = 56565
PSN_DEFAULT_UDP_MCAST_ADDRESS = "236.10.10.10"


# Helper functions
def get_time_ms():
    return int(time.time() * 1000)


START_TIME = get_time_ms()


def get_elapsed_time_ms():
    return get_time_ms() - START_TIME


def pic_to_scene_coords(x, y):
    return x / 100, y / 100

def run_psn_server():
    print("Starting PSN server")
    # Setup a UDP socket to send tracker packets on
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Encoder / Decoder
    encoder = psn.Encoder("Server 1")
    decoder = psn.Decoder()
    packets = []
    trackers = {}
    trackers[0] = psn.Tracker(0, "Tracker 0")
    trackers[0].set_pos(psn.Float3(0, 0, 0))

    last_sent_time = get_elapsed_time_ms()

    while True:
        # for id, tracker in trackers.items():
        #     old_x = tracker.get_pos().x if tracker.get_pos().x < 10 else -10
        #     tracker.set_pos(psn.Float3(old_x + 0.005, 0, 0))

        time_stamp = get_elapsed_time_ms()
        # if time_stamp % 16 == 0:
        if time_stamp - last_sent_time >= 32:
            r = requests.get("http://localhost:8000/mouse-position")
            data = r.json()
            x, y = pic_to_scene_coords(data["x"], data["y"])
            trackers[0].set_pos(psn.Float3(x, y, 0))
            packets.extend(encoder.encode_data(trackers, time_stamp))
            last_sent_time = time_stamp

        if time_stamp % 1000 == 0:
            packets.extend(encoder.encode_info(trackers, time_stamp))

        for p in packets:
            sock.sendto(p, (PSN_DEFAULT_UDP_MCAST_ADDRESS, PSN_DEFAULT_UDP_PORT))

        packets = []

        time.sleep(0.001)


if __name__ == "__main__":
    run_psn_server()
