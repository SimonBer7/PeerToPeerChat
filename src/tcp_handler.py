import threading
import socket
import json
import time
from conf.conf_reader import ConfReader


class TCPHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.peer_id = None
        self.broadcast = None
        self.tcp_port = None
        self.message_history = {}
        self.client_socket = None
        self.set_values()

    def set_values(self):
        config = ConfReader()
        self.peer_id, self.broadcast, self.tcp_port = config.read_tcp_conf()

    def run(self):
        try:
            # Connect to the peer's TCP server
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Send hello message
            hello_message = {"command": "hello", "peer_id": self.peer_id}
            self.send_message(hello_message)

            # Receive handshake response containing message history
            response, addr = self.receive_message()
            self.client_socket.connect(addr)
            if response.get("status") == "ok" and "messages" in response:
                self.message_history = response["messages"]
                print(f"Received message history from {self.peer_id}: {self.message_history}")

            # Start sending new messages to the peer
            #self.send_new_messages()

        except Exception as e:
            print(f"Exception in TCPHandler for {self.peer_id}: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()

    def send_message(self, message):
        self.client_socket.sendall(json.dumps(message).encode("utf-8"))

    def receive_message(self):
        data, addr = self.client_socket.recv(1024)
        return json.loads(data.decode("utf-8")), addr

    def send_new_messages(self):
        while True:
            # Simulating sending new messages
            message = input("Enter your message (or type 'exit' to quit): ")
            if message == "exit":
                break

            # Generate message ID
            message_id = str(int(time.time() * 1000))

            # Prepare new message
            new_message = {"command": "new_message", "message_id": message_id, "message": message}

            # Send the new message
            self.send_message(new_message)

            # Receive acknowledgment
            response = self.receive_message()
            if response.get("status") == "ok":
                print("Message sent successfully")


