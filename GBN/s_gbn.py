import socket
import time
import random
import struct

DEST_IP = "127.0.0.1"
DEST_PORT = 10001
WINDOW_SIZE = 4
TIMOUT = 0.1
LOSS_PROB = 0.1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DEST_IP, DEST_PORT))

messages = [f"Message {i}" for i in range(1, 21)]
base = 0 
next_seq = 0
sent_packets = {}
start_time = None


def make_packet(seq, payload):
    return struct('!I', seq) + payload.encode()


def start_timer():
    global start_time
    start_time = time.time()


def timer_expired():
    if(start_time == None):
        return False
    return (time.time() - start_time) > TIMOUT

print("Starting transmision.....")

while(base< len(messages)):
    while next_seq < base + WINDOW_SIZE and next_seq<len(messages):
        pkt = make_packet(next_seq, messages[next_seq])
        sent_packets[next_seq] = pkt

        if random.random() >= LOSS_PROB:
            sock.sendto(pkt, (DEST_IP, DEST_PORT))
            print("Sender ne bhej dia")
        else:
            print("Simulated loss")

        
        if base == next_seq:
            start_timer()
        
        next_seq += 1


    try:
        data, _ = sock.recvfrom(1024)
        if len(data) >= 4:
            ack_seq = struct.unpack('!I', data[:4])[0]
            print("ack mil gaya")

            base = ack_seq + 1

            if base != next_seq:
                start_timer()
            else:
                start_time = None
    except socket.timeout:
        pass


    if timer_expired():
        print("Timout h gaya")
        for seq in range(base, next_seq):
            pkt = sent_packets[seq]
            if random.random() >= LOSS_PROB:
                sock.sendto(pkt, (DEST_IP, DEST_PORT))
                print("retransjd")
            else:
                print("simulated loss")
        start_timer()

print("All ackd. transd, complet")
sock.close
        