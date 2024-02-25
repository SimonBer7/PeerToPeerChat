"""
UDP Server Module Documentation

This module implements a UDP server that listens for messages from peers on a specified port.
It allows peers to send "hello" messages to announce themselves and respond to those messages with an acknowledgment.
The server runs in a separate thread to handle incoming messages concurrently.

Usage:
    1. Instantiate the UdpServer class.
    2. Call the start() method to start the server.

Attributes:
    peer_id (str): The identifier of the current peer.
    udp_port (int): The port on which the server listens for UDP messages.
    broadcast (str): The broadcast address used for communication.
    peers (set): A set containing tuples of (peer_id, (ip, port)) representing connected peers.

Methods:
    get_peers(): Returns the set of connected peers.
    set_values(): Reads configuration values (peer_id, udp_port, broadcast) from a configuration file.
    run(): Overrides the run method of the threading.Thread class to start the server.
"""

import socket
import json
import threading
from conf.conf_reader import ConfReader

class UdpServer(threading.Thread):
    def __init__(self):
        """
        Initialize the UDP server.

        Initializes attributes and reads configuration values.
        """
        threading.Thread.__init__(self)
        self.peer_id = None
        self.udp_port = None
        self.broadcast = None
        self.peers = set()
        self.set_values()

    def get_peers(self):
        """
        Get the set of connected peers.

        Returns:
            set: A set containing tuples of (peer_id, (ip, port)).
        """
        return self.peers

    def set_values(self):
        """
        Set configuration values.

        Reads configuration values (peer_id, udp_port, broadcast) from a configuration file.
        """
        config = ConfReader()
        self.peer_id, self.broadcast, self.udp_port = config.read_udp_conf()

    def run(self):
        """
        Run the UDP server.

        Listens for incoming messages from peers and processes them accordingly.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", self.udp_port))
            while True:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode("utf-8"))
                if 'command' in message:
                    if message['command'] == 'hello' and message['peer_id'] != self.peer_id:
                        print(f"Received 'hello' from {message['peer_id']}")
                        self.peers.add((message["peer_id"], addr))
                        ok_message = {'status': 'ok', 'peer_id': self.peer_id}
                        sock.sendto(json.dumps(ok_message).encode("utf-8"), addr)
                elif 'status' in message:
                    if message['status'] == 'ok' and message['peer_id'] != self.peer_id:
                        print(f"Received ok from {message['peer_id']}")
                else:
                    print(f"Unsupported message from {message['peer_id']}")

        except ValueError as ve:
            print(f"ValueError in udp_server: {ve}")
        except Exception as e:
            print(f"Exception in udp_server: {e}")
