import configparser


class ConfReader:
    def __init__(self):
        self.path = "conf/configuration.ini"

    def read_udp_conf(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        peer_id = config.get("chat", "peer_id")
        broadcast = config.get("chat", "broadcast")
        udp_port = config.getint("udp", "udp_port")
        return peer_id, broadcast, udp_port

    def read_tcp_conf(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        peer_id = config.get("chat", "peer_id")
        broadcast = config.get("chat", "broadcast")
        tcp_port = config.getint("tcp", "tcp_port")
        return peer_id, broadcast, tcp_port


c = ConfReader()
print(c.read_udp_conf())