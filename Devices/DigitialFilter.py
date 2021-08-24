import numpy as np

from Simulation_Content.Signals import Signals
from Simulation_Content.Simulation import FSample
from Devices.Devices import  _Device


class DigitFilter(_Device):

    def __init__(self, signal: Signals = None):
        super().__init__(signal)

    def HighPass(self, frequence: float, Signal: Signals = None, fSample=FSample) -> Signals:
        from numpy.fft import irfft
        FFTData = self._FFT(Signal, fSample)

        cut_f_signal = FFTData['FourierTransform']
        cut_f_signal[(FFTData['Frequencies'] < frequence)] = 0
        return Signals(irfft(cut_f_signal))

    def LowPass(self, cutoff: float, Signal: Signals = None, fSample=FSample) -> Signals:
        from numpy.fft import irfft
        FFTData = self._FFT(Signal, fSample)

        cut_f_signal = FFTData['FourierTransform']
        cut_f_signal[(FFTData['Frequencies'] > cutoff)] = 0

        return Signals(irfft(cut_f_signal))

    def BandPas(self, fc1: float, fc2: float, Signal: Signals = None, fSample=FSample) -> Signals:
        if fc2 < fc1:
            fc1, fc2 = fc2, fc1
        from numpy.fft import irfft
        FFTData = self._FFT(Signal, fSample)

        cut_f_signal = FFTData['FourierTransform']
        cut_f_signal[(FFTData['Frequencies'] > fc2)] = 0  # Low pass : f<fc2
        cut_f_signal[(FFTData['Frequencies'] < fc1)] = 0  # High Pass : fc<f

        return Signals(irfft(cut_f_signal))

    def Notch(self, fc1: float, fc2: float, Signal: Signals = None, fSample=FSample) -> Signals:
        if fc2 < fc1:
            fc1, fc2 = fc2, fc1
        from numpy.fft import irfft
        FFTData = self._FFT(Signal, fSample)

        cut_f_signal = FFTData['FourierTransform']
        # cut_f_signal[(FFTData['Frequencies'] < fc2)] = 0  # Low pass : f<fc2
        cut_f_signal[np.logical_and(FFTData['Frequencies'] > fc1, FFTData['Frequencies'] < fc2)] = 0  # High Pass : fc<f

        return Signals(irfft(cut_f_signal))
