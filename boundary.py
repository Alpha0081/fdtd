#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import numpy.typing as npt
from abc import ABCMeta, abstractmethod


class Boundary(metaclass=ABCMeta):
    @abstractmethod
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        pass


class SimpleBoundaryLeft(Boundary):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[0] = E[1]
        H[0] = H[1]
        return True


class SimpleBoundaryRight(Boundary):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[-1] = E[-2]
        H[-1] = H[-2]
        return True


class PECLeft(Boundary):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[0] = 0
        return True


class PECRight(Boundary):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[-1] = 0
        return True

class PMCLeft(Boundary):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        H[0] = 0
        return True


class PMCRight(Boundary):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        H[-1] = 0
        return True


class ABCBase(Boundary):
    def __init__(self) -> None:
        self._Sc: float = 1
        self._eps: float = 1
        self._mu: float = 1

    @property
    def Sc(self) -> float:
        return self._Sc

    @Sc.setter
    def Sc(self, value: float) -> bool:
        self._Sc = value
        return True

    @property
    def eps(self) -> float:
        return self._eps

    @eps.setter
    def eps(self, value: float) -> bool:
        self._eps = value
        return True

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, value: float) -> bool:
        self._mu = value
        return True

    @abstractmethod
    def update_coefficient(self) -> bool:
        pass


class ABCFirst(ABCBase):
    def __init__(self):
        super().__init__()
        self._oldE = 0

    def update_coefficient(self):
        temp = self._Sc / (self._mu * self._eps) ** 0.5
        self._coefficient = (temp - 1) / (temp + 1)


class ABCFirstLeft(ABCFirst):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[0] = self._oldE + self._coefficient * (E[1] - E[0])
        self._oldE = E[1]
        return True


class ABCFirstRight(ABCFirst):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[-1] = self._oldE + self._coefficient * (E[-2] - E[-1])
        self._oldE = E[-2]
        return True


class ABCSecond(ABCBase):
    def __init__(self):
        super().__init__()
        self._oldE: npt.NDArray[np.float64] = np.zeros(3)
        self._old_oldE: npt.NDArray[np.float64] = np.zeros(3)

    def update_coefficient(self):
        Sc_env = self._Sc / (self._eps * self._mu) ** 0.5
        self._k1 = -1 / (1 / Sc_env + 2 + Sc_env)
        self._k2 = 1 / Sc_env - 2 + Sc_env
        self._k3 = 2 * (Sc_env - 1 / Sc_env)
        self._k4 = 4 * (1 / Sc_env + Sc_env)


class ABCSecondLeft(ABCSecond):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[0] = (
            self._k1
            * (
                self._k2 * (E[2] + self._old_oldE[0])
                + self._k3 * (self._oldE[0] + self._oldE[2] - E[1] - self._old_oldE[1])
                - self._k4 * self._oldE[1]
            )
            - self._old_oldE[2]
        )
        self._old_oldE[:] = self._oldE[:]
        self._oldE[:] = E[0:3]
        return True


class ABCSecondRight(ABCSecond):
    def update_field(
        self, E: npt.NDArray[np.float64], H: npt.NDArray[np.float64]
    ) -> bool:
        E[-1] = (
            self._k1
            * (
                self._k2 * (E[-3] + self._old_oldE[-1])
                + self._k3
                * (self._oldE[-1] + self._oldE[-3] - E[-2] - self._old_oldE[-2])
                - self._k4 * self._oldE[-2]
            )
            - self._old_oldE[-3]
        )
        self._old_oldE[:] = self._oldE[:]
        self._oldE[:] = E[-3:]
        return True
