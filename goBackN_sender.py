import socket
import random
import time
import logging
from collections import deque
from math import floor

# ---------------- CONFIG ----------------
SERVER_ADDR = ('localhost', 9999)
GBN_WINDOW_SIZE = 4
TOTAL_PACKETS = 10
ACK_WAIT_TIME = 3  # seconds
LOSS_PROBABILITY = 0.2

# ----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(message)s',
    datefmt='%H:%M:%S'
)

# ----------------------------------------
class BasicTimer:
    def __init__(self):
        self.start_time = None
        self.interval = None

    def start(self, interval):
        self.start_time = self.current_time_in_millis()
        self.interval = interval

    def has_timeout_occurred(self):
        if not self.start_time:
            return False
        cur_time = self.current_time_in_millis()
        return (cur_time - self.start_time) > self.interval * 1000

    def is_running(self):
        return self.start_time is not None

    def stop(self):
        self.start_time = None
        self.interval = None

    def restart(self, interval):
        self.start(interval)

    @staticmethod
    def current_time_in_millis():
        return int(floor(time.time() * 1000))


# ----------------------------------------
def send_packet(sock, seq_num):
    """Simulate sending a packet"""
    msg = f"PACKET:{seq_num}"
    if random.random() < LOSS_PROBABILITY:
        logging.warning(f"X Simulated loss of packet {seq_num}")
        return False
    sock.sendto(msg.encode(), SERVER_ADDR)
    logging.info(f"^ Sent {msg}")
    return True


# ----------------------------------------
def go_back_n_sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(ACK_WAIT_TIME)

    base = 0
    next_seq = 0
    window = deque()
    timer = BasicTimer()
    while base < TOTAL_PACKETS:
        # Send packets in window
        while next_seq < base + GBN_WINDOW_SIZE and next_seq < TOTAL_PACKETS:
            send_packet(sock, next_seq)
            window.append(next_seq)
            next_seq += 1

            if not timer.is_running():
                timer.start(ACK_WAIT_TIME)

        # Wait for ACK or timeout
        try:
            ack, _ = sock.recvfrom(1024)
            ack_num = int(ack.decode().split(':')[1])
            logging.info(f">> ACK {ack_num} received")

            # Slide window
            while window and window[0] <= ack_num:
                base = window.popleft() + 1
            if not window:
                timer.stop()
            else:
                timer.restart(ACK_WAIT_TIME)
        except socket.timeout:
            logging.warning("Timeout! Resending all packets in window.")
            for seq in list(window):
                send_packet(sock, seq)
            timer.restart(ACK_WAIT_TIME)
    sock.sendto("END".encode(), SERVER_ADDR)
    sock.close()
    logging.info(">> All packets sent successfully.")
# ----------------------------------------
if __name__ == "__main__":
    go_back_n_sender()
