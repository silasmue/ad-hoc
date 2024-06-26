                                                                                           
import socket
import uuid
import logging

BROADCAST_ADDR = '192.168.210.255'
PORT = 5002
NODE_NAME = socket.gethostname()

routes = {}

logging.basicConfig(filename=f'{NODE_NAME}.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

UUID = str(uuid.uuid4())

def setup_broadcast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def setup_receive_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))
    return sock

def broadcast_discovery_message(sock, message, message_id, destination):
    packet = f"D:{NODE_NAME}:{destination}:{message}:[{NODE_NAME}]"
    sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info(f"Broadcasting D message: {packet}")

def broadcast_relay_message(sock, message, message_id, destination, route):
    packet = f"R:{NODE_NAME}:{destination}:{message}:[{', '.join(route)}]"
    sock.sendto(packet.encode('utf-8'), (BROADCAST_ADDR, PORT))
    logging.info(f"Broadcasting R message: {packet}")

def listen_for_messages(sock):
    logging.info(f"Listening on port {PORT}...")
    while True:
        data, address = sock.recvfrom(1024)
        packet = data.decode('utf-8')
        if process_packet(packet):
            return packet

def process_packet(packet):
    packet_type, source, destination, message, route = packet.split(':', 4)
    route = route.strip('[]').split(',')
    
    if destination == NODE_NAME:
        logging.info(f"Route {route} received for destination {source}")
        routes[source] = route[::-1]
        return True
    return False

def main():
    global routes
    message = input("Enter message: ")
    dest = input("Enter destination: ")
    
    if dest in routes:
        print(f"Route already exists, sending using route")
        socket = setup_broadcast_socket()
        broadcast_relay_message(socket, message, UUID, dest, routes[dest])
    else:
        socket = setup_broadcast_socket()
        broadcast_discovery_message(socket, message, UUID, dest)
        socket = setup_receive_socket()
        route_packet = listen_for_messages(socket)

        if route_packet:
            process_packet(route_packet)
            if dest in routes:
                broadcast_relay_message(socket, message, UUID, dest, routes[dest])
            else:
                print(f"Route to {dest} not found after discovery.")
                logging.info(f"Route to {dest} not found after discovery.")
        else:
            print(f"No route information received for {dest}.")
            logging.info(f"No route information received for {dest}.")

if __name__ == "__main__":
    while True:
        main()
