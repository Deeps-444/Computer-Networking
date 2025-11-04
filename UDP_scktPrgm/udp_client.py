import socket
#create udp socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#serveer address
server_address = ('127.0.0.10', 12345)

#send message
message = "Hello from UDP client!"
client_socket.sendto(message.encode(), server_address);

#receive reply
data, addr = client_socket.recvfrom(1024)
print("Server replied: ", data.decode())

client_socket.close()