import socket
import random
import logging
import time
RECEIVER_PORT = 9999
LOSS_PROBABILITY = 0.2
WINDOW_SIZE = 4
TOTAL_PACKETS = 10
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(message)s',
    datefmt='%H:%M:%S'
)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', RECEIVER_PORT))
expected_base = 0
received_buffer = [False] * TOTAL_PACKETS
logging.info(f"Receiver started (Selective Repeat) on port {RECEIVER_PORT}\n")
while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()
    if msg == "END":
        logging.info("All packets received. Closing connection.")
        break
    seq = int(msg.split(':')[1])
    # Simulate random loss
    if random.random() < LOSS_PROBABILITY:
        logging.warning(f" Simulated loss of packet {seq}")
        continue
    received_buffer[seq] = True
    logging.info(f"Packet {seq} received successfully.")
    # Send ACK immediately
    logging.info(f"Sending ACK {seq}")
    sock.sendto(f"ACK:{seq}".encode(), addr)
    while expected_base < TOTAL_PACKETS and received_buffer[expected_base]:
        expected_base += 1
    time.sleep(0.3)
