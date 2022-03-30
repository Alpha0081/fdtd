#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


class Display:
    """Display."""

    def __init__(self, x_lim: tuple, y_lim: tuple, y_label: str) -> None:
        self.__xlim = x_lim
        self.__ylim = y_lim
        self.__ylabel = y_label
        self.__xlist = np.arange(self.__xlim[1])

    def activate(self, dx) -> bool:
        """activate.

        :rtype: bool
        """
        plt.ion()
        self.__fig, self.__ax = plt.subplots()
        self.__ax.set_xlim(0, self.__xlim[1] * dx)
        self.__ax.set_ylim(self.__ylim)
        self.__ax.set_xlabel("м")
        self.__ax.grid()
        (self.__yline,) = self.__ax.plot(
            self.__xlist * dx, np.zeros(self.__xlim[1])
        )
        return True

    def draw_probes(self, probes: list, dx: float) -> bool:
        """draw_probes.

        :param probes_position:
        :type probes_position: list
        :rtype: bool
        """
        for probe in probes:
            self.__ax.plot(probe.position * dx, 0, "xr")
        return True

    def draw_sources(self, sources, dx) -> bool:
        """draw_sources.

        :param sources_position:
        :type sources_position: int
        :rtype: bool
        """
        for source in sources:
            self.__ax.plot(source.position * dx, [0], "ok")
        return True

    def draw_boundary(self, positions) -> bool:
        """draw_boundary.

        :param positions:
        :rtype: bool
        """
        for position in positions:
            self.__ax.plot(
                [position, position], self.__ylim, "--k"
            )

    def stop(self) -> bool:
        """stop.

        :rtype: bool
        """
        plt.ioff()
        return True

    def update_data(self, data: np.ndarray, time: int) -> bool:
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



