import socket
import struct
import random

#configurations
LISTEN_IP = '127.0.0.1' # receiver ip =>localhost
LISTEN_PORT = 10000
LOSS_PROB = 0.1

# creating sockets and binding them
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))
print(f"[Receiver] Listening on {LISTEN_IP}: {LISTEN_PORT}")

#initialise state var
expected_seq = 0 #next expected seq number
delivered = 0  # number of deliverd packets


#function for sending acknowledgemnt 
def send_ack(addr, seq):
    data = struct.pack('!I', seq) # !I = network byte order, unsigned int (4 bytes)
    sock.sendto(data, addr)
    print(f"[Receiver] Sent ACK {seq}")

"""
 So '!I' means:

“Read or write a 4-byte unsigned integer in network (big-endian) order.”
"""


#MAIN RECEIVING LOOP
while True: 
    packet, addr = sock.recvfrom(4096)

    #simulating random packet lossss
    if random.random() < LOSS_PROB:
        print("[Receiver] Simulated packet loss - dropped.")
        continue

    if len(packet) < 4:
        print("[Reciever] Invalid packet -too short.")
        continue

    #extract seq number and payload
    seq = struct.unpack('!I', packet[:4])[0]
    payload = packet[4:].decode(errors='ignore')

    if seq == expected_seq:
        print(f"[Receiver] Received expected packet seq={seq} payload='{payload}' ")

        delivered += 1
        expected_seq += 1

        send_ack(addr, seq)
    else:
        last_inorder = expected_seq -1 if expected_seq > 0 else 0
        print(f"[Receiver] Out-of-order packet seq = {seq}, expected={expected_seq}. Re-ACK {last_inorder}")
        send_ack(addr, last_inorder)

