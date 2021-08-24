from __future__ import annotations

from typing import Union

import numpy as np

class Signals:
    """Represents an electrical signal, derived from np.ndarray but some features aren't available for realism
    purpose """
    def __init__(self, data: np.ndarray, length: int = None, Max: float = None, Min: float = None, rms: float = None):
        """
        :param data: VOltage value over time
        :type data: np.ndarray, element has to numbers
        :param length: Size of data (default None, compute after initialisation)
        :type length: int
        :param Max: Max value of the dataset (default None, compute after initialisation)
        :type Max: float
        :param Min: Min value of the dataset (default None, compute after initialisation)
        :type Min: float
        :param rms: Rms value of the dataset (default None, compute after initialisation)
        :type rms: float
        """
        self._data: np.ndarray = data.copy()
        self._len: int = length if (length is not None) else data.size
        self._max: float = Max
        self._min: float = Min
        self._rms: float = rms
        self._freq : Union[float, None] = None
        if not Max or not Min:
            self._sort = self.ToList()

    def ToList(self) -> list:
        """
        In case of a list is needed, not recommended
        :return: data with type of list
        :rtype:list
        """
        return [value for value in self._data]

    def __eq__(self, other: Signals) -> bool:
        """
        Overload of == symbol
        :param other: other Signal that has to compared
        :type other: Signals
        :return: True if data, max,min,rms are equals
        :rtype: bool
        """
        if self.len != other.len:
            return False
        flag = True
        flag *= np.array_equal(self.data,other.data)
        flag *= self._rms == other.RMSValue
        flag *= self._min == other.Min
        flag *= self._max == other.Max
        return flag

    @property
    def data(self) -> np.ndarray:
        """
        Get signal's raw data
        :return: Signal dataset
        :rtype: np.ndarray
        """
        return self._data

    @property
    def RMSValue(self) -> float:
        """
        Get Signal's rms value
        :return: Signal's rms value
        :rtype: float
        """
        if not self._rms:
            self._rms = self.Max / np.sqrt(2)
        return self._rms

    @property
    def len(self) -> int:
        """
        Get Signal data's  size
        :return: Signal's size
        :rtype: int
                """
        return self._len

    @property
    def Max(self) -> float:
        """
        Get Signal data's  max value
        :return: Signal's max value
        :rtype: float
                        """
        if not self._max:
            self._max = self._sort[0]
        return self._max

    @property
    def Min(self) -> float:
        """
        Get Signal data's  min value
        :return: Signal's min value
        :rtype: float
                        """
        if not self._min:
            self._min = self._sort[-1]
        return self._min

    def _sort(self) -> list:
        """
        Use to find out max and min
        :return: sorted list of data
        :rtype: list
        """
        copy = self.ToList()
        copy.sort()
        return copy

    @staticmethod
    def _QSort(u: list) -> list:
        if not u:
            return []
        pivot, g, d = u[0], [], []
        for x in u[1:]: g.append(x) if x < pivot else d.append(x)
        return Signals._QSort(g) + [u[0]] + Signals._QSort(d)
