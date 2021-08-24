import numpy as np

from Simulation_Content.Simulation import Simulation_time
from Simulation_Content.Signals import Signals


class Plug(Signals):
    """"Class inherited from Signals, represents electricity from the plug """
    def __init__(self, t: Simulation_time = Simulation_time()) -> None:
        """"Class inherited from Signals, represents electricity from the plug
        :param t: Duration of the Simulation
        :type t :Simulation_time
        """
        self._freq = 50
        self._data = 325 * np.sin(2 * np.pi * self._freq * t.Value) # 50 Hz Signal 230 rms value
        self._Power = 100 # Watt
        super().__init__(self._data, Min=-325, Max=-325, rms=230)
        return
