from src.udp_discovery import UdpDiscovery
from src.tcp_handler import TCPHandler

def main():
    udp = UdpDiscovery()
    udp.start()
    tcp = TCPHandler()
    tcp.start()


if __name__ == "__main__":
    main()
