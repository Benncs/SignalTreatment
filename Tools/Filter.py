from dataclasses import dataclass
from scipy import signal

import numpy as np

from Simulation_Content.Simulation import  DX


@dataclass
class Filters:
    NAME: str
    FC: float = None
    TYPE: str = ""
    ORDER: int = 1
    FC2: float = None
    FS: float = 1/DX


class Filter:
    def __init__(self, T=None):
        if T is None:
            T = []
        self._t = T

    @staticmethod
    def ToList(Array: np.ndarray) -> list:
        return [value for value in Array]

    def Frequencies(self, FilterInfo: Filters) -> list:
        f_nyq = FilterInfo.FS / 2.

        return [FilterInfo.FC / f_nyq] if FilterInfo.FC2 is None else [FilterInfo.FC / f_nyq, FilterInfo.FC2 / f_nyq]

    def ButterWorth_LowPass(self, Signal: list, order: int, fc: float, fs: float = 10000) -> list:
        f_nyq = fs / 2.
        W = fc / f_nyq
        [b, a] = signal.butter(order, W, 'low', analog=False)
        return self.ToList(signal.filtfilt(b, a, Signal))

    def LowPass(self, Signal, t, filt: Filters):
        f = np.sin(2 * np.pi * filt.FS * t) / (t * np.pi)

        c = np.cos(6.28 * filt.FS * t)

        demod = 2 * c * np.asarray(Signal)

        return np.convolve(f, demod)

    def ButterWorth_LowPass1(self, Signal: list, FilterProperties: Filters) -> list:
        W = self.Frequencies(FilterProperties)
        [b, a] = signal.butter(FilterProperties.ORDER, W, 'low', analog=False)
        return self.ToList(signal.filtfilt(b, a, Signal))

    def BandPass(self, fe, fca, fcb, p=50):
        a = fca / fe
        b = fcb / fe

        def g(k):
            if k == 0:
                return 2 * (b - a)
            else:
                return (np.sin(2 * np.pi * k * b) - np.sin(2 * np.pi * k * a)) / (k * np.pi)

        return self._GeneralFilter(g, p)

    @staticmethod
    def _GeneralFilter(g, P, window="hann"):
        from scipy.signal import get_window
        N = 2 * P + 1  # ordre du filtre
        Klist = np.arange(start=-P, stop=P + 1)
        n = Klist.size
        h = np.zeros(n)
        for k in range(n):
            h[k] = g(Klist[k])
        if window != "rect":
            h = h * get_window(window, N)
        return h

    def ButterWorth_BandPass(self, Signal: list, FilterProperties: Filters) -> list:
        W = self.Frequencies(FilterProperties)
        [b, a] = signal.butter(FilterProperties.ORDER, W, btype='band')
        s_but = [i for i in signal.filtfilt(b, a, Signal)]
        return s_but

    def ButterWorth_BandPass2(self, Signal: list, FilterProperties: Filters) -> list:
        W = self.Frequencies(FilterProperties)
        sos = signal.butter(FilterProperties.ORDER, W, btype='band', output='sos',analog=False)
        return self.ToList(signal.sosfiltfilt(sos, Signal))

    def ButterWorth_LowPass2(self, Signal: list, FilterProperties: Filters) -> list:
        W = self.Frequencies(FilterProperties)
        sos = signal.butter(FilterProperties.ORDER, W, 'low', output='sos', analog=False)
        return self.ToList(signal.sosfiltfilt(sos, Signal))

    def ButterWorth_HighPass(self, Signal: list, FilterProperties: Filters) -> list:
        W = self.Frequencies(FilterProperties)
        sos = signal.butter(FilterProperties.ORDER, W, 'high', output='sos', analog=False)
        return self.ToList(signal.sosfiltfilt(sos, Signal))
