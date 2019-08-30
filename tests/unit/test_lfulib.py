# -*- coding: utf-8 -*-
# vim: ft=python
"""
tests.unit.test_lfulib
"""

from __future__ import absolute_import

# Import 3rd party libs.
import pytest

# Import from local project.
from lfucache.exceptions import InvalidItemException
from lfucache.lfulib import LFUCache

# Import test scaffolding.
from tests.unit.fixtures.all import (
    FREQUENCY,
    NOT_FOUND,
)

# Mark everything here.
pytestmark = pytest.mark.unit


def test_get():
    """
    Test - Use get to return the expected values.
    """
    cache = LFUCache(2)

    assert cache.get(1) == NOT_FOUND

    cache.put(1, 1)
    cache.put(2, 2)

    # Increment the count for 1, moving 2 to least frequently used.
    assert cache.get(1) == 1

    cache.put(3, 3)
    assert cache.get(2) == NOT_FOUND
    assert cache.get(3) == 3

    cache.put(4, 4)
    assert cache.get(1) == NOT_FOUND
    assert cache.get(3) == 3
    assert cache.get(4) == 4


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


def test_peek():
    """
    Test - Check the content without incrementing the counter.
    """
    cache = LFUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    _ = cache.get(1)
    _ = cache.peek(1)
    assert cache.peek(1) == (1, 2)


def test_get_frequency():
    """
    Test - Check the frequency of .
    """
    cache = LFUCache(3)

    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    _ = cache.get(1)

    assert cache.get_frequency() == FREQUENCY
