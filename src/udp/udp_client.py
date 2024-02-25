"""
UDP Client Module Documentation

This module implements a UDP client that sends "hello" messages to peers at regular intervals.
It runs in a separate thread to allow concurrent execution with other parts of the program.

Usage:
    1. Instantiate the UdpClient class.
    2. Call the start() method to start the client.

Attributes:
    peer_id (str): The identifier of the current peer.
    udp_port (int): The port on which the client sends UDP messages.
    broadcast (str): The broadcast address used for communication.

Methods:
    set_values(): Reads configuration values (peer_id, udp_port, broadcast) from a configuration file.
    run(): Overrides the run method of the threading.Thread class to start the client and send "hello" messages at regular intervals.
"""

import socket
import json
import threading
import time
from conf.conf_reader import ConfReader

class UdpClient(threading.Thread):
    def __init__(self):
        """
        Initialize the UDP client.

        Initializes attributes and reads configuration values.
        """
        threading.Thread.__init__(self)
        self.peer_id = None
        self.broadcast = None
        self.udp_port = None
        self.set_values()

    def set_values(self):
        """
        Set configuration values.

        Reads configuration values (peer_id, udp_port, broadcast) from a configuration file.
        """
        config = ConfReader()
        self.peer_id, self.broadcast, self.udp_port = config.read_udp_conf()

    def run(self):
        """
        Run the UDP client.

        Sends "hello" messages to peers at regular intervals.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            hello_message = {"command": "hello", "peer_id": self.peer_id}
            while True:
                sock.sendto(json.dumps(hello_message).encode("utf-8"), (self.broadcast, self.udp_port))
                print(f"Sent 'hello' from {self.peer_id}")
                time.sleep(5)
        except Exception as e:
            print(f"Exception in udp_client: {e}")
