#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Layer:
    def __init__(
        self, field: tuple[float], eps: float = 1, mu: float = 1, sigma: float = 0
    ) -> None:
        self.__eps: float = eps
        self.__mu: float = mu
        self.__sigma: float = sigma
        self.__field: tuple = field
        self.__name: str = ""

    @property
    def eps(self) -> float:
        return self.__eps

    @eps.setter
    def eps(self, value) -> bool:
        self.__eps = value
        return True

    @property
    def mu(self) -> float:
        return self.__mu

    @mu.setter
    def mu(self, value) -> bool:
        self.__mu = value
        return True

    @property
    def sigma(self) -> float:
        return self.__sigma

    @sigma.setter
    def sigma(self, value) -> bool:
        self.__sigma = value
        return True

    @property
    def field(self) -> tuple[float]:
        return self.__field

    @field.setter
    def field(self, value: tuple[float]) -> bool:
        self.__field = value
        return True

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> bool:
        self.__name = value
        return True
