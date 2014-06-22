"""
    gorilla.utils
    ~~~~~~~~~~~~~
    
    Utility functions.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import collections

import gorilla._constants
import gorilla._python


def get_original_attribute(object, name):
    """Retrieve an attribute overriden during the patching process.
    
    This method can be accessed from within an overriding function to call
    the original attribute and preserve the intended behavior.
    
    Parameters
    ----------
    object : object
        Object owning the attribute to look for.
    name : str
        Name of the attribute to look for.
    
    Returns
    -------
    object
        The attribute found, None otherwise.
    """
    return getattr(object, gorilla._constants.ORIGINAL % name, None)


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
    elif (isinstance(value, collections.Iterable) and
            not isinstance(value, gorilla._python.STRING_TYPES)):
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
