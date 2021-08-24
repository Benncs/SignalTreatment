from typing import Union

import numpy as np

from Simulation_Content.Signals import Signals

from Components._Components import _Components


class SummingAmplifier(_Components):
    """To simulate signal addition, by ac or dc voltage """

    def Run(self, Signal: Signals) -> Signals:
        raise NotImplementedError()

    def Apply(self, Signal1: Union[Signals, float], Signal2: Signals) -> Signals:
        """
        Main method
        :param Signal1: First signal that has to be added, can be scalar or wave
        :type Signal1: Union[Signals,float]
        :param Signal2: Second signal that has to be added, can only be wave
        :type Signal2: Signals
        :return: Added signals
        :rtype: Signals
        """

        # Type checking
        if type(Signal1) == Signals:
            return Signals(data=Signal1.data + Signal2.data, length=Signal1.len)
        else:
            return Signals(data=Signal1 + Signal2.data, length=Signal2.len)


class Multiplier(_Components):
    """To simulate signal multiplication, by ac or dc voltage """

    def Run(self, Signal: Signals) -> Signals:
        raise NotImplementedError()

    def Apply(self, Signal1: Union[Signals, float], Signal2: Signals) -> Signals:
        """
        Main method, in case of scalar multiplication, in works as a perfect gain
        :param Signal1: First signal that has to be multiplied, can be scalar or wave
        :type Signal1: Union[Signals,float]
        :param Signal2: Second signal that has to be multiplied, can only be wave
        :type Signal2: Signals
        :return: Added signals
        :rtype: Signals
        """
        if type(Signal1) == Signals:
            return Signals(data=Signal1.data * Signal2.data, length=Signal1.len)
        else:
            return Signals(data=Signal1 * Signal2.data, length=Signal2.len)


# class SignalOperation:
#     # TODO Add class for each specified component
#
#     @staticmethod
#     def Multiplicator(FirstSignal: np.ndarray, SecondSignal: np.ndarray) -> np.ndarray:
#         if len(FirstSignal) != len(SecondSignal):
#             raise Exception("Signals must have same size")
#         # return [FirstSignal[i] * SecondSignal[i] for i in range(len(FirstSignal))]
#         return FirstSignal*SecondSignal
#
#     @staticmethod
#     def Offset( Signal: np.ndarray, Offsetvalue: float) -> np.ndarray:
#         #return [Offsetvalue + i for i in Signal]
#         return Offsetvalue + Signal
#
#     @staticmethod
#     def PerfectGain(Signal: np.ndarray, Gain: float) -> np.ndarray:
#         #return [Gain* i for i in Signal]
#         return Gain*Signal
#
#
#     @staticmethod
#     def AddAmplitude(FirstSignal: np.ndarray, SecondSignal: np.ndarray) -> np.ndarray:
#         if len(FirstSignal) != len(SecondSignal):
#             raise Exception("Signals must have same size")
#         # Res :list= []
#         # for i in range(len(FirstSignal)):
#         #     Res.append(FirstSignal[i]+SecondSignal[i])
#         return FirstSignal+SecondSignal


class Diode(_Components):
    """Simulate a diode, cut negative voltages """

    def Apply(self, Signal1: Union[Signals, float], Signal2: Signals) -> Signals:
        raise NotImplementedError()

    def Run(self, Signal: Signals) -> Signals:
        """

        :param Signal: Signal that has to be pass through diode
        :type Signal: Signals
        :return: Signal after diode
        :rtype: Signals
        """
        sizeof = Signal.len
        Res = np.zeros(sizeof)  # Init Result
        # If value < 0, replacing value by 0
        for value in range(sizeof):
            Res[value] = Signal.data[value] if (Signal.data[value] > 0) else 0
        return Signals(Res, Min=0, length=sizeof)  # [abs(val) for val in Signal]
