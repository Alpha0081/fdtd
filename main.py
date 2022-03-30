#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from probe import Probe
from display import Display
from source import Source
from fdtd import FDTD
from signals import get_function, Signal, SignalType

if __name__ == "__main__":

    fdtd = FDTD(500, 0.5, 4e-6, 1)
    fdtd.add_source(Source(50, Signal.get_function(signal_type=SignalType.GAUSSIAN, delay=0.5e-6, duration=0.5e-7, fdtd=fdtd, pos=50)))
    #  fdtd.add_source(
        #  Source(
            #  100,
            #  Signal.get_function(
                #  signal_type=SignalType.RECTANGULAR,
                #  delay=0.25e-6,
                #  duration=0.5e-7,
                #  fdtd=fdtd,
                #  pos=100,
            #  ),
        #  )
    #  )
    fdtd.add_probes([20, 70])
    #  fdtd.set_eps((0, 500), 4)
    fdtd.set_eps((120, 200), 9)
    #  fdtd.set_eps((125, 200), 36)
    fdtd.analyze()
    fdtd.showProbeSignals()
