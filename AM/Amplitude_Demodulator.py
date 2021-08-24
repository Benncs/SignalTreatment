from typing import Union

import numpy as np

from Components.Diode import  Multiplier
from Tools.Filter import Filters
from Devices.DigitialFilter import *


class Demodulator:
    """
    To demodulation an signal modulated with AM protocol
    """
    def __init__(self, Carrier: Signals, ToDemodulate: Signals) :
        """
        :param Carrier: Carrier Wave used for demodulation
        :type Carrier: Signals
        :param ToDemodulate: Signal that has to be demodulated
        :type Demodulator: Signals
        """
        self._Signal = ToDemodulate
        self._Carrier = Carrier
        self._ToBeFiltered: Union[Signals,None] = None

    def Run(self, filt: Filters)-> Signals:
        """
        class' main method


        :param filt: Low pass filter used for demodulation
        :type filt: Filters
        :rtype: Signals
        """
        self._SignalTreatments()
        # Demodulation with a digital low pass filter
        if filt.NAME == 'fft':
            Demodulated = DigitFilter(self._ToBeFiltered).LowPass(cutoff=filt.FC, fSample=filt.FS)
        elif filt.NAME =='fftbp':
            Demodulated = DigitFilter(self._ToBeFiltered).BandPas(fc1=filt.FC,fc2=filt.FC2, fSample=filt.FS)
        else:
            return Signals(np.zeros(0))

        return Demodulated #self._Diode(Demodulated)

    def _SignalTreatments(self) -> None:
        """"Synchronous AM Detector, works in place"""
        self._ToBeFiltered = Multiplier().Apply(self._Signal,self._Carrier)

    @staticmethod
    def _Diode(Signal: Signals) -> Signals:
        """"Apply a diode to a signal  """
        from Components.Diode import Diode
        return Diode().Run(Signal)
