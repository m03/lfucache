# -*- coding: utf-8 -*-
# vim: ft=python
"""
lfucache.lfulib
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A quick implementation of Least Frequently Used leveraging collections.deque.
"""
# Import python libs.
from __future__ import absolute_import
from collections import deque
import logging
import numbers

# Import from local project.
from lfucache.exceptions import (
    InvalidItemException,
    LFUCacheException,
)


_LOGGER = logging.getLogger(__name__)

_NOT_FOUND = -1


class LFUCache:
    """ The Least Frequently Used cache """

    __slots__ = ['max_items', 'item_count', 'items', 'frequency']

    def __init__(self, max_items):
        if max_items < 1:
            raise LFUCacheException('Invalid maximum item count: {}'.format(max_items))

        self.max_items = max_items
        self.item_count = 0
        self.items = dict()
        self.frequency = dict()


    @staticmethod
    def _validate_item(key, value):
        """
        Verify that the key-value pair does not contain invalid data.

        :param int key: The cache key.
        :param int value: The value for the given key.

        :return: None
        :rtype: None
        """
        if not isinstance(key, numbers.Integral) or key < 1:
            raise InvalidItemException('Invalid key: {}'.format(key))
        if not isinstance(value, numbers.Integral) or value < 1:
            raise InvalidItemException('Invalid value: {}'.format(value))


    def get(self, key):
        """
        Get the value of the provided key from the cache.

        :param int key: The cache key.

        :return: The value of the given key in cache.
        :rtype: int
        """
        # The value and the number of times the key has been seen
        # are stored in the items dictionary.
        try:
            value, count = self.items[key]
        except KeyError:
            return _NOT_FOUND

        if count > 0:
            self.frequency[count].remove(key)

            if not self.frequency[count]:
                self.frequency.pop(count)

        count += 1
        if count not in self.frequency:
            self.frequency[count] = deque()

        # Add the key in a position that indicates that it's the
        # newest item in the list.
        self.frequency[count].append(key)
        self.items[key] = (value, count)

        _LOGGER.debug('Item %s value: %s, count: %s', key, value, count)
        return value


    def get_frequency(self):
        """
        Check the item counts and the relative position of the item keys.

        :return: A dictionary of the item counts and the relative position of the item keys.
        :rtype: dict
        """
        return self.frequency


    def peek(self, key):
        """
        Get the value and the current count without incrementing the counter.

        :return: A tuple of the value and the access frequency, or the not found value.
        :rtype: Union[(int, int), int]
        """
        try:
            return self.items[key]
        except KeyError:
            return _NOT_FOUND


    def put(self, key, value):
        """
        Enter the key-value pair into the cache.

        :param int key: The cache key.
        :param int value: The value for the given key.

        :return: None
        :rtype: None
        """
        self._validate_item(key, value)

        if key in self.items:
            self.items[key] = (value, self.items[key][-1])
        else:
            if self.item_count >= self.max_items:
                # Get the lowest frequency count, and then get the oldest item from that group
                # of items. The oldest item will be the leftmost item in the list.
                least_frequent = min(self.frequency)
                oldest_item_key = self.frequency[least_frequent].popleft()

                if not self.frequency[least_frequent]:
                    self.frequency.pop(least_frequent)

                self.items.pop(oldest_item_key)
            else:
                self.item_count += 1

            self.items[key] = (value, 0)

        # Since this is least frequently used and not least frequently retrieved,
        # always count the put as a use and increment the counter.
        self.get(key)
