import random


class Supervisor_robin:

    def __init__(self, args):
        self.args = args
        self.ber = self.args.ber
        self.byteCount = 0
        self.packetCount = 0
        self.wrongFrameCount = 0
        self.timeTaken = 0

    
    '''
    compute the total percent of wrong frames
    '''
    def computeErrorRate(self):
        return self.wrongFrameCount / self.packetCount * 100
