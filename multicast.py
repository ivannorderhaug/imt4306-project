import socket
import struct

"""
    Multicast class to send and receive messages
"""
class Multicast:
    def __init__(self, group, port):
        self.group = group
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) # time to live
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0) # 0 = no loopback, 1 = loopback
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        mreq = struct.pack('4sl', socket.inet_aton(group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # join the multicast group

    def send_message(self, message):
        if isinstance(message, str):
            message = message.encode()
        self.sock.sendto(message, (self.group, self.port))

    def receive_message(self):
        data, address = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        return data.decode(), address
    
    def close(self):
        self.sock.close()