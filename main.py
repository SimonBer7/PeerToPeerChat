"""
Main Module Documentation

This module initializes and manages the UDP server, UDP client, and TCP handler threads for communication.

Usage:
    1. Run the main() function to start the communication system.
    2. The main() function initializes and starts the UDP server, UDP client, and TCP handler threads.

Example:
    main()

Functions:
    main(): Initializes and manages the UDP server, UDP client, and TCP handler threads.
"""

from src.udp.udp_server import UdpServer
from src.udp.udp_client import UdpClient
from src.tcp.tcp_handler import TCPHandler


def main():
    """
    Initialize and manage the communication system.

    Initializes and starts the UDP server, UDP client, and TCP handler threads.
    """
    udp_server = UdpServer()
    udp_client = UdpClient()
    tcp = TCPHandler(udp_server)

    threads = [udp_server, udp_client, tcp]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
