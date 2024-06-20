import socket
import threading
import time
import argparse
import logging
import uuid


# Broadcast address and port
BROADCAST_ADDR = '192.168.210.255' # Basic broacast address see slides 
PORT = 5002 # Port 5000 + 2 for team 2 
NODE_NAME = socket.gethostname()

received_messages = {}

forwarded_messages = set()

# Set up the socket for broadcasting
def setup_broadcast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# Function to listen for messages
def listen_for_messages(socket):
    while True:
        data, address = socket.recvfrom(1024)
        packet = data.decode('utf-8')
        process_packet(socket, packet)

def process_packet(socket, packet):
    message_id, source, destination, message = packet.split(':', 3)

    if message_id in received_messages:
        return

    received_messages[message_id] = packet
    logging.info(f"Received message: {message} with ID: {message_id} from {source} with destination {destination}")

    if NODE_NAME == destination:
        logging.info(f"Message from {source} reached destination {destination}")
        return

    forward_message(socket, packet)

def forward_message(socket, packet):
    socket.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info("Forwarded message {packet}")


def main():
    broadcast_sock = setup_broadcast_socket()
    listen_sock = setup_broadcast_socket()
    
    # Bind the listening socket to the port
    listen_sock.bind(('', PORT))
    
    # Start broadcasting and listening threads
    threading.Thread(target=listen_for_messages, args=(listen_sock,)).start()

if __name__ == "__main__":
    main()
