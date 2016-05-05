"""
    gorilla._utils
    ~~~~~~~~~~~~~~

    Utility functions for internal use.

    :copyright: Copyright 2014-2016 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import collections
import inspect

import gorilla._constants
import gorilla._objecttype
import gorilla._python


def class_attribute_iterator(cls):
    """Iterate over the attributes of a class that are suitable for patching.

    The search is also done within the base classes.

    Parameters
    ----------
    cls : class
        Class to retrieve the attributes from.

    Yields
    ------
    tuple of (name, attribute)

        name : str
            The name of the attribute found.
        attribute : object
            The attribute found.
    """
    ignore = ('__class__', '__dict__', '__weakref__')
    valid_types = (gorilla._objecttype.CLASS, gorilla._objecttype.DESCRIPTOR)
    bases = (base for base in inspect.getmro(cls)
             if base not in (type, object))
    yielded = set()
    for base in bases:
        for name, attribute in gorilla._python.iteritems(base.__dict__):
            if (name not in ignore and name not in yielded
                    and gorilla._objecttype.get(attribute) in valid_types):
                yield (name, attribute)
                yielded.add(name)


def extension_iterator(obj):
    """Iterate over the extensions nested under an object.

    The object can be a module, a class or a descriptor.

    The search is done recursively.

    Parameters
    ----------
    obj : object
        Object to retrieve the extensions from.

    Yields
    ------
    Extension
        The extensions found.
    """
    underlying = get_underlying_object(obj)
    if hasattr(underlying, gorilla._constants.DECORATOR_DATA):
        data = getattr(underlying, gorilla._constants.DECORATOR_DATA)
        extensions = data.get('extensions', [])
        for extension in extensions:
            yield extension

    if not hasattr(underlying, '__dict__'):
        return
        yield

    valid_types = (gorilla._objecttype.CLASS, gorilla._objecttype.DESCRIPTOR)
    for attribute in underlying.__dict__.values():
        if gorilla._objecttype.get(attribute) in valid_types:
            for extension in extension_iterator(attribute):
                yield extension


def get_decorator_data(obj):
    """Retrieve the data attached by the Gorilla decorators.

    If no data exists, it is being created.

    Parameters
    ----------
    obj : object
        Object to check for any decorated data. Usually a class or
        a descriptor.

    Returns
    -------
    dict
        The data found, mapped to the name of the owning decorator.
    """
    underlying = get_underlying_object(obj)
    if hasattr(underlying, gorilla._constants.DECORATOR_DATA):
        return getattr(underlying, gorilla._constants.DECORATOR_DATA)

    data = {}
    setattr(underlying, gorilla._constants.DECORATOR_DATA, data)
    return data


def get_underlying_object(obj):
    """Retrieve the leaf underlying object of an object.

    The object returned is the most likely to be the one holding the
    correct ``__name__``, ``__doc__``, and others attributes alike.

    This works for wrappers descriptors such as ``classmethod``,
    ``staticmethod``, and ``property``.

    The operation is done recursively until no more underlying objects
    are to be found.

    Parameters
    ----------
    obj : object
        Object to unwrap.

    Returns
    -------
    object
        The leaf underlying object found or the same object otherwise.
    """
    for obj in _underlying_object_iterator(obj):
        pass

    return obj


def is_settings(obj):
    """Check if a given object represents a settings class.

    Settings matched needs to inherit from the class
    `~gorilla.settings.Settings`.

    Parameters
    ----------
    object : object
        Object to check.

    Returns
    -------
    bool
        True if the given object represents a settings class.
    """
    if (isinstance(obj, gorilla._python.CLASS_TYPES)
            and gorilla.settings.Settings in inspect.getmro(obj)):
        return True

    return False


def listify(value, valid=None):
    """Convert a value into a list.

    Useful to ensure that an input argument is always a list even when
    allowing single values to be passed.

    Parameters
    ----------
    value : object
        Value to convert.
    valid : sequence, optional
        Allows certain values to be considered as valid and to
        be preserved.

    Returns
    -------
    list
        The resulting list.

    Examples
    --------
    >>> listify('abc')
    ['abc']
    >>> listify((True, False))
    [True, False]
    >>> listify(None)
    []
    >>> listify(None, valid=(None, ))
    [None]
    """
    if isinstance(value, list):
        return value
    elif (isinstance(value, collections.Iterable)
            and not isinstance(value, gorilla._python.STRING_TYPES)):
        return [item for item in value]
    elif valid is None:
        return [value] if value else []

    return [value] if value or value in valid else []


def uniquify(sequence):
    """Make the elements of a sequence unique while preserving their order.

    Taken from the article `Fastest way to uniqify a list in Python
    <http://www.peterbe.com/plog/uniqifiers-benchmark>`_
    by Peter Bengtsson.

    Parameters
    ----------
    sequence : sequence
        Iterable sequence to uniquify.

    Returns
    -------
    list
        The uniquified sequence.
    """
    seen = set()
    return [item for item in sequence
            if item not in seen and not seen.add(item)]


def _underlying_object_iterator(obj):
    """Iterate recursively through the underlying objects of an object.

    Parameters
    ----------
    obj : object
        Object to unwrap.

    Yields
    ------
    object
        The underlying objects found or the same object otherwise.
    """
    if hasattr(obj, '__func__'):
        obj = obj.__func__
    elif isinstance(obj, property):
        obj = obj.fget
    elif isinstance(obj, (classmethod, staticmethod)):
        # Fallback for Python < 2.7 back when no `__func__` attribute
        # was defined for those descriptors.
        import __builtin__
        obj = obj.__get__(None, __builtin__.object)
    else:
        return
        yield

    yield obj
    for obj in _underlying_object_iterator(obj):
        yield obj
