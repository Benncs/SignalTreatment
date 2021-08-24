from typing import Union

from AM.AM_Receiver import AMReceiver
from AM.AM_Transimitter import AMTransmitter
from Simulation_Content.Signals import Signals
from Simulation_Content.Simulation import FSample


class AMTransceiver:
    """Can emit and receive AM Signals

    -Needs power to work
    -Has its own Carrier Wave
    """

    def __init__(self, Power: Signals):
        """
        :param Power: Power needed to work
        :type Power: Signals
        """
        self._Transmitter = AMTransmitter(Power)
        self._Receiver = AMReceiver(self._Transmitter.Carrier, Power)
        self._demodulated: Union[None, Signals] = None
        self._Modulated: Union[None, Signals] = None

    @property
    def Demodulated(self) -> Signals:
        """Get Demodulated Signal


        :return: Demodulated signal
        :rtype: Signals """
        if not self._demodulated:
            raise Exception("Nothing to receive")
        return self._demodulated

    @property
    def Modulated(self) -> Signals:
        """Modulated Signal


                :return: Modulated signal
                :rtype: Signals """
        if not self._Modulated:
            raise Exception("Nothing to receive")
        return self._Modulated

    @Modulated.setter
    def Modulated(self, Modulated: Signals) -> None:
        """Modulated Signal

        :param Modulated: Signal to demodulate thus it has to be modulated
        :type Modulated: Signals
        """
        self._Modulated = Modulated

    def Send(self, Content: Signals) -> None:
        """Send Content (Modulate it)


        :param Content: Content to send
        :type Content: Signals"""
        self._Modulated = self._Transmitter.Send(Content)

    def Demodulate(self, FC=10000, Fs=FSample) -> None:
        """Demodulate content of self.Modulated


         :param FC: Cutoff frequency (must be bigger than signal frequency and smaller than carrier frequency (default FC=10000Hz)
         :type FC: float
         :param Fs: Sample frequency must be the same of time-step simulation (default Fs=FSample)
         :type Fs: float"""
        if not self._Modulated:
            raise Exception("Nothing to receive")
        self._Receiver.Demodulate(self._Modulated, FC, Fs)
        self._demodulated = self._Receiver.Demodulated

    def TreatSignal(self, FC=5, FS=FSample) -> None:
        """Apply a high pass to remove demodulated signal's offset caused by modulation


        :param FC: Cutoff of high pass frequency, must be smalle as possible (default is 5Hz)
        :type FC:float
        :param FS: Sample frequency must be the same of time-step simulation (default Fs=FSample)
        :type FS: float"""
        self._Receiver.TreatSignal(FC, FS)
        self._demodulated = self._Receiver.Demodulated
