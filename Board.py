from typing import List
from AM.AM_Transceiver import *
from Devices.HF_Lf_Generator import FGenerator
from Devices.Oscilloscop import Scope
from Devices.SpectrumAnalyser import SpectrumAnalyser
from Simulation_Content.Signals import Signals
from Tools.Mixer import Mixer


class Board:
    """Main element of the simulation, each device and element has to be attached to this board,
    it simulated a bread-board"""

    def __init__(self, Power: Signals, *args: str):
        """"Main element of the simulation, each device and element has to be attached to this board,
        it simulated a bread-board

        :param Power: Alternative tension needed by every device
        :type Power: Signals
        :param *args:  Every devices that have to be attached to this board
            """
        self._Power = Power  # AC
        self._Devices: List[str] = []  # Devices list

        # Devices attached
        self._scope: Union[Scope, None] = None
        self._Generator: Union[FGenerator, None] = None
        self._Spectrum: Union[SpectrumAnalyser, None] = None
        self._Mixer: Union[Mixer, None] = None
        self._Transceiver: Union[AMTransceiver, None] = None

        for i in args:
            self._Devices.append(i)

        self._checkDevices()

    @property
    def Power(self) -> Signals:
        """" Get Power Property

        :return: AC Power attached to the board
        :rtype: Signals"""
        return self._Power

    @Power.setter
    def Power(self, Value: Signals):
        """" Set Power Property
        :type: Signals
         """
        self._Power = Value

    @property
    def Scope(self) -> Scope:
        """" Get Scope Property
                :return: Scope attached to the board
                :rtype: Signals"""
        if self._scope:
            return self._scope
        else:
            raise Exception("Scope is not wired to this board")

    @property
    def Mixer(self) -> Mixer:
        """" Get Mixer Property
                        :return: Mixer attached to the board
                        :rtype: Signals"""
        if self._Mixer:
            return self._Mixer
        else:
            raise Exception("Mixer is not wired to this board")

    @property
    def Transceiver(self) -> AMTransceiver:
        """" Get Transceiver Property
                        :return: Transceiver attached to the board
                        :rtype: Signals"""
        if self._Mixer:
            return self._Transceiver
        else:
            raise Exception("Transceiver is not wired to this board")

    @property
    def Generator(self) -> FGenerator:
        """" Get Generator Property
         :return: Generator attached to the board
        :rtype: Signals"""
        if self._Generator:
            return self._Generator
        else:
            raise Exception("Generator is not wired to this board")

    @property
    def Spectrum(self) -> SpectrumAnalyser:
        """" Get Spectrum Property
             :return: Spectrum Analyser attached to the board
            :rtype: Signals"""
        if self._Spectrum:
            return self._Spectrum
        else:
            raise Exception("Spectrum Analyser is not wired to this board")

    def _Switch(self, arg: str):
        """"To init specified property """
        if arg == "Scope":
            self._scope = Scope()
        elif arg == 'Spectrum':
            self._Spectrum = SpectrumAnalyser()
        elif arg == "Generator":
            self._Generator = FGenerator(self._Power)
        elif arg == "Mixer":
            self._Mixer = Mixer()
        elif arg == "AMTransceiver":
            self._Transceiver = AMTransceiver(self._Power)
        else:
            raise Exception(arg + " is an invalid Device")

    def _checkDevices(self):
        """To Attach each device to the board"""
        for i in self._Devices:
            self._Switch(i)
