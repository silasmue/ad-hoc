from asyncio import sleep
import socket
import uuid
import logging
import argparse

BROADCAST_ADDR = '192.168.210.255'
PORT = 5002
message = ""
NODE_NAME = socket.gethostname()
dest = ""

routes = dict

logging.basicConfig(filename=f'{NODE_NAME}.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

UUID = str(uuid.uuid4())

def setup_broadcast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def setup_recieve_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# Function to broadcast message with intent to discover
def broadcast_discovery_message(sock, message, message_id, destination):
    packet = f"D:{NODE_NAME}:{destination}:{message}:[{NODE_NAME}]"
    sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info(f"Broadcasting D message: {packet}")

# Function to broadcast message with intent to relay
def broadcast_relay_message(sock, message, message_id, destination):
    packet = f"R:{NODE_NAME}:{destination}:{message}:[{NODE_NAME}]"
    sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info(f"Broadcasting R message: {packet}")

# Function to listen for messages
def listen_for_messages(sock):
    logging.info(f"Listening on port {PORT}...")
    while True:
        data, address = sock.recvfrom(1024)
        packet = data.decode('utf-8')
        if process_packet(sock, packet):
            return

def process_packet(sock, packet):
    type, source, destination, message, route = packet.split(':', 4)

    if destination == NODE_NAME:
        logging.info(f"Route {route} recived for destination {source}")

        routes[dest] = route[::-1]
        return True

    return False


def main():
    message = input("enter message: ")
    dest = input("enter dest: ")
    socket = setup_broadcast_socket()

    if routes[dest] == None:
        print(f"Route already exists, sending using route")
        broadcast_relay_message(socket, message, UUID, dest)
        return

    broadcast_discovery_message(socket, message, UUID, dest)

    socket = setup_recieve_socket()
    socket.bind(('', PORT))

    listen_for_messages(socket)


if __name__ == "__main__":
    while True:
        main()