from scapy.all import Raw, Ether, IP, UDP, sendp
from packets.packet import Packet
from bitstring import BitArray
import crcmod
import sys

sysorder=sys.byteorder
class ScapyPacket(Packet):

    def __init__(self):

        # sizes in bytes
        '''
            self.ETHERNET_HEADER_SIZE = 14
            self.IP_HEADER_SIZE = 20
            self.UDP_HEADER_SIZE = 8
            self.HEADER_SIZE = self.ETHERNET_HEADER_SIZE + \
                self.IP_HEADER_SIZE + self.UDP_HEADER_SIZE


            self.payloadSize = len(payload)
            self.checksumSize = 4
            '''
        self.IP_DST_ADDRESS = "127.0.0.1"
        self.UDP_PORT = 12349
        self.baseTrame = Ether() / IP(dst=self.IP_DST_ADDRESS) / \
            UDP(sport=self.UDP_PORT, dport=self.UDP_PORT + 1)

        self.crc32_func = crcmod.mkCrcFun(
            0x104c11db7,
            initCrc=0,
            xorOut=0xFFFFFFFF)  # preparing checksum computation
        self.flippedBit=[]

    def send(self):
        """send loaded packet"""
        sendp(Raw(self.trame.bytes), verbose=0, iface='lo')
        return self.totalSize

    def sendErroned(self):
        # TODO test it instead of printing it
        # print ('before\n', bits.bytes )
        self.flipBit(int(self.totalSize / 2))
        # print( 'after\n',bits.bytes)
        sendp(Raw(self.trame.bytes), verbose=0, iface='lo')

# sendErronned is not supposed to alter target payload. to ecnonomise the
# copy we just flip back altered bits at the end
        self.flipBit(int(self.totalSize / 2))
        return self.totalSize

    def setPayload(self, payload):
        self.flippedBit=[]
        self.payloadSize = len(payload)
        payload = Raw(load=payload)
        self.trame = BitArray(  # translate the whole trame to binary
            bytes(
                self.baseTrame /
                payload
            )
        )
        self.computeTotalSize()
        self.initialCheckSum = self.getFCS()

#        print ("before check:",self.trame, "check=", self.initialCheckSum)
        self.trame.append(BitArray(self.initialCheckSum.to_bytes(4, sysorder)))
#       print ("after check:",self.trame)
        return self.initialCheckSum

    def getFCS(self):
        #compute checksum, ignoring cut last bytes
        currentCheksum = self.crc32_func(self.trame.bytes)
        return currentCheksum

    def computeTotalSize(self):
        self.totalSize = len(self.trame.bytes)

    def getSize(self):
        return self.totalSize

    def flipBit(self, position):
        self.flippedBit.append(position)
        self.trame.invert(position)


#needed for bitwise stuff section

    def unflip(self):
        """reset the frame to match the initial one"""
        for i in self.flippedBit:
            self.trame.invert(i)
        self.flippedBit=[]

    def checkIfErronned(self):
        """return true if the current frame checksum match the initial one"""
        currentCheksum = self.crc32_func(self.trame.bytes[:-4])#ignoring initialchecksum
        return (currentCheksum != self.initialCheckSum)
