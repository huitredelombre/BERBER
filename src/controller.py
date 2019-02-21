#!/usr/bin/python3
from supervisor_robin import Supervisor_robin
from simulations.noPacket import NoPacketSimulation
from simulations.randomSeriesSimulation import RandomSeriesSimulation
from simulations.sendTrueFile import TrueFileSimulation
import time


class Controller:

    def __init__(self, args):
        self.args = args
        self.supervisor = Supervisor_robin(args)
        if (args.simulated):
            self.simulation = NoPacketSimulation(self.supervisor, args)
        else:
            if (args.random):
                self.simulation = RandomSeriesSimulation(self.supervisor)
            else:
                self.simulation = TrueFileSimulation(self.supervisor, args)

    def run(self):
        self.simulation.preRun()
        self.simulation.run()
        self.simulation.terminate()
