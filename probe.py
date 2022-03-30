#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class Probe:
    def __init__(self, position: int, max_time: int) -> None:
        self.__position = position
        self.__E = np.zeros(max_time)
        self.__H = np.zeros(max_time)
        self.__time = 0

    def update_data(self, E: np.ndarray, H: np.ndarray) -> bool:
        self.__E[self.__time] = E[self.__position]
        self.__H[self.__time] = H[self.__position]
        self.__time += 1
        return True

    @property
    def E(self) -> np.ndarray:
        return self.__E

    @property
    def time(self) -> int:
        return self.__time

    @property
    def H(self) -> np.ndarray:
        return self.__H

    @property
    def position(self) -> int:
        return self.__position
