import socket
import threading
import time

# Broadcast address and port
BROADCAST_ADDR = '192.168.210.255' # Basic broacast address see slides 
PORT = 5002 # Port 5000 + 2 for team 2 
MESSAGE = "Hello World"

# Set up the socket for broadcasting
def setup_broadcast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# Function to broadcast message
def broadcast_message(sock, message):
    while True:
        sock.sendto(message.encode('utf-8'), (BROADCAST_ADDR, PORT))
        print(f"Broadcasting message: {message}")
        time.sleep(5)  # Broadcast every 5 seconds

# Function to listen for messages
def listen_for_messages(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data.decode('utf-8')} from {addr}")

def main():
    broadcast_sock = setup_broadcast_socket()
    listen_sock = setup_broadcast_socket()
    
    # Bind the listening socket to the port
    listen_sock.bind(('', PORT))
    
    # Start broadcasting and listening threads
    threading.Thread(target=broadcast_message, args=(broadcast_sock, MESSAGE)).start()
    threading.Thread(target=listen_for_messages, args=(listen_sock,)).start()

if __name__ == "__main__":
    main()
