#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from types import FunctionType, MethodType

import numpy as np


class SourceBase(metaclass=ABCMeta):
    @abstractmethod
    def E(self, m: float, q: float) -> float:
        pass


class Source(SourceBase):
    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> bool:
        self._position = value
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

    @property
    def Sc(self) -> float:
        return self._Sc

    @Sc.setter
    def Sc(self, value: float) -> bool:
        self._Sc = value
        return True

    @property
    def dt(self) -> float:
        return self._dt

    @dt.setter
    def dt(self, value: float) -> bool:
        self._dt = value
        return True


class SourceGauss(Source):
    def __init__(self, position: float, delay: float, duration: float) -> None:
        self._position: float = position
        self._delay = delay
        self._duration = duration

    def E(self, m: float, q: float) -> float:
        return np.exp(
            -(
                (
                    (
                        (q - m * (self._eps * self._mu) ** 0.5 / self._Sc)
                        - self._delay / self._dt
                    )
                    / (self._duration / self.dt)
                )
                ** 2
            )
        )


class SourceModulatedGaussian(Source):
    def __init__(
        self,
        position: float,
        delay: float,
        duration: float,
        period: float,
        phase: float,
    ) -> None:
        self._position: float = position
        self._delay = delay
        self._duration = duration
        self._period = period
        self._phase = phase

    def E(self, m: float, q: float) -> float:
        return np.exp(
            -(
                (
                    (
                        (q - m * (self._eps * self._mu) ** 0.5 / self._Sc)
                        - self._delay / self._dt
                    )
                    / (self._duration / self.dt)
                )
                ** 2
            )
        ) * np.cos(
            2
            * np.pi
            / (self._period / self._dt)
            * (q - m * self._eps * self._mu / self._Sc)
            + self._phase
        )


class SourceRectangular(Source):
    def __init__(self, position: float, delay: float, duration: float) -> None:
        self._position: float = position
        self._delay = delay
        self._duration = duration

    def E(self, m: float, q: float) -> float:
        return (
            1.0
            if 0
            <= (
                q
                - m * (self._eps * self._mu) ** 0.5 / self._Sc
                - self._delay / self._dt
            )
            <= self._duration / self._dt
            else 0.0
        )


class SourceHarmonic(Source):
    def __init__(
        self, position: float, delay: float, frequency: float, phase: float, count=None
    ) -> None:
        self._position: float = position
        self._delay = delay
        self._frequency = frequency
        self._phase = phase
        self._count = count

    def E(self, m: float, q: float) -> float:
        return (
            0.25
            * np.sin(
                2
                * np.pi
                * self._frequency
                * self._dt
                * (q - m * self._eps * self._mu / self._Sc)
                + self._phase
            )
            if self._count is None
            else np.sin(
                2
                * np.pi
                * self._frequency
                * self._dt
                * (q - m * self._eps * self._mu / self._Sc)
                + self._phase
            )
            if q * self._dt <= self._count / self._frequency
            else 0
        )
