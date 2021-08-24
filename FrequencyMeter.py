import numpy as np

import Simulation_Content
from Simulation_Content.Signals import Signals


class FrequencyMeter:
    def __init__(self, Wave:Signals, fSample = Simulation_Content.FSample):
        self._Wave = Wave
        self._fs = fSample
        return

    def _fft(self):
        from numpy.fft import rfft
        f_signal = rfft(self._Wave.data)

        N = self._Wave.len
        n = np.arange(N)
        T1 = N / self._fs
        W = n[:int(N / 2) + 1] / T1
        Max = self._QSort(W)[-1]
        if Max != 0:
            return Max


    @staticmethod
    def _QSort(u: list) -> list:
        if not u:
            return []
        pivot, g, d = u[0], [], []
        for x in u[1:]: g.append(x) if x < pivot else d.append(x)
        return FrequencyMeter._QSort(g) + [u[0]] + FrequencyMeter._QSort(d)

