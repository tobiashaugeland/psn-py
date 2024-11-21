import psn
import time
import socket

PSN_DEFAULT_UDP_PORT = 56565
PSN_DEFAULT_UDP_MCAST_ADDRESS = "236.10.10.10"


# Helper functions
def get_time_ms():
    return int(time.time() * 1000)


start_time = get_time_ms()


def get_elapsed_time_ms():
    return get_time_ms() - start_time


# Setup a UDP socket to send tracker packets on
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Encoder / Decoder
encoder = psn.Encoder("Server 1")
decoder = psn.Decoder()
packets = []
trackers = {}
trackers[0] = psn.Tracker(0, "Tracker 0")
trackers[0].set_pos(psn.Float3(0, 0, 0))

while True:
    for id, tracker in trackers.items():
        old_x = tracker.get_pos().x if tracker.get_pos().x < 10 else -10
        tracker.set_pos(psn.Float3(old_x + 0.005, 0, 0))

    time_stamp = get_elapsed_time_ms()
    if time_stamp % 16 == 0:
        packets.extend(encoder.encode_data(trackers, time_stamp))

    if time_stamp % 1000 == 0:
        packets.extend(encoder.encode_info(trackers, time_stamp))

    for p in packets:
        sock.sendto(p, (PSN_DEFAULT_UDP_MCAST_ADDRESS, PSN_DEFAULT_UDP_PORT))

    packets = []

    time.sleep(0.001)
