#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BoundaryTypeError(Exception):
    def __str__(self):
        return "Not valid boundary type"

class AreaSizeError(Exception):
    def __str__(self):
        return "Area size less than or equal to 0"

class SpaceStepError(Exception):
    def __str__(self):
        return "Space step is greater than area size"

class ScValueError(Exception):
    def __str__(self):
        return "Sc less than or equal 0"

class TimeDurationError(Exception):
    def __str__(self):
        return "Time duration less than or equal to 0"

class TimeStepError(Exception):
    def __str__(self):
        return "Time step is greater than time duration"
