#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BoundaryTypeError(Exception):
    def __str__(self):
        return "Not valid boundary type"
