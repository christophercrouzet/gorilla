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
    
    invalid = 0
    module = 1
    cls = 2
    descriptor = 3  # Functions, methods, and any descriptor.
    
    @classmethod
    def get(cls, object):
        if isinstance(object, types.ModuleType):
            return cls.module
        elif isinstance(object, gorilla._python.CLASS_TYPES):
            return cls.cls
        elif hasattr(object, '__get__'):
            return cls.descriptor
        
        return cls.invalid
