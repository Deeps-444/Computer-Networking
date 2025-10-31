import socket
import random
import logging
import time
LOSS_PROBABILITY = 0.2
RECEIVER_PORT = 9999
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(message)s',
                    datefmt='%H:%M:%S')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', RECEIVER_PORT))
expected_seq = 0
logging.info(f"Receiver started on port {RECEIVER_PORT}\n")
while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    if msg == "END":
        logging.info(">> All packets received. Closing connection.")
        break

    seq = int(msg.split(':')[1])

    # Simulate packet loss
    if random.random() < LOSS_PROBABILITY:
        logging.warning(f"XX Packet {seq} lost (simulated)")
        continue

    if seq == expected_seq:
        logging.info(f">> Packet {seq} received, sending ACK {seq}")
        sock.sendto(f"ACK:{seq}".encode(), addr)
        expected_seq += 1
    else:
        logging.warning(f"Unexpected packet {seq}, expected {expected_seq}. Sending last ACK.")
        sock.sendto(f"ACK:{expected_seq - 1}".encode(), addr)
    time.sleep(0.5)
