# -*- coding: utf-8 -*-
"""
tests.unit.test_lfulib
"""

from __future__ import absolute_import

# Import 3rd party libs.
import pytest

# Import from local project.
from lfucache.lfulib import InvalidItemException, LFUCache


def test_get():
    """
    Test - Use get to return the expected values.
    """
    cache = LFUCache(2)

    assert cache.get(1) == -1

    cache.put(1, 1)
    cache.put(2, 2)

    # Increment the count for 1, moving 2 to least frequently used.
    assert cache.get(1) == 1

    cache.put(3, 3)
    assert cache.get(2) == -1


def test_put_failed():
    """
    Test - Use put to check the expected functionality.
    """
    cache = LFUCache(1)

    with pytest.raises(InvalidItemException):
        cache.put('invalid key', 1)
    with pytest.raises(InvalidItemException):
        cache.put(1, 'invalid value')
    with pytest.raises(InvalidItemException):
        cache.put(-1, -1)
