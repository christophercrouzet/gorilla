"""
    gorilla._objecttype
    ~~~~~~~~~~~~~~~~~~~
    
    Object types recognized by the patching process.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import types

import gorilla._python


INVALID = 0
MODULE = 1
CLASS = 2
DESCRIPTOR = 3


def get(object):
    if isinstance(object, types.ModuleType):
        return MODULE
    elif isinstance(object, gorilla._python.CLASS_TYPES):
        return CLASS
    elif hasattr(object, '__get__'):
        # Functions, methods, and any descriptor.
        return DESCRIPTOR
    
    return INVALID
