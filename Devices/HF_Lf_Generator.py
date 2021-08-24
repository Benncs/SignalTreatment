import numpy as np

from Plug import Plug
from Simulation_Content.Signals import Signals
from Simulation_Content.Simulation import Simulation_time

from Devices.Devices import _Device


class FGenerator(_Device):
    def __init__(self, Power:Signals):
        super().__init__()
        self._VACNeeded: Signals = Plug()
        self._VDCNeeded = Power.RMSValue
        if not Power == self._VACNeeded:
            raise Exception("Voltage too low")
        return

    def Cos(self, t: Simulation_time, f, amplitude=1, phi=0) -> Signals:
        Res = Signals(data=amplitude * np.cos(2 * np.pi * f * t.Value + phi), Max=amplitude, Min=-amplitude)
        if amplitude > self._VDCNeeded:
            return self._Saturation(Res)
        else:
            return Res
        # return np.cos(2 * np.pi * f * Time.Value + phi)

    def Sin(self, t: Simulation_time, f, amplitude=1, phi=0) -> Signals:
        Res = Signals(data=amplitude * np.sin(2 * np.pi * f * t.Value + phi), Max=amplitude, Min=-amplitude)
        if amplitude > self._VDCNeeded:
            return self._Saturation(Res)
        else:
            return Res

    def Square(self, t: Simulation_time, f, duty=1) -> Signals:
        # T = 1/f/duty
        sin = np.sin(2 * np.pi * f * t.Value)
        return self._sign(sin)

    @staticmethod
    def _sign(x: np.ndarray) -> Signals:
        sizeof = x.size
        data = np.zeros(sizeof)
        for index in range(sizeof):
            if x[index] < 0:
                data[index] = -1
            elif x[index] == 0:
                data[index] = 0
            else:
                data[index] = 1
        return Signals(data, length=sizeof, Min=-1, Max=1)

    def Sawtooth(self, x: np.ndarray, f, phi=0) -> np.ndarray:
        timeshift = phi / np.pi
        time = (x - timeshift)
        slope = (time - np.floor(time))
        return np.mod(slope, 1 / f)

    def _Pulse(self, x, f, duty=1, sumindex=100):
        return self.Sawtooth(x, f, 0) - self.Sawtooth(x, f, -np.pi / 2)
