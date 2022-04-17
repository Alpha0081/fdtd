#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from constants import W_0, c
from display import Display
from layer import Layer
from probe import Probe
from source import Source


class FDTD:
    def __init__(
        self, field_size: float, space_step: float, time_duration: float, Sc: float
    ) -> None:
        self.__dx: float = space_step
        self.__Sc: float = Sc
        self.__field_size: int = int(field_size // self.__dx)
        self.__time_duration: float = time_duration
        self.__dt: float = self.__dx * self.__Sc / c
        self.__time_counts: int = int(self.__time_duration // self.__dt)
        self.__E: npt.NDArray[np.float64] = np.zeros(self.__field_size)
        self.__H: npt.NDArray[np.float64] = np.zeros(self.__field_size - 1)
        self.__eps: npt.NDArray[np.float64] = np.ones(self.__field_size)
        self.__sigma: npt.NDArray[np.float64] = np.zeros(self.__field_size)
        self.__mu: npt.NDArray[np.float64] = np.ones(self.__field_size - 1)
        self.__boundary: List[int] = []
        self.__display: Display = Display((0, self.__field_size), (-1.1, 1.1), "Ez В/м")
        self.__display.activate(self.__dx)
        self.__sources: List[Source] = []
        self.__probes: List[Probe] = []
        self.__layers: list[Layer] = []

    def analyze(self) -> bool:
        self.__display.draw_probes(self.__probes, self.__dx)
        self.__display.draw_boundary(self.__boundary)
        self.__display.draw_sources(self.__sources, self.__dx)

        ceze = (1 - self.__sigma) / (1 + self.__sigma)
        cezh = W_0 / (self.__eps * (1 + self.__sigma))

        for q in range(self.__time_counts):
            self.__H = self.__H + (self.__E[1:] - self.__E[:-1]) * self.__Sc / (
                W_0 * self.__mu
            )
            for source in self.__sources:
                self.__H[source.position - 1] -= (
                    self.__Sc / (W_0 * self.__mu[source.position - 1]) * source.E(0, q)
                )

            self.__E[1:-1] = (
                ceze[1:-1] * self.__E[1:-1]
                + (self.__H[1:] - self.__H[:-1]) * self.__Sc * cezh[1:-1]
            )

            for source in self.__sources:
                self.__E[source.position] += (
                    self.__Sc
                    / (self.__eps[source.position] * self.__mu[source.position]) ** 0.5
                    * source.E(-0.5, (q + 0.5))
                )

            for probe in self.__probes:
                probe.update_data(self.__E, self.__H)

            if not q % 3:
                self.__display.update_data(self.__E, q * self.__dt)
                self.__display.stop()
        return True

    def show_probe_signals(self) -> bool:
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
        if issubclass(type(sources), Source):
            sources.position = int(sources.position // self.__dx)
            sources.eps = self.__eps[sources.position]
            sources.mu = self.__mu[sources.position]
            sources.Sc = self.__Sc
            sources.dt = self.__dt
            self.__sources.append(sources)
        elif type(sources) == list:
            for source in sources:
                source.position = int(source.position // self.__dx)
                source.eps = self.__eps[sources.position]
                source.mu = self.__mu[sources.position]
                source.Sc = self.__Sc
                source.dt = self.__dt
                self.__sources.append(source)
        return True

    def add_layer(self, layer: Layer) -> bool:
        layer.name = "Layer" + str(len(self.__layers))
        self.__layers.append(layer)
        begin, end = int(layer.field[0] / self.__dx), int(layer.field[1] / self.__dx)
        self.__eps[begin:end] = layer.eps
        self.__mu[begin:end] = layer.mu
        self.__sigma[begin:end] = layer.sigma
        self.__boundary.append(layer.field[0])
        self.__boundary.append(layer.field[1])
        return True

    def delete_layer(self, name: str) -> bool:
        for i, layer in enumerate(self.__layers):
            if layer.name == name:
                begin, end = int(layer.field[0] / self.__dx), int(
                    layer.field[1] / self.__dx
                )
                self.__eps[begin:end] = 1
                self.__mu[begin:end] = 1
                self.__sigma[begin:end] = 0
                self.__boundary.pop(2 * i + 1)
                self.__boundary.pop(2 * i)
                self.__layers.pop(i)
                break
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
