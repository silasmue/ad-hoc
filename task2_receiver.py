from asyncio import sleep
import socket
import logging

# With the help of ChatGPT-4o


# Broadcast address and port
BROADCAST_ADDR = '192.168.210.255' # Basic broacast address see slides
PORT = 5002 # Port 5000 + 2 for team 2
NODE_NAME = socket.gethostname()

received_messages = {}


# Set up the socket for broadcasting
def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# Function to listen for messages
def listen_for_messages(sock):
    logging.info(f"Listening on port {PORT}...")
    while True:
        data, address = sock.recvfrom(1024)
        packet = data.decode('utf-8')
        if process_packet(sock, packet):
            return

def process_packet(sock, packet):
    message_type, source, destination, message, route = packet.split(':', 4)

    sleep(0.1)

    if NODE_NAME == destination:
        logging.info(f"Message from {source} reached destination {destination} with route {route}, relayin>")
        origin = route[1:-1].split(':')[0]
        packet = f"R:{NODE_NAME}:{origin}:{message}:[{route[1:-1]}, {NODE_NAME}]"
        sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
        logging.info(f"Sent route to origin. Current route: [{route[1:-1]}, {NODE_NAME}]")
        return True
    if message_type == "D":
        packet = f"D:{NODE_NAME}:{destination}:{message}:[{route[1:-1]}, {NODE_NAME}]"
        sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
        logging.info(f"Forwarded Discovery message {message}. Current route: [{route[1:-1]}, {NODE_NAME}]")
        return True

    if route.find(NODE_NAME) and message_type == "R":
        sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
        logging.info(f"Forwarded Relay message {packet}.")
        return True

    return

def main():
    logging.getLogger().setLevel(logging.INFO)
    listen_sock = setup_socket()

    # Bind the listening socket to the port
    listen_sock.bind(('', PORT))

    logging.info(f"Service started with hostname {NODE_NAME}")
    listen_for_messages(listen_sock)

if __name__ == "__main__":
    main()