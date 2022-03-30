#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum, auto 
import numpy as np
from types import FunctionType
from constants import c

class SignalType(Enum):
    COS = auto()
    GAUSSIAN = auto()
    MODULATED_GAUSSIAN = auto()
    RECTANGULAR = auto()

class Signal:

    @staticmethod
    def get_function(**kwargs):
        signal_type = kwargs["signal_type"]
        fdtd = kwargs["fdtd"]
        pos = kwargs["pos"]
        eps = fdtd.eps[int(pos // fdtd.dx)]
        mu = fdtd.eps[int(pos // fdtd.dx) - 1]
        Sc = fdtd.Sc 
        if signal_type == SignalType.COS:
            freq = kwargs["freq"]
            phase = kwargs["phase"]
            f = lambda q, m: np.cos(2 * np.pi * freq * q + phase)
        elif signal_type == SignalType.GAUSSIAN:
            duration = kwargs["duration"] / fdtd.dt
            delay = kwargs["delay"] / fdtd.dt
            f = lambda q, m: np.exp(-(((q - m * (eps * mu) ** .5 / Sc) - delay) / duration) ** 2)
        elif signal_type == SignalType.MODULATED_GAUSSIAN:
            pass
        elif signal_type == SignalType.RECTANGULAR:
            duration = kwargs["duration"] / fdtd.dt
            delay = kwargs["delay"] / fdtd.dt
            f = lambda q, m: 1 if 0 <= (q - m * (eps * mu) ** .5 / Sc - delay) <= duration else 0
        return f

def get_function(**kwargs):
    signal_type = kwargs["signal_type"]
    eps = kwargs["eps"]
    Sc = kwargs["Sc"]
    mu = kwargs["mu"]
    fdtd = kwargs["fdtd"]
    if signal_type == SignalType.COS:
        freq = kwargs["freq"]
        phase = kwargs["phase"]
        f = lambda q, m: np.cos(2 * np.pi * freq * q + phase)
    elif signal_type == SignalType.GAUSSIAN:
        duration = kwargs["duration"] / fdtd.dt
        delay = kwargs["delay"] / fdtd.dt
        f = lambda q, m: np.exp(-((q - m * (eps * mu) ** .5 / Sc - delay) / duration) ** 2)
    elif signal_type == SignalType.MODULATED_GAUSSIAN:
            pass
    return f



if __name__ == "__main__":
    print(Signal.get_function(signal_type=SignalType.COS, freq=5, phase=0, eps=1, mu=1, Sc=1)(1, 2))
