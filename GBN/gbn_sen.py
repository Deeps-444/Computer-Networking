import socket
import struct
import time
import random

# =====================
# CONFIGURATION
# =====================
DEST_IP = "127.0.0.1"      # Receiver IP (localhost)
DEST_PORT = 10000          # Receiver port
WINDOW_SIZE = 4            # Number of packets that can be sent without ACK
TIMEOUT = 1.0              # Retransmission timeout (in seconds)
LOSS_PROB = 0.1            # Probability to simulate packet loss

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)  # Wait max 0.5s for ACK before checking timer

# Message data
messages = [f"Message {i}" for i in range(1, 21)]

# Sender state variables
base = 0                 # Oldest unacknowledged packet
next_seq = 0             # Next packet to send
sent_packets = {}        # Stores sent packets for retransmission
start_time = None        # Timer start time


# =====================
# PACKET CREATION
# =====================
def make_packet(seq, payload):
    """
    Packets = [4 bytes seq_no][payload bytes]
    """
    return struct.pack('!I', seq) + payload.encode()


# =====================
# TIMER FUNCTIONS
# =====================
def start_timer():
    global start_time
    start_time = time.time()

def timer_expired():
    if start_time is None:
        return False
    return (time.time() - start_time) > TIMEOUT


# =====================
# MAIN SENDING LOOP
# =====================
print("[Sender] Starting transmission...")

while base < len(messages):
    # 1️⃣ Send new packets within the window
    while next_seq < base + WINDOW_SIZE and next_seq < len(messages):
        pkt = make_packet(next_seq, messages[next_seq])
        sent_packets[next_seq] = pkt

        # Simulate packet loss
        if random.random() >= LOSS_PROB:
            sock.sendto(pkt, (DEST_IP, DEST_PORT))
            print(f"[Sender] Sent seq={next_seq}, payload='{messages[next_seq]}'")
        else:
            print(f"[Sender] Simulated loss of seq={next_seq}")

        # Start timer for first unACKed packet
        if base == next_seq:
            start_timer()

        next_seq += 1

    # 2️⃣ Wait for ACK
    try:
        data, _ = sock.recvfrom(1024)
        if len(data) >= 4:
            ack_seq = struct.unpack('!I', data[:4])[0]
            print(f"[Sender] Received ACK {ack_seq}")

            # Move window forward
            base = ack_seq + 1

            # Restart timer if there are still unACKed packets
            if base != next_seq:
                start_timer()
            else:
                start_time = None  # All acknowledged, stop timer

    except socket.timeout:
        pass  # No ACK received this round — check timer below

    # 3️⃣ Handle timeout
    if timer_expired():
        print(f"[Sender] Timeout! Retransmitting from base={base}")
        for seq in range(base, next_seq):
            pkt = sent_packets[seq]
            if random.random() >= LOSS_PROB:
                sock.sendto(pkt, (DEST_IP, DEST_PORT))
                print(f"[Sender] Retransmitted seq={seq}")
            else:
                print(f"[Sender] Simulated loss during retransmission seq={seq}")
        start_timer()

# Transmission complete
print("[Sender] All messages acknowledged. Transmission complete.")
sock.close()
