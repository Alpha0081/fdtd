#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from types import FunctionType, MethodType

import numpy as np


class Source(ABC):
    @abstractmethod
    def E(self, m: float, q: float) -> float:
        pass

    @property
    @abstractmethod
    def position(self) -> float:
        pass

    @position.setter
    @abstractmethod
    def position(self, value: float) -> bool:
        pass

    @property
    @abstractmethod
    def eps(self) -> float:
        pass

    @eps.setter
    @abstractmethod
    def eps(self, value: float) -> bool:
        pass

    @property
    @abstractmethod
    def mu(self) -> float:
        pass

    @mu.setter
    @abstractmethod
    def mu(self, value: float) -> bool:
        pass

    @property
    @abstractmethod
    def Sc(self) -> float:
        pass

    @Sc.setter
    @abstractmethod
    def Sc(self, value: float) -> bool:
        pass

    @property
    @abstractmethod
    def dt(self) -> float:
        pass

    @dt.setter
    @abstractmethod
    def dt(self, value: float) -> bool:
        pass


class SourceGauss(Source):
    def __init__(self, position: float, delay: float, duration: float) -> None:
        self.__position: float = position
        self.__delay = delay
        self.__duration = duration

    def E(self, m: float, q: float) -> float:
        return np.exp(
            -(
                (
                    (
                        (q - m * (self.__eps * self.__mu) ** 0.5 / self.__Sc)
                        - self.__delay / self.__dt
                    )
                    / (self.__duration / self.dt)
                )
                ** 2
            )
        )

    @property
    def position(self) -> float:
        return self.__position

    @position.setter
    def position(self, value: float) -> bool:
        self.__position = value
        return True

    @property
    def eps(self) -> float:
        return self.__eps

    @eps.setter
    def eps(self, value: float) -> bool:
        self.__eps = value
        return True

    @property
    def mu(self) -> float:
        return self.__mu

    @mu.setter
    def mu(self, value: float) -> bool:
        self.__mu = value
        return True

    @property
    def Sc(self) -> float:
        return self.__Sc

    @Sc.setter
    def Sc(self, value: float) -> bool:
        self.__Sc = value
        return True

    @property
    def dt(self) -> float:
        return self.__dt

    @dt.setter
    def dt(self, value: float) -> bool:
        self.__dt = value
        return True


class SourceModulatedGaussian(Source):
    def __init__(
        self,
        position: float,
        delay: float,
        duration: float,
        period: float,
        phase: float,
    ) -> None:
        self.__position: float = position
        self.__delay = delay
        self.__duration = duration
        self.__period = period
        self.__phase = phase

    def E(self, m: float, q: float) -> float:
        return np.exp(
            -(
                (
                    (
                        (q - m * (self.__eps * self.__mu) ** 0.5 / self.__Sc)
                        - self.__delay / self.__dt
                    )
                    / (self.__duration / self.dt)
                )
                ** 2
            )
        ) * np.cos(
            2
            * np.pi
            / (self.__period / self.__dt)
            * (q - m * self.__eps * self.__mu / self.__Sc)
            + self.__phase
        )

    @property
    def position(self) -> float:
        return self.__position

    @position.setter
    def position(self, value: float) -> bool:
        self.__position = value
        return True

    @property
    def eps(self) -> float:
        return self.__eps

    @eps.setter
    def eps(self, value: float) -> bool:
        self.__eps = value
        return True

    @property
    def mu(self) -> float:
        return self.__mu

    @mu.setter
    def mu(self, value: float) -> bool:
        self.__mu = value
        return True

    @property
    def Sc(self) -> float:
        return self.__Sc

    @Sc.setter
    def Sc(self, value: float) -> bool:
        self.__Sc = value
        return True

    @property
    def dt(self) -> float:
        return self.__dt

    @dt.setter
    def dt(self, value: float) -> bool:
        self.__dt = value
        return True


class SourceRectangular(Source):
    def __init__(self, position: float, delay: float, duration: float) -> None:
        self.__position: float = position
        self.__delay = delay
        self.__duration = duration

    def E(self, m: float, q: float) -> float:
        return (
            1.0
            if 0
            <= (
                q
                - m * (self.__eps * self.__mu) ** 0.5 / self.__Sc
                - self.__delay / self.__dt
            )
            <= self.__duration / self.__dt
            else 0.0
        )

    @property
    def position(self) -> float:
        return self.__position

    @position.setter
    def position(self, value: float) -> bool:
        self.__position = value
        return True

    @property
    def eps(self) -> float:
        return self.__eps

    @eps.setter
    def eps(self, value: float) -> bool:
        self.__eps = value
        return True

    @property
    def mu(self) -> float:
        return self.__mu

    @mu.setter
    def mu(self, value: float) -> bool:
        self.__mu = value
        return True

    @property
    def Sc(self) -> float:
        return self.__Sc

    @Sc.setter
    def Sc(self, value: float) -> bool:
        self.__Sc = value
        return True

    @property
    def dt(self) -> float:
        return self.__dt

    @dt.setter
    def dt(self, value: float) -> bool:
        self.__dt = value
        return True


class SourceHarmonic(Source):
    def __init__(
        self, position: float, delay: float, frequency: float, phase: float, count=None
    ) -> None:
        self.__position: float = position
        self.__delay = delay
        self.__frequency = frequency
        self.__phase = phase
        self.__count = count

    def E(self, m: float, q: float) -> float:
        return (
            np.sin(
                2
                * np.pi
                * self.__frequency
                * self.__dt
                * (q - m * self.__eps * self.__mu / self.__Sc)
                + self.__phase
            )
            if self.__count is None
            else np.sin(
                2
                * np.pi
                * self.__frequency
                * self.__dt
                * (q - m * self.__eps * self.__mu / self.__Sc)
                + self.__phase
            )
            if q * self.__dt <= self.__count / self.__frequency
            else 0
        )

    @property
    def position(self) -> float:
        return self.__position

    @position.setter
    def position(self, value: float) -> bool:
        self.__position = value
        return True

    @property
    def eps(self) -> float:
        return self.__eps

    @eps.setter
    def eps(self, value: float) -> bool:
        self.__eps = value
        return True

    @property
    def mu(self) -> float:
        return self.__mu

    @mu.setter
    def mu(self, value: float) -> bool:
        self.__mu = value
        return True

    @property
    def Sc(self) -> float:
        return self.__Sc

    @Sc.setter
    def Sc(self, value: float) -> bool:
        self.__Sc = value
        return True

    @property
    def dt(self) -> float:
        return self.__dt

    @dt.setter
    def dt(self, value: float) -> bool:
        self.__dt = value
        return True
