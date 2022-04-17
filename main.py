#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication

from constants import c
from display import Display
from fdtd import FDTD
from GUI.mainwindow import MainWindow
from layer import Layer
from probe import Probe
from source import (SourceGauss, SourceHarmonic, SourceModulatedGaussian,
                    SourceRectangular)

if __name__ == "__main__":
    #  app = QApplication(sys.argv)
    #  execute = MainWindow()
    #  sys.exit()
    fdtd = FDTD(5, 5e-3, 1e-7, 1)
    #  fdtd.add_source(SourceModulatedGaussian(0.02, 0.5e-10, .125e-10, .25e-10, np.pi))
    #  fdtd.add_source(SourceGauss(0.02, 0.50e-9, .25e-9))
    fdtd.add_source(SourceHarmonic(1.5, 1e-10, c, 0))
    #  fdtd.add_source(SourceHarmonic(1.5, 1e-10, 2 * c / 3, np.pi))

    #  fdtd.add_source(SourceRectangular(0.02, 1e-9, .3e-10))
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
    fdtd.add_probes([2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25])
    #  fdtd.set_eps((0.06, 0.12), 3.5)
    #  fdtd.set_sigma((0.06, 0.12), .001)
    #  fdtd.add_layer(Layer((0.06, 0.12), 9, 1, 0.005))
    fdtd.add_layer(Layer((4.5, 5), 2, 1))
    #  fdtd.set_sigma((0.12, 0.18), .002)
    #  fdtd.set_sigma((0.18, 0.28), .003)
    #  fdtd.set_sigma((0.28, 0.5), .004)
    #  fdtd.set_eps((0.12, 0.18), 2.2)
    #  fdtd.set_eps((0.18, 0.28), 4)
    #  fdtd.set_eps((0.28, 0.5), 6)
    fdtd.analyze()
    fdtd.show_probe_signals()
