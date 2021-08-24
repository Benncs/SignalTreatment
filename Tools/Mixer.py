from Devices.Devices import _Device
from Simulation_Content.Signals import Signals


class Mixer(_Device):
    """Mixer, to treat signal amplitude """
    def __init__(self):
        super().__init__()

    @staticmethod
    def LowPass(MaxAmplitudeWanted: float, Value: Signals) -> Signals:
        """

        :param MaxAmplitudeWanted: Max amplitude wanted has to be smaller than signal's max
        :type MaxAmplitudeWanted: float
        :param Value: Signal to treat
        :type Value: Signals
        :return: Low passed signal
        :rtype: Signals
        """
        Copy = Value.data.copy()
        for i in range(len(Copy)):
            if Copy[i] > MaxAmplitudeWanted:
                Copy[i] = MaxAmplitudeWanted
            else:
                pass
        return Signals(Copy, Max=MaxAmplitudeWanted, Min=Value.Min, length=Value.len)

    @staticmethod
    def Compressor(MaxValueWanted: float, Value: Signals) -> Signals:
        """
        Linear compression, that is to say divide each signal's value by the same coefficient
        :param MaxValueWanted: Max value wanted has to be smaller than signal's max
        :type MaxValueWanted: float
        :param Value: Signal to treat
        :type Value: Signals
        :return: Compressed signal
        :rtype: Signals
        """
        ListMaxValue = Value.Max
        if ListMaxValue < MaxValueWanted:
            raise Exception("Value chosen is bigger than every value in the list")
        data = MaxValueWanted / ListMaxValue * Value.data
        return Signals(data=data, Max=MaxValueWanted, length=Value.len)

    @staticmethod
    def Norm(Signal: Signals) -> Signals:
        return Mixer().Compressor(1, Signal)
