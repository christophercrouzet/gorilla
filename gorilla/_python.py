"""
    gorilla._python
    ~~~~~~~~~~~~~~~
    
    Compatibility layer for writing code that runs on Python 2 and 3.
    
    Taken from `six <https://pypi.python.org/pypi/six>`_
    by Benjamin Peterson.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import sys
import types


VERSION = sys.version_info
PY2 = VERSION[0] == 2
PY3 = VERSION[0] == 3


if PY3:
    CLASS_TYPES = type,
    STRING_TYPES = str,
    
    def iteritems(dictionary, **kwargs):
        return iter(dictionary.items(**kwargs))
else:
    CLASS_TYPES = (type, types.ClassType)
    STRING_TYPES = basestring,
    
    def iteritems(dictionary, **kwargs):
        return iter(dictionary.iteritems(**kwargs))
