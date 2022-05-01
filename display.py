#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from .probe import Probe
from .source import Source
from typing import List


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
        plt.ion()
        self.__fig, self.__ax = plt.subplots()
        self.__ax.set_xlim(0, self.__xlim[1] * dx)
        self.__ax.set_ylim(self.__ylim[0], self.__ylim[1])
        self.__ax.set_xlabel("м")
        self.__ax.grid()
        (self.__yline,) = self.__ax.plot(self.__xlist * dx, np.zeros(self.__xlim[1]))
        return True

    def draw_probes(self, probes: list[Probe], dx: float) -> bool:
        """draw_probes.

        :param probes_position:
        :type probes_position: list
        :rtype: bool
        """
        for probe in probes:
            self.__ax.plot(probe.position * dx, 0, color="red", marker="x")
        return True

    def draw_sources(self, sources: list[Source], dx: float) -> bool:
        """draw_sources.

        :param sources_position:
        :type sources_position: int
        :rtype: bool
        """
        for source in sources:
            self.__ax.plot(source.position * dx, [0], color="black", marker="o")

        return True

    def draw_borders(self, positions: list[float]) -> bool:
        """draw_borders.

        :param positions:
        :rtype: bool
        """
        for position in positions:
            self.__ax.plot(
                [position, position], self.__ylim, color="black", linestyle="--"
            )
        return True

    def stop(self) -> bool:
        """stop.

        :rtype: bool
        """
        plt.ioff()
        return True

    def update_data(self, data: npt.NDArray[np.float64], time: float) -> bool:
        """update_data.

        :param data:
        :type data: np.ndarray
        :param time:
        :type time: int
        :rtype: bool
        """
        self.__yline.set_ydata(data)
        self.__ax.set_title(str(time))
        self.__fig.canvas.draw()
        self.__fig.canvas.flush_events()
        return True
