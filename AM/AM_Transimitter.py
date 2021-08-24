from typing import Union

import numpy as np

from AM.Amplitude_Modulator import Modulator
from Colpitts_Oscillator import ColpittsOscillator
from Devices.Devices import _Device
from Simulation_Content.Signals import Signals


class AMTransmitter(_Device):
    """To emit signal with amplitude modulation, uses AM_Modulator,

    -Need power to work

    -Generate a Carrier Wave """

    def __init__(self, Power: Signals):
        super().__init__()

        # Check power needed
        self._VACNeeded = Power
        self._VDCNeeded = Power.RMSValue
        if not Power == self._VACNeeded:
            raise Exception("Voltage too low")

        self._Carrier: Signals = ColpittsOscillator(self._VDCNeeded / 10e3).Run()
        self._Modulator: Modulator = Modulator(self._Carrier) # Init modulator
        self._Mod: Union[Signals, None] = None

    def Send(self, Content: Signals) -> Signals:
        """Send Wave that is to say modulate a content
        :param Content: Message to send (to modulate)
        :type Content: Signals
        :return: Modulated Signal
        :rtype: Signals
        """
        self._Mod = self._Modulator.Run(Content)
        return self._Mod

    @property
    def Carrier(self) -> Signals:
        """" Get Carrier Property

            :return: Carrier Wave use to emit signal
            :rtype: Signals"""
        return self._Carrier
