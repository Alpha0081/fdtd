#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Layer:
    def __init__(
        self,
        area: tuple[float, float],
        eps: float = 1.,
        mu: float = 1.,
        sigma: float = 0.,
    ) -> None:
        self.__eps: float = eps
        self.__mu: float = mu
        self.__sigma: float = sigma
        self.__area: tuple[float, float] = area
        self.__name: str = ""

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
    def sigma(self) -> float:
        return self.__sigma

    @sigma.setter
    def sigma(self, value: float) -> bool:
        self.__sigma = value
        return True

    @property
    def area(self) -> tuple[float, float]:
        return self.__area

    @area.setter
    def area(self, value: tuple[float, float]) -> bool:
        self.__area = value
        return True

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> bool:
        self.__name = value
        return True
