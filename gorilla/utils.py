"""
    gorilla.utils
    ~~~~~~~~~~~~~
    
    Utility functions.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import collections
import pkgutil
import sys
import types

import gorilla._constants
import gorilla._python
import gorilla._utils
import gorilla.settings
from gorilla.extensionset import ExtensionSet


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


def register_extensions(packages_and_modules, settings=None,
                        recursive=True, patch=False):
    """Scan and register all the extensions found.
    
    Parameters
    ----------
    packages_and_modules : [list of] module
        Package(s) and/or module(s) to scan recursively.
    settings : dict or gorilla.settings.Settings, optional
        Settings to apply to all the extensions found. Any setting
        already existing on the extension level won't be overridden.
    recursive : bool, optional
        True to recursively scan for extensions in subpackages.
    patch : bool, optional
        True to also apply the patches.
    
    Returns
    -------
    gorilla.extensionset.ExtensionSet
        Extensions found grouped within an extension set.
    
    Raises
    ------
    TypeError
        The input is not a valid package or module.
    """
    if gorilla._python.PY3:
        def load_module(finder, name):
            loader, _ = finder.find_loader(name)
            return loader.load_module()
    else:
        def load_module(finder, name):
            loader = finder.find_module(name)
            return loader.load_module(name)
    
    def register(package_or_module, extension_set, settings):
        extensions = list(
            gorilla._utils.extension_iterator(package_or_module))
        if settings:
            for extension in extensions:
                if extension.settings:
                    # Make sure that settings directly defined at the
                    # extension level overwrite the global settings.
                    compiled_settings = settings.copy()
                    compiled_settings.update(extension.settings)
                    extension.settings = compiled_settings
                else:
                    extension.settings = settings.copy()
        
        extension_set.add(extensions)
        
        # The `__path__` attribute of a package might return a list of
        # paths if the package is referenced as a namespace.
        paths = getattr(package_or_module, '__path__', None)
        if not paths:
            return
        
        packages = []
        paths = uniquify(listify(paths))
        for path in paths:
            modules = pkgutil.iter_modules([path])
            for finder, name, is_package in modules:
                module_name = "%s.%s" % (package_or_module.__name__, name)
                module = sys.modules.get(module_name, None)
                if not module:
                    # Import the module through the finder rather than with
                    # the `__builtin__` function to support package
                    # namespaces.
                    module = load_module(finder, module_name)
                
                if is_package:
                    if recursive:
                        # Breadth-first traversal, recurse over the
                        # subpackages only after having processed the
                        # modules at the current level.
                        packages.append(module)
                else:
                    register(module, extension_set, settings)
        
        for package in packages:
            register(package, extension_set, settings)
    
    
    if gorilla._utils.is_settings(settings):
        settings = settings.as_dict()
    
    extension_set = ExtensionSet()
    modules = uniquify(listify(packages_and_modules))
    for module in modules:
        if not isinstance(module, types.ModuleType):
            raise TypeError(
                "The path '%s' isn't a valid package or module." % module)
        
        register(module, extension_set, settings)
    
    if patch:
        extension_set.patch()
    
    return extension_set


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
