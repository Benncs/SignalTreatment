from Simulation_Content.Signals import Signals
from Devices.DigitialFilter import DigitFilter
from Simulation_Content.Simulation import *


class ColpittsOscillator:
    """Oscillator that give a Carrier Wave with a frequency of 58 MHz"""
    def __init__(self, current=5e-3):
        """Oscillator that give a Carrier Wave with a frequency of 58 MHz
        :param current: bias current of the simulated transistor
        :type current: float"""

        self._I = current
        # Analogical component to init oscillation
        self._R1 = 2.2e3
        self._L = 150e-9
        self._C1 = 1e-10
        self._C2 = 1e-10
        self._C3 = 100e-9
        self._R2 = 10e3
        self._R3 = 10e3
        self._C = (self._C1 * self._C2) / (self._C1 + self._C2)
        self._Amplitude = 2 * self._I * self._R3 * (self._C2 / (self._C1 + self._C2))

    @property
    def freq(self):
        return 1 / (2 * np.pi * np.sqrt(self.L * self._C))

    def Run(self, time: Simulation_time = Simulation_time(), Filtrage: bool = False) -> Signals:
        """Return the carrier signal
        :param time: Duration of the simulation
        :type time: Simulation_time
        :param Filtrage: Filtrate the wave to have a better signal (default is False)
        :type Filtrage: bool
        :return Signal of the Carrier
        :rtype: Signals
        """

        LoadCollectorRes = 5
        freq = self.freq  # Amplitude computed with component value
        amp = self._Amplitude  # Amplitude computed with component value
        data :np.ndarray = amp*np.cos(2*np.pi*freq*time.Value)
        Res :Signals= Signals(data,Max=amp,Min=-amp)
        if not Filtrage:
            return Res #FGenerator().Cos(Time=time, f=freq, amplitude=amp, phi=0)
        else:
            return self._Filtrage(Res)

    @property
    def Amplitude(self):
        return self._Amplitude

    def _Filtrage(self, Signal: Signals) -> Signals:
        return DigitFilter().BandPas(58e6, 59e6, Signal, DX)

    @property
    def R1(self):
        return self._R1

    @R1.setter
    def R1(self, value):
        if value > 0:
            self._R1 = value
        else:
            raise Exception("Value must be positive")

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, value):
        if value > 0:
            self._L = value
        else:
            raise Exception("Value must be positive")

    @property
    def C1(self):
        return self._C1

    @C1.setter
    def C1(self, value):
        if value > 0:
            self._C1 = value
        else:
            raise Exception("Value must be positive")

    @property
    def C3(self):
        return self._C3

    @C3.setter
    def C3(self, value):
        if value > 0:
            self._C3 = value
        else:
            raise Exception("Value must be positive")
