from typing import Union

from Devices.Devices import _Device
from Devices.DigitialFilter import DigitFilter
from Simulation_Content.Signals import Signals
from Simulation_Content.Simulation import FSample
from Tools.Filter import Filters
from AM.Amplitude_Demodulator import Demodulator
from Tools.Mixer import Mixer


class AMReceiver(_Device):
    """To receive signal with amplitude modulation, uses AM_Demodulator,

        -Need power to work

    """

    def __init__(self, Carrier: Signals, Power: Signals):
        """
        :param Carrier: Carrier wave, needed to demodulation (Synchronous)
        :type Carrier: Signals
        :param Power: AC needed
        :type Power: Signals
        """
        super().__init__()
        self._Carrier = Carrier

        # Power verification
        self._VACNeeded = Power
        self._VDCNeeded = Power.RMSValue
        if not Power == self._VACNeeded:
            raise Exception("Voltage too low")

        self._LowPassFilter = Filters("fft") # Filter needed for demodulation
        self._HighPassFiler = Filters("HpFft", FC=1, FS=FSample) # Filter needed for treatment
        self._demodulated : Union[Signals,None]= None

    @staticmethod
    def _Norm(Signal: Signals) -> Signals:
        """
        Norm signal, id : linear compression of  amplitude to have vmax = 1V, Vmax = -1
        :param Signal: Signal that we want to Norm
        :type Signal: Signals
        :return: Normed signal
        :rtype: Signals
        """
        return Mixer().Norm(Signal)

    @property
    def Demodulated(self) -> Signals:
        """
        Get signal demodulated
        :return: Demodulated Signal
        :rtype: Signals
        """
        if not self._demodulated:
            raise Exception("Please demoduled before")
        return self._demodulated

    def Demodulate(self, Wave: Signals, FC: float = 10000, Fs: float = FSample) -> None:
        """
        Main method, demodulate the signal
        :rtype: None
        :param Wave: Signal that we want to demodulate, thus has to be modulate
        :type Wave: Signals
        :param FC: cutoff frequency of low pass filter (defaut fc= 10000Hz), f_content<<fc<<f_carrier
        :type FC: float
        :param Fs: Sampling frequency, has to be the same as time step (default = FSample)
        :type Fs: float
        """
        demodulator = Demodulator(self._Carrier, Wave)  # Init Demodulator
        # Setup filter
        self._LowPassFilter.FC = FC
        self._LowPassFilter.FS = Fs
        self._demodulated = demodulator.Run(self._LowPassFilter) # get demodulated signal

    def TreatSignal(self, FC: float = 5, FS: float = FSample) -> None:
        """

        :rtype: None
        :param FC: cutoff frequency of high pass filter, has to be smaller has possible to reduce offset due to modulation
        :type FC: float
        :param FS: Sampling frequency, has to be the same as time step (default = FSample)
        :type FS: float
        """
        if not self._demodulated:
            raise Exception("Please demodulate before")
        else:
            # Setup filter
            self._HighPassFiler.FC = FC
            self._HighPassFiler.FS = FS
            self._demodulated = self._Norm(DigitFilter().HighPass(Signal=self._demodulated,
                                                                  frequence=self._HighPassFiler.FC,
                                                                  fSample=self._HighPassFiler.FS))
