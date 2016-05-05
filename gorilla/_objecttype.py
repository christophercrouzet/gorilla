"""
    gorilla._objecttype
    ~~~~~~~~~~~~~~~~~~~

    Object types recognized by the patching process.

    :copyright: Copyright 2014-2016 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import types

import gorilla._python


INVALID = 0
MODULE = 1
CLASS = 2
DESCRIPTOR = 3


def get(obj):
    """Retrieve the type of the object.

    Only types recognized by the patching process are considered.

    Parameters
    ----------
    obj : object
        Object to check the type of.

    Returns
    -------
    int
        The object type.
    """
    if isinstance(obj, types.ModuleType):
        return MODULE
    elif isinstance(obj, gorilla._python.CLASS_TYPES):
        return CLASS
    elif hasattr(obj, '__get__'):
        # Functions, methods, and any descriptor.
        return DESCRIPTOR

    return INVALID
