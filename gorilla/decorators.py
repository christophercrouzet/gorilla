"""
    gorilla.decorators
    ~~~~~~~~~~~~~~~~~~
    
    Decorators to control how to patch some external code.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla._constants
import gorilla._utils
from gorilla.extension import Extension


def patch(target, name='', apply=None):
    """Decorator to mark an object to use as a patch for a specified target.
    
    Parameters
    ----------
    target : object
        Target where to patch the decorated object.
        Usually a module or a class.
    name : str, optional
        Name for the resulting attribute. Defaults to the actual name of
        the decorated object when not provided.
    apply : callable or list of callables, optional
        Callable objects to apply during the patching process.
    
    Returns
    -------
    object
        The decorated object.
    
    Examples
    --------
    The two following examples achieve the same result.
    
    >>> import gorilla
    >>> from gorilla.utils import get_original_attribute
    >>> import guineapig
    >>> @gorilla.patch(guineapig, name='GuineaPig')
    ... class Needle(object):
    ...     def needle(self, arg):
    ...         print("awesome")
    ...         # We're overriding an existing method here,
    ...         # preserve its original behavior.
    ...         return get_original_attribute(self, 'needle')(arg)
    ...     
    ...     @staticmethod
    ...     def static_needle():
    ...         print("awesome")
    
    Here, the entire content of the class ``Needle`` is patched in the
    target module ``guineapig``. We make sure that ``Needle``
    overrides the existing class ``guineapig.GuineaPig`` by
    providing an explicit name.
    
    >>> import gorilla
    >>> from guineapig import GuineaPig
    >>> @gorilla.patch(GuineaPig)
    ... def needle(self, arg):
    ...     print("awesome")
    ...     # We're overriding an existing method here,
    ...     # preserve its original behavior.
    ...     return get_original_attribute(self, 'needle')(arg)
    ...
    ... @gorilla.patch(GuineaPig, apply=staticmethod)
    ... def static_needle(arg):
    ...     print("awesome")
    
    While here, each attribute is patched individually into the class
    ``guineapig.GuineaPig``. We need to pass the ``staticmethod`` to the
    list of callables to apply otherwise the function ``static_needle()``
    would have been added as a method and would have raised an exception
    upon calling because of the missing first argument referring to its
    self instance.
    
    See Also
    --------
    `~gorilla.extension.Extension`
    """
    def decorator(wrapped):
        extension = Extension(wrapped, target, name=name, apply=apply)
        data = gorilla._utils.get_decorator_data(wrapped)
        data.setdefault('extensions', []).insert(0, extension)
        return wrapped
    
    return decorator


def name(value):
    """Decorator to override the patching name.
    
    When using an entire class for being used as a patch, this allows to
    define the name of each individual class member. The default class
    attribute name are otherwise used.
    
    This decorator can also applied on top of a `patch` decorator, in
    which case it will override its name value.
    
    Parameters
    ----------
    value : str
        Name for the patching object.
    
    Returns
    -------
    object
        The decorated object.
    
    Examples
    --------
    >>> import gorilla
    >>> import guineapig
    >>> @gorilla.patch(guineapig, name='GuineaPig')
    ... class Needle(object):
    ...     @gorilla.name('needle')
    ...     def my_function(self):
    ...         print("awesome")
    """
    def decorator(wrapped):
        data = gorilla._utils.get_decorator_data(wrapped)
        extensions = data.get('extensions', None)
        if extensions:
            extensions[0].name = value
        else:
            data['name'] = value
        
        return wrapped
    
    return decorator


def apply(*args, **kwargs):
    """Decorator to dynamically apply callable objects.
    
    When using an entire class for being used as a patch, this allows to
    define additional callable objects to be applied dynamically on each
    individual class member at runtime.
    
    Any decorator such as ``classmethod`` or ``staticmethod`` already
    statically defined will be taken into consideration during the patching
    process and shouldn't be applied again through this decorator.
    
    By default, this decorator will override any previous list of objects
    to apply but this is also possible to append or prepend to the list by
    using the corresponding keyword argument.
    
    Callable objects at the front of the list are to be applied last as if
    they were on top of attributes decorator stack.
    
    This decorator can also applied on top of a `patch` operator, in which
    case it will update its list of callable objects to apply.
    
    Parameters
    ----------
    args
        Variable number of callable objects to apply.
    kwargs
        Optional keyword arguments to define the type of insertion. If
        the keywords `append` or `prepend` are found, this will accordingly
        insert the objects into the list of callables to apply. Otherwise,
        the list of callables will be replaced with the objects defined in
        `*args`.
    
    Returns
    -------
    object
        The decorated object.
    
    Raises
    ------
    ValueError
        Both the `append` and `prepend` keywords have been passed.
    
    Examples
    --------
    >>> import gorilla
    >>> import guineapig
    >>> import my_decorator_module
    >>> @gorilla.patch(guineapig, name='GuineaPig')
    ... class Needle(object):
    ...     @gorilla.apply(my_decorator_module.decorator, prepend=True)
    ...     def needle(self):
    ...         print("awesome")
    """
    if all(key in kwargs for key in ('append', 'prepend')):
        raise ValueError("Choose if you want to either append or prepend to "
                         "any existing list.")
    
    def decorator(wrapped):
        data = gorilla._utils.get_decorator_data(wrapped)
        extensions = data.get('extensions', None)
        if extensions:
            callable_list = extensions[0].apply
        else:
            callable_list = data.setdefault('apply', [])
        
        if 'append' in kwargs:
            callable_list.extend(args)
        elif 'prepend' in kwargs:
            callable_list[:0] = args
        else:
            callable_list[:] = args
        
        return wrapped
    
    return decorator
