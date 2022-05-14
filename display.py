#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from .probe import Probe
from .source import Source
from typing import List
import pyqtgraph as pg
from random import randint


class Display:
    """Display."""

    def __init__(
        self, x_lim: tuple[int, int], y_lim: tuple[float, float], y_label: str
    ) -> None:
        self.__xlim: tuple[int, int] = x_lim
        self.__ylim: tuple[float, float] = y_lim
        self.__ylabel: str = y_label
        self.__xlist: npt.NDArray[np.float64] = np.arange(self.__xlim[1], dtype=float)

    def activate(self, dx: float) -> bool:
        """activate.

        :rtype: bool
        """
        self.__dx = dx
        self.__plot = pg.plot()
        self.__plot.setXRange(0, self.__xlim[1] * dx)
        self.__plot.setYRange(self.__ylim[0], self.__ylim[1])
        self.__plot.setLabel("bottom", "м")
        self.__plot.showGrid(x=True, y=True)
        self.__curve = self.__plot.plot(pen="y")
        return True

    def draw_probes(self, probes: list[Probe], dx: float) -> bool:
        """draw_probes.

        :param probes_position:
        :type probes_position: list
        :rtype: bool
        """
        for probe in probes:
            self.__plot.plot([probe.position * dx], [0], pen=None, symbol="x")
        return True

    def draw_sources(self, sources: list[Source], dx: float) -> bool:
        """draw_sources.

        :param sources_position:
        :type sources_position: int
        :rtype: bool
        """
        for source in sources:
            self.__plot.plot([source.position * dx], [0], pen=None, symbol="o")
        return True

    def draw_borders(self, positions: list[float]) -> bool:
        """draw_borders.

        :param positions:
        :rtype: bool
        """
        for position in positions:
            self.__plot.plot([position, position], self.__ylim, pen="w")
        return True

    def stop(self) -> bool:
        """stop.

        :rtype: bool
        """
        plt.ioff()
        return True

    def show_probe_signals(self, time_duration, dt, dx, probes) -> bool:
        p = pg.plot()

        p.addLegend()
        for probe in probes:
            p.plot(
                np.arange(probe.time) * dt,
                probe.E,
                name=f"Probe x = {probe.position * dx}",
                pen=(randint(1, 254), randint(1, 254), randint(1, 254)),
            )

        p.setXRange(0, time_duration)
        p.setYRange(-1.1, 1.1)
        p.setLabel("bottom", "Время, с")
        p.setLabel("left", "Ez, В/м")
        p.showGrid(x=True, y=True)

        #  plt.show()
        pg.exec()
        return True

    def draw(self, data, time) -> bool:
        self.__curve.setData(self.__xlist * self.__dx, data)
        self.__plot.setTitle(f"{time:.7g}")
