from typing import Union

import numpy as np
from Simulation_Content.Signals import Signals
from Simulation_Content.Singleton import Singleton


class _Device(metaclass=Singleton):
    """Base of device, can be measure device or other kind of electronic device """
    _FftProp = {'FourierTransform': np.ndarray, 'Frequencies': np.ndarray}  # type for a dict use in fft method

    def __init__(self, signal: Signals = None):
        """
        :param signal: Optional
        :type signal: Signals
        """
        if signal is not None:
            self._Signal = signal.data
        self._VDCNeeded = 0
        self._VACNeeded = 0

    def _FFT(self, Signal: Union[Signals,None], fSample: float) -> _FftProp:
        """

        :param Signal: Signal to wich fft is processed
        :type Signal: Signals
        :param fSample: Sampling frequency, has to be the same of 1/timestep
        :type fSample: float
        :return: Dict with fourier transform and associated frequencies
        :rtype: _FftProp
        """
        from numpy.fft import rfft
        f_signal: np.ndarray = np.zeros(0)

        # Process to FFT
        if Signal is None:
            f_signal = rfft(self._Signal)
        else:
            f_signal = rfft(Signal.data)

        N = Signal.len if (Signal is not None) else self._Signal.size # Compute size
        n = np.arange(N)
        T1 = N / fSample # samplig period
        W = n[:int(N / 2) + 1] / T1 # Associated frequencies, half of n because there is complex frequencies that is not useful
        #W = rfftfreq(N, d=fSample)

        return {"FourierTransform": f_signal, "Frequencies": W}

    def _Saturation(self, Value: Signals) -> Signals:
        """
        Simulate saturation if voltage's signal > voltage's alimentation
        :param Value: Value to "Saturate"
        :type Value: Signals
        :return: Saturated signals
        :rtype: Signals
        """
        Copy = Value.data.copy()
        # if abs(value)>power value = power

        for i in range(len(Copy)):
            if Copy[i] > self._VDCNeeded:
                Copy[i] = self._VDCNeeded
            elif Copy[i] < -self._VDCNeeded:
                Copy[i] = -self._VDCNeeded
            else:
                pass
        return Signals(Copy, Max=self._VDCNeeded, Min=Value.Min, length=Value.len)
