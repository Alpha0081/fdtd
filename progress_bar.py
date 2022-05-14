#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ProgressBar:
    def __init__(self, output):
        self.__output = output 

    def show(self, current_value, max_value):
        percent = current_value / max_value * 100
        bar = '#' * int(percent) + '-' * (100 - int(percent))
        self.__output.write(f'Progress: |{bar}| {percent:.2f}%')

class ConsoleOutput:
    def write(self, message):
        print(f"\r{message}", end='\r')
