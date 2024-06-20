import socket
import uuid
import logging
import argparse

# With the help of ChatGPT-4o

parser = argparse.ArgumentParser(description='Ad-hoc network flooding client')
parser.add_argument('--message', type=str, required=True, help='Message to broadcast via flooding')
parser.add_argument('--destination', type=str, required=True, help='Destination for the message to send')
args = parser.parse_args()

BROADCAST_ADDR = '192.168.210.255'
PORT = 5002
MESSAGE = args.message
NODE_NAME = socket.gethostname()
DESTINATION = args.destination

logging.basicConfig(filename=f'{NODE_NAME}.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

UUID = str(uuid.uuid4())

def setup_broadcast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# Function to broadcast message
def broadcast_message(sock, message, message_id, destination):
    packet = f"{message_id}:{NODE_NAME}:{destination}:{message}"
    sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info(f"Broadcasting message: {packet}")

def main():
    socket = setup_broadcast_socket()
    broadcast_message(socket, MESSAGE, UUID, DESTINATION)

if __name__ == "__main__":
    main()
