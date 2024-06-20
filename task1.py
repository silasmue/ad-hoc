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
        process_packet(sock, packet)

def process_packet(sock, packet):
    message_id, source, destination, message = packet.split(':', 3)

    if message_id in received_messages:
        return

    received_messages[message_id] = packet
    logging.info(f"Received message: {message} with ID: {message_id} from {source} with destination {destination}")

    if NODE_NAME == destination:
        logging.info(f"Message from {source} reached destination {destination}")
        return

    forward_message(sock, packet)

def forward_message(sock, packet):
    sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info(f"Forwarded message {packet}")


def main():
    logging.getLogger().setLevel(logging.INFO)
    listen_sock = setup_socket()
    
    # Bind the listening socket to the port
    listen_sock.bind(('', PORT))
     
    logging.info(f"Service started with hostname {NODE_NAME}")
    listen_for_messages(listen_sock)

if __name__ == "__main__":
    main()
