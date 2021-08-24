from dataclasses import dataclass

import numpy as np
from numpy import arange

DX = 2e-9  # time set

FSample = 1 / DX # sampling frequency

VDC = 12

fQuartz = 1e9  # Local Oscillator 1 Ghz


@dataclass
class Simulation_time:
    """
    Contains time information for simulation
    """
    Start_Time: float = 0
    End_Time: float = 0.00005
    Step: float = DX
    Value: np.ndarray = arange(Start_Time, End_Time, DX)
    Length = Value.size


Time = Simulation_time()
