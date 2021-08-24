import warnings

import numpy as np

from Simulation_Content.Signals import Signals
from Components.Diode import Multiplier, SummingAmplifier


class Modulator:
    """
        To modulation an signal modulated with AM protocol
        """

    def __init__(self, Carrier: Signals):
        """

        :param Carrier: Carrier Wave used for modulation : xp(t)
        :type Carrier: Signals
        """
        self._Carrier:Signals = Carrier
        self._k = 1  # Modulation factor
        self._Mult = Multiplier()
        self._Add = SummingAmplifier()

    def Run(self, Content: Signals) -> Signals:
        """
        Class' main method

        :param Content: Content to modulate : xm(t)
        :type Content: Signals
        :return: Modulated signal
        :rtype: Signals
        """
        # h = self._k * self.MaxWave(Message)
        if Content.len != self._Carrier.len:
            raise Exception("Message must be the same length as carrier")

        # Modulation formula : y(t) = xp(t)+k*xp(t)*xm(t)

        Res = self._Mult.Apply(self._Carrier, Content)
        Res = self._Mult.Apply(self._k, Res)
        Res = self._Add.Apply(self._Carrier, Res)
        self._OverModulationCheck(Res)
        return Res

    @property
    def Carrier(self) -> Signals:
        """" Get Carrier Property
            :return: Carrier wave for modulation
            :rtype: Signals"""
        return self._Carrier

    @Carrier.setter
    def Carrier(self, NewCarrier: Signals)-> None:
        """
        :param NewCarrier: To change carrier wave
        :type NewCarrier: Signals
        """
        self._Carrier = NewCarrier

    def _OverModulationCheck(self, Signal: Signals):
        """"
        To detect if signal is overmodulated
        """
        Max = Signal.Max
        MaxCarrier = self._Carrier.Max
        if Max > 2 * MaxCarrier:  # Amplitude of modulated signals has to be less than 200% than the carrier's one
            warnings.warn("OverModulation")
