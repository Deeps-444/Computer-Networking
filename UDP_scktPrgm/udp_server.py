import socket

#create udp socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
""" 
creates new socket object
AF_INET: means we r using IPv4 
SOCK_DGRAM: udp (datagram based)
"""

#bind to local address and port
server_socket.bind(('127.0.0.10', 12345))
print("UDP server listening on port 12345")

while True:
    data, addr = server_socket.recvfrom(1024)
    #1024 bytes:max data to receive
    print(f"Received from {addr}: {data.decode()}")

    server_socket.sendto(b"message received!", addr) #bytes message 
    
