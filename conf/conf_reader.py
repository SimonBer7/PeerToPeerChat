"""
Configuration Reader Module Documentation

This module provides functionality to read configuration values from a configuration file.

Usage:
    1. Instantiate the ConfReader class.
    2. Call the appropriate method to read UDP or TCP configuration values.

Attributes:
    path (str): The path to the configuration file.

Methods:
    read_udp_conf(): Reads UDP configuration values from the configuration file and returns them as a tuple (peer_id, broadcast, udp_port).
    read_tcp_conf(): Reads TCP configuration values from the configuration file and returns them as a tuple (peer_id, broadcast, tcp_port).
"""

import configparser


class ConfReader:
    def __init__(self):
        """
        Initialize the Configuration Reader.

        Sets the path to the configuration file.
        """
        self.path = "conf/configuration.ini"

    def read_udp_conf(self):
        """
        Read UDP configuration values.

        Returns:
            tuple: A tuple containing UDP configuration values (peer_id, broadcast, udp_port).
        """
        config = configparser.ConfigParser()
        config.read(self.path)
        peer_id = config.get("chat", "peer_id")
        broadcast = config.get("chat", "broadcast")
        udp_port = config.getint("udp", "udp_port")
        return peer_id, broadcast, udp_port

    def read_tcp_conf(self):
        """
        Read TCP configuration values.

        Returns:
            tuple: A tuple containing TCP configuration values (peer_id, broadcast, tcp_port).
        """
        config = configparser.ConfigParser()
        config.read(self.path)
        peer_id = config.get("chat", "peer_id")
        broadcast = config.get("chat", "broadcast")
        tcp_port = config.getint("tcp", "tcp_port")
        return peer_id, broadcast, tcp_port

