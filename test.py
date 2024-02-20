import socket
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import time

# Global variables
PEER_ID = "simon-peer1"
UDP_PORT = 9876
TCP_PORT = 9876
HTTP_PORT = 8000
MESSAGE_HISTORY_SIZE = 100
MESSAGE_TIMEOUT = 30  # seconds
peers = set()
message_history = {}


class UDPDiscoveryThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('0.0.0.0', UDP_PORT))
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while True:
            data, addr = udp_socket.recvfrom(1024)
            message = json.loads(data.decode())
            if message.get('command') == 'hello' and message.get('peer_id') != PEER_ID:
                peer_id = message.get('peer_id')
                peers.add((peer_id, addr[0]))
                # Send response
                response = {'status': 'ok', 'peer_id': PEER_ID}
                udp_socket.sendto(json.dumps(response).encode(), addr)


class TCPMessageHandler(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address

    def run(self):
        with self.connection:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                self.handle_message(message)

    def handle_message(self, message):
        command = message.get('command')
        if command == 'hello':
            self.handle_hello(message)
        elif command == 'new_message':
            self.handle_new_message(message)

    def handle_hello(self, message):
        peer_id = message.get('peer_id')
        if peer_id != PEER_ID:
            peers.add((peer_id, self.address[0]))
            # Send message history
            response = {'status': 'ok', 'messages': message_history}
            self.connection.sendall(json.dumps(response).encode())

    def handle_new_message(self, message):
        message_id = message.get('message_id')
        message_text = message.get('message')
        if message_id not in message_history:
            message_history[message_id] = {'peer_id': PEER_ID, 'message': message_text}
            self.broadcast_message(message)

    def broadcast_message(self, message):
        for peer in peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((peer[1], TCP_PORT))
                    s.sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"Error broadcasting message to {peer}: {e}")


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == '/messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(message_history).encode())
        elif parsed_path.path == '/send':
            message = query_params.get('message', [''])[0]
            if message:
                message_id = str(int(time.time() * 1000))  # milliseconds since epoch
                new_message = {'command': 'new_message', 'message_id': message_id, 'message': message}
                for peer in peers:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((peer[1], TCP_PORT))
                            s.sendall(json.dumps(new_message).encode())
                    except Exception as e:
                        print(f"Error sending message to {peer}: {e}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def main():
    udp_thread = UDPDiscoveryThread()
    udp_thread.start()

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind(('0.0.0.0', TCP_PORT))
    tcp_server.listen(5)

    http_server = HTTPServer(('0.0.0.0', HTTP_PORT), HTTPRequestHandler)
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.daemon = True
    http_thread.start()

    while True:
        conn, addr = tcp_server.accept()
        tcp_handler = TCPMessageHandler(conn, addr)
        tcp_handler.start()


if __name__ == "__main__":
    main()
