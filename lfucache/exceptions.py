# -*- coding: utf-8 -*-
# vim: ft=python
"""
lfucache.exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All the exceptions specific to this package.

"""

class LFUCacheException(Exception):
    """ Parent for all exceptions in this package """


class InvalidItemException(LFUCacheException):
    """ The item key or value does not pass validation """
