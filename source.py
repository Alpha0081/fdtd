#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from signals import Signal, SignalType


class Source:
    def __init__(self, position: int, signal: Signal) -> None:
        self.__position = position
        self.__signal = signal
        print(self.__signal)

    def E(self, m: float, q: float) -> np.ndarray:
        return self.__signal(q, m) 

    def set_singal(self, signal: Signal) -> bool:
        self.__signal = signal
        return True
    
    @property
    def position(self) -> int:
        return self.__position

    @position.setter
    def position(self, value) -> bool:
        self.__position = value
        return True
