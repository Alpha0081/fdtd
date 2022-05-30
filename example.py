#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boundary import (
    ABCSecondLeft,
    ABCSecondRight,
)
from fdtd import FDTD
from layer import Layer
from source import (
    SourceGauss,
)


if __name__ == "__main__":
    fdtd = FDTD(5, 5e-3, 5e-8, 1)
    fdtd.set_left_boundary(ABCSecondLeft())
    fdtd.set_right_boundary(ABCSecondRight())
    fdtd.add_source(SourceGauss(1, 5e-9, 0.5e-9))
    fdtd.add_probes([2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25])
    fdtd.add_layer(Layer((0, 0.5), 9))
    fdtd.add_layer(Layer((4.5, 5), 4))
    fdtd.analyze()
    fdtd.show_probe_signals()
