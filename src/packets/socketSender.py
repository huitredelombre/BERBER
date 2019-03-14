from scapy.all import Raw
from packets.scapyPacket import ScapyPacket
import socket
class SocketSender(ScapyPacket):

    def __init__(self):
        super().__init__()
        self.sock= socket.socket( socket.AF_PACKET,socket.SOCK_RAW)
        self.sock.bind(('lo',0))
        
    def send(self):
        """send loaded packet"""
        self.sock.send(self.trame.bytes)
        return self.totalSize

    