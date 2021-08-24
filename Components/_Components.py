from typing import Union

from Simulation_Content.Signals import Signals


from Simulation_Content.Singleton import Singleton

class _Components(metaclass=Singleton):
    def Run(self, Signal: Signals) -> Signals:
        raise NotImplementedError()

    def Apply(self, Signal1: Union[Signals,float],Signal2: Signals) -> Signals:
        raise NotImplementedError()
