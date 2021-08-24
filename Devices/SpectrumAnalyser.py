import numpy as np
from matplotlib import pyplot as plt
from numpy.fft import fft

from Devices.Devices import _Device
from Simulation_Content.Signals import Signals
from Simulation_Content.Simulation import FSample


class SpectrumAnalyser(_Device):
    @staticmethod
    def _Compute(Signal: Signals, xlim=None, text=''):
        X = fft(Signal.data)
        N = len(X)
        n = np.arange(N)
        sr = FSample
        T1 = N / sr
        freq = n / T1
        plt.figure()
        plt.stem(freq, np.abs(X), 'b', markerfmt=" ", basefmt="-b")
        plt.xlabel('Freq (Hz)' + text)
        plt.ylabel('FFT Amplitude |X(freq)|')
        if xlim is not None:
            plt.xlim(xlim)
        return

    @staticmethod
    def Show(*args: Signals):
        for i in args:
            SpectrumAnalyser._Compute(i)
        plt.show()
        return