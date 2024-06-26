import asyncio
import socket
import logging

# Broadcast address and port
BROADCAST_ADDR = '192.168.210.255'  # Broadcast address for your network
PORT = 5002  # Port for communication
NODE_NAME = socket.gethostname()

received_messages = {}

# Set up the socket for broadcasting
def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# Function to listen for messages
async def listen_for_messages(sock):
    logging.info(f"Listening on port {PORT}...")
    while True:
        data, address = sock.recvfrom(1024)
        packet = data.decode('utf-8')
        process_packet(sock, packet)

# Process received packet
def process_packet(sock, packet):
    message_type, source, destination, message, route = packet.split(':', 4)

    if NODE_NAME == destination:
        logging.info(f"Message from {source} reached destination {destination} with route {route}, relaying")
        origin = route[1:-1].split(':')[0]
        packet = f"R:{NODE_NAME}:{origin}:{message}:[{route[1:-1]}, {NODE_NAME}]"
        sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
        logging.info(f"Sent route to origin. Current route: [{route[1:-1]}, {NODE_NAME}]")

        # Wait for message from sender (assuming sender will send another message)
        data, address = sock.recvfrom(1024)
        packet = data.decode('utf-8')
        process_packet(sock, packet)
    
    elif message_type == "D":
        packet = f"D:{NODE_NAME}:{destination}:{message}:[{route[1:-1]}, {NODE_NAME}]"
        sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
        logging.info(f"Forwarded Discovery message {message}. Current route: [{route[1:-1]}, {NODE_NAME}]")

    elif route.find(NODE_NAME) and message_type == "R":
        sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
        logging.info(f"Forwarded Relay message {packet}.")

def main():
    logging.getLogger().setLevel(logging.INFO)
    sock = setup_socket()
    sock.bind(('', PORT))

    logging.info(f"Service started with hostname {NODE_NAME}")
    asyncio.run(listen_for_messages(sock))

if __name__ == "__main__":
    main()
