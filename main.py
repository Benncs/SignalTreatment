from random import Random

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft

from Board import Board
from Simulation_Content.Simulation import *
from Simulation_Content.Signals import Signals
from Plug import Plug


class Message(Signals):
    """
    Object that represent message to send with AM transceiver,
    Inherited from Signals
    """

    def __init__(self):
        _freq = 100000
        _freq2 = 50000
        _amp1 = 1
        _amp2 = 0.5
        _Wave: np.ndarray = _amp1 * np.cos(_freq * 2 * np.pi * Time.Value)
        _Wave2: np.ndarray = _amp2 * np.cos(_freq2 * 2 * np.pi * Time.Value)
        _FinalWave: np.ndarray = _Wave + _Wave2
        for i in range(10):
            _FinalWave +=  Random().random()* np.cos(60000*(1+Random().random())*Time.Value*2*np.pi)
        super(Message, self).__init__(_FinalWave)


if __name__ == '__main__':
    """Simulation for signal treatment"""

    # Init Board
    Power = Plug()
    DevicesWanted = ['Scope', "Spectrum", 'Generator', 'Mixer', "AMTransceiver"]
    board = Board(Power, *DevicesWanted)
    Scope = board.Scope
    Transceiver = board.Transceiver
    Mixer = board.Mixer
    Generator = board.Generator

    board.Power = 5

    # Message To     Emit
    ToSend = Mixer.Norm(Message())

    Transceiver.Send(ToSend)

    Transceiver.Demodulate(FC=150000)
    Transceiver.TreatSignal()

    Scope.Show(ToSend, color='r')
    Scope.Show(Transceiver.Demodulated, end=True)

