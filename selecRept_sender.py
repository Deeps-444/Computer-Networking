import socket
import time
import random
import logging
from math import floor

# ---------------- CONFIG ----------------
SERVER_ADDR = ('localhost', 9999)
TOTAL_PACKETS = 10
WINDOW_SIZE = 4
TIMEOUT = 2  # seconds
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

    def start(self):
        self.start_time = self.current_time_in_millis()

    def has_timeout_occurred(self, interval):
        if self.start_time is None:
            return False
        cur = self.current_time_in_millis()
        return (cur - self.start_time) > interval * 1000

    def restart(self):
        self.start_time = self.current_time_in_millis()

    def stop(self):
        self.start_time = None

    @staticmethod
    def current_time_in_millis():
        return int(floor(time.time() * 1000))


# ----------------------------------------
def send_packet(sock, seq_num):
    """Send a packet with simulated loss"""
    msg = f"PACKET:{seq_num}"
    if random.random() < LOSS_PROBABILITY:
        logging.warning(f"❌ Simulated loss of packet {seq_num}")
        return False
    sock.sendto(msg.encode(), SERVER_ADDR)
    logging.info(f"📤 Sent {msg}")
    return True
# ----------------------------------------
def selective_repeat_sender():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.5)

    base = 0
    next_seq = 0
    acked = [False] * TOTAL_PACKETS
    timers = [None] * TOTAL_PACKETS

    logging.info("Sender started (Selective Repeat)\n")

    while base < TOTAL_PACKETS:
        # Send packets within window
        while next_seq < base + WINDOW_SIZE and next_seq < TOTAL_PACKETS:
            send_packet(sock, next_seq)
            timers[next_seq] = BasicTimer()
            timers[next_seq].start()
            next_seq += 1

        # Receive ACKs
        try:
            data, _ = sock.recvfrom(1024)
            ack_num = int(data.decode().split(':')[1])
            logging.info(f"✅ ACK {ack_num} received")
            acked[ack_num] = True
            timers[ack_num] = None

            # Slide window forward
            while base < TOTAL_PACKETS and acked[base]:
                base += 1

        except socket.timeout:
            pass

        # Check for individual packet timeouts
        for i in range(base, min(base + WINDOW_SIZE, TOTAL_PACKETS)):
            if not acked[i] and timers[i] and timers[i].has_timeout_occurred(TIMEOUT):
                logging.warning(f"⏰ Timeout for packet {i}, retransmitting...")
                send_packet(sock, i)
                timers[i].restart()

    sock.sendto("END".encode(), SERVER_ADDR)
    sock.close()
    logging.info("\n✅ All packets sent successfully using Selective Repeat.")


# ----------------------------------------
if __name__ == "__main__":
    selective_repeat_sender()
