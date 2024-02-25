"""
TCP Handler Module Documentation

This module implements a TCP handler that connects to peers obtained from a UDP server,
exchanges messages, and manages message history.

Usage:
    1. Instantiate the TCPHandler class with a reference to the UDP server.
    2. Call the start() method to start the TCP handler.

Attributes:
    peer_id (str): The identifier of the current peer.
    broadcast (str): The broadcast address used for communication.
    tcp_port (int): The port on which the TCP handler listens for incoming connections.
    message_history (dict): A dictionary containing message history.
    client_socket (socket.socket): The TCP socket for communication with a peer.
    peers (set): A set containing tuples of (peer_id, (ip, port)) representing connected peers.
    peers_with_sock (set): A set containing tuples of (peer_id, (ip, port), socket) representing connected peers with their socket objects.
    udp (UdpServer): The UDP server instance for obtaining peers.

Methods:
    get_messages(): Returns the message history.
    set_values(): Reads configuration values (peer_id, broadcast, tcp_port) from a configuration file.
    run(): Overrides the run method of the threading.Thread class to start the TCP handler and manage connections with peers.
    save_messages(): Saves the message history to a file.
    send_message(message): Sends a message to a connected peer.
    receive_message(): Receives a message from a connected peer.
    merge_message_history(new_messages): Merges new messages into the message history.
"""

import socket
import json
import threading
from conf.conf_reader import ConfReader


class TCPHandler(threading.Thread):
    def __init__(self, udp):
        """
        Initialize the TCP Handler.

        Initializes attributes and reads configuration values.

        Args:
            udp (UdpServer): An instance of the UDP server for obtaining peers.
        """
        threading.Thread.__init__(self)
        self.peer_id = None
        self.broadcast = None
        self.tcp_port = None
        self.message_history = {}
        self.client_socket = None
        self.set_values()
        self.peers = None
        self.peers_with_sock = set()
        self.udp = udp

    def get_messages(self):
        """
        Get the message history.

        Returns:
            dict: A dictionary containing message history.
        """
        return self.message_history

    def set_values(self):
        """
        Set configuration values.

        Reads configuration values (peer_id, broadcast, tcp_port) from a configuration file.
        """
        config = ConfReader()
        self.peer_id, self.broadcast, self.tcp_port = config.read_tcp_conf()

    def run(self):
        """
        Run the TCP Handler.

        Connects to peers obtained from the UDP server, exchanges messages,
        and manages message history.
        """
        try:
            running = True
            while running:
                self.peers = self.udp.get_peers()
                if len(self.peers) == 0:
                    continue
                else:
                    print(self.peers)
                    for peer in self.peers:
                        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.client_socket.settimeout(5)
                        self.client_socket.connect(peer[1])
                        hello_message = {"command": "hello", "peer_id": self.peer_id}
                        self.send_message(hello_message)
                        response = self.receive_message()
                        print(f"Received message history from {peer[0]}: {response}")
                        if response.get("status") == "ok":
                            self.message_history = response
                            self.save_messages()
                            self.peers_with_sock.add((peer[0], peer[1], self.client_socket))
                            running = False
                            break
        except Exception as e:
            print(f"Exception in TCPHandler for {self.peer_id}: {e}")

    def save_messages(self):
        """
        Save the message history to a file.
        """
        try:
            with open("messages/messages.txt", 'w') as file:
                json.dump(self.message_history, file, indent=4)
            print("Data saved successfully to messages.txt")
        except Exception as e:
            print("Error saving data to file:", e)

    def send_message(self, message):
        """
        Send a message to a connected peer.

        Args:
            message (dict): The message to send.
        """
        self.client_socket.sendall(json.dumps(message).encode("utf-8"))

    def receive_message(self):
        """
        Receive a message from a connected peer.

        Returns:
            dict: The received message.
        """
        data = self.client_socket.recv(100000)
        return json.loads(data.decode("utf-8"))

    def merge_message_history(self, new_messages):
        """
        Merge new messages into the message history.

        Args:
            new_messages (dict): Dictionary containing new messages to merge.
        """
        for message_id, message_content in new_messages.items():
            if message_id not in self.message_history:
                self.message_history[message_id] = message_content
