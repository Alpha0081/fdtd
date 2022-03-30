#!/usr/bin/env python
# -*- coding: utf-8 -*-

from display import Display
from constants import c, W_0
import matplotlib.pyplot as plt
import numpy as np
from probe import Probe
from source import Source


class FDTD:
    def __init__(
        self, field_size: float, space_step: float, time_duration: float, Sc: float
    ) -> None:
        self.__dx = space_step
        self.__Sc = Sc
        self.__field_size = int(field_size // self.__dx)
        self.__time_duration = time_duration
        self.__dt = self.__dx * self.__Sc / c
        self.__time_counts = int(self.__time_duration // self.__dt)
        self.__E = np.zeros(self.__field_size)
        self.__H = np.zeros(self.__field_size - 1)
        self.__eps = np.ones(self.__field_size)
        self.__mu = np.ones(self.__field_size - 1)
        self.__boundary = []
        self.__display = Display([0, self.__field_size], [-1.1, 1.1], "Ez В/м")
        self.__display.activate(self.__dx)
        self.__sources: list = []
        self.__probes: list = []

    def analyze(self) -> bool:
        self.__display.draw_probes(self.__probes, self.__dx)
        self.__display.draw_boundary(self.__boundary)
        self.__display.draw_sources(self.__sources, self.__dx)
        for q in range(self.__time_counts):
            self.__H = self.__H + (self.__E[1:] - self.__E[:-1]) * self.__Sc / (
                W_0 * self.__mu
            )
            for source in self.__sources:
                self.__H[source.position - 1] -= (
                    self.__Sc
                    / (W_0 * self.__mu[source.position - 1])
                    * source.E(0, q)
                )

            self.__E[1:-1] = (
                self.__E[1:-1]
                + (self.__H[1:] - self.__H[:-1]) * self.__Sc * W_0 / self.__eps[1:-1]
            )

            for source in self.__sources:
                self.__E[source.position] += (
                    self.__Sc
                    / (self.__eps[source.position] * self.__mu[source.position]) ** .5
                    * source.E(-.5, (q + .5))
                )
                print(source.E(-.5, (q + .5)))

            for probe in self.__probes:
                probe.update_data(self.__E, self.__H)

            if not q % 2:
                self.__display.update_data(self.__E, q * self.__dt)
                self.__display.stop()
        return True

    def showProbeSignals(self):
        fig, ax = plt.subplots()

        ax.set_xlim(0, self.__dt * self.__time_counts)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlabel("Время, с")
        ax.set_ylabel("Ez, В/м")
        ax.grid()

        for probe in self.__probes:
            ax.plot(np.arange(probe.time) * self.__dt, probe.E)

        legend = [
            "Probe x = {}".format(probe.position * self.__dx) for probe in self.__probes
        ]
        ax.legend(legend)
        plt.show()
        return True

    def add_probes(self, probes_position) -> bool:
        if type(probes_position) == int:
            self.__probes.append(
                Probe(int(probes_position // self.__dx), self.__time_counts)
            )
        elif type(probes_position) == list:
            for probe_position in probes_position:
                self.__probes.append(
                    Probe(int(probe_position // self.__dx), self.__time_counts)
                )
        return True

    def add_source(self, sources) -> bool:
        if type(sources) == Source:
            sources.position = int(sources.position // self.__dx)
            self.__sources.append(sources)
        elif type(sources) == list:
            for source in sources:
                source.position = int(source.position // self.__dx)
                self.__sources.append(source)
        return True

    def set_eps(self, field: tuple, eps: float) -> bool:
        self.__eps[int(field[0] // self.__dx):int(field[1] // self.__dx)] = eps
        self.__boundary.append(field[0])
        self.__boundary.append(field[1])
        return True

    @property
    def Sc(self) -> float:
        return self.__Sc

    @property
    def dt(self) -> float:
        return self.__dt

    @property
    def dx(self) -> float:
        return self.__dx

    @property
    def mu(self) -> np.ndarray:
        return self.__mu

    @property
    def eps(self) -> np.ndarray:
        return self.__eps
