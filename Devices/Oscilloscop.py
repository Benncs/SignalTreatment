import matplotlib.pyplot as plt

from Devices.Devices import _Device
from Simulation_Content.Signals import Signals
from Simulation_Content.Simulation import Time


class Scope(_Device):
    @staticmethod
    def Show(Signal: Signals, color: str = "", xlim=None, ylim=None, end=False):

        if color != "":
            plt.plot(Time.Value, Signal.data, color=color)
        else:
            plt.plot(Time.Value, Signal.data)
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        if end:
            plt.show()
