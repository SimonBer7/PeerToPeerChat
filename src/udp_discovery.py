import socket
import json
import threading
from conf.conf_reader import ConfReader
import time


class UdpDiscovery(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.peers = set()
        self.udp_port = None
        self.peer_id = None
        self.broadcast = None
        self.set_values()
        self.hello_message = {"command": "hello", "peer_id": self.peer_id}
        self.ok_message = {'status': 'ok', 'peer_id': self.peer_id}

    def get_peers(self):
        return self.peers

    def set_values(self):
        config = ConfReader()
        self.peer_id, self.broadcast, self.udp_port = config.read_udp_conf()

    def run_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", self.udp_port))

            while True:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode("utf-8"))
                print(message)
                if message is None:
                    raise ValueError()
                else:
                    if message['command'] == 'hello' and message['peer_id'] != self.peer_id:
                        print(f"Received 'hello' from {message['peer_id']}")
                        self.peers.add((message["peer_id"], addr[0]))
                        sock.sendto(json.dumps(self.ok_message).encode("utf-8"), addr)
        except ValueError as ve:
            print(f"ValueError in udp_server: {ve}")
        except Exception as e:
            print(f"Exception in udp_server: {e}")

    def run_client(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                sock.sendto(json.dumps(self.hello_message).encode("utf-8"), (self.broadcast, self.udp_port))
                print(f"Sent 'hello' from {self.peer_id}")
                time.sleep(5)
        except Exception as e:
            print(f"Exception in udp_client: {e}")

    def run(self):
        try:
            udp_server = UdpDiscovery()
            udp_client = UdpDiscovery()

            threading.Thread(target=udp_server.run_server).start()
            threading.Thread(target=udp_client.run_client).start()
        except Exception as e:
            print(f"Exception in starting servers: {e}")






