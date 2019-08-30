# -*- coding: utf-8 -*-
# vim: ft=python

"""
Pytest fixtures for all lfulib tests.
"""
# Import Python Libs.
from __future__ import absolute_import
from collections import deque

# Imports to others.
__all__ = []

FREQUENCY = {
    1: deque([2, 3]),
    2: deque([1]),
}

NOT_FOUND = -1
