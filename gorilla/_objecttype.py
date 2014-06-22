"""
    gorilla._objecttype
    ~~~~~~~~~~~~~~~~~~~
    
    Object types recognized by the patching process.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import types

import gorilla._python


class ObjectType(object):
    
    INVALID = 0
    MODULE = 1
    CLASS = 2
    DESCRIPTOR = 3  # Functions, methods, and any descriptor.
    
    @classmethod
    def get(cls, object):
        if isinstance(object, types.ModuleType):
            return cls.MODULE
        elif isinstance(object, gorilla._python.CLASS_TYPES):
            return cls.CLASS
        elif hasattr(object, '__get__'):
            return cls.DESCRIPTOR
        
        return cls.INVALID
