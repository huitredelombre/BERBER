import random
from supervisors.supervisor import Supervisor


class BitWiseSupervisor(Supervisor):

    '''
    Create and use a PacketSender to launch packet and actually computes statistics
    '''

    def realSend(self):
        #self.numberOfPacket += 1
        while True:
            erroned = self.applyBER()
            self.senderSend()
            if not erroned:
                break
            self.packetFailure += 1
            self.sender.resetTrame()
    '''
    Invert all bits of the frame to send, with a probability corresponding to BER
    '''

    def applyBER(self):
        for i in range(self.sender.getSize()):
            randFloat = random.uniform(0, 1)
            if randFloat < self.BER:
                self.sender.flipBit(i)
        return self.sender.checkIfErronned()
