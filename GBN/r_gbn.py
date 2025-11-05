import struct
import time
import socket
import random

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 10001
LOSS_PROB = 0.1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

expected_seq = 0
delivered = 0

# function for sending acknowledgemnt
def send_ack(addr, seq):
    data = struct.pack('!I', seq)
    sock.sendto(data, addr)
    print(f"[Receiver] Sent ACK {seq}")


#MAIN LOOP
while True:
    packet, addr = sock.recvfrom(4096)

    #simulated loss
    if random.random() < LOSS_PROB:
        print("[Receiver] Simulated Loss of packet- dropped")
        continue
    
    if len(packet) < 4:
        print("[Receiver] packet too short")

    seq = struct.unpack('!I', packet[:4])[0]
    payload = packet[4:].decode(errors='ignore')

    if (seq == expected_seq):
        print("[Receiver] Received {seq} ")
        delivered += 1
        expected_seq +=1
        send_ack(addr, seq)
    else:
        last_inorder = expected_seq -1 if expected_seq -1 >0 else 0
        print("out of ordr pckts")
        send_ack(addr, last_inorder)