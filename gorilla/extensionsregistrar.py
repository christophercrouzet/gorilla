"""
    gorilla.extensionsregistrar
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Utility to find and register extensions.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import pkgutil
import sys
import types

import gorilla._python
import gorilla._utils
import gorilla.utils
from gorilla.extensionset import ExtensionSet


class ExtensionsRegistrar(object):
    
    """Registrar for the extensions."""
    
    @classmethod
    def register_extensions(cls, packages_and_modules, patch=False):
        """Scan and register all the extensions found.
        
        The extensions are recursively scanned from the list of packages and
        modules provided.
        
        Parameters
        ----------
        packages_and_modules : list of modules
            List of packages and modules to scan recursively.
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
        
        def register(package_or_module, extension_set):
            extensions = list(gorilla._utils.extension_iterator(
                package_or_module))
            extension_set.extensions.extend(extensions)
            
            # The `__path__` attribute of a package might return a list of
            # paths if the package is referenced as a namespace.
            paths = getattr(package_or_module, '__path__', None)
            if not paths:
                return
            
            packages = []
            paths = gorilla.utils.uniquify(gorilla.utils.listify(paths))
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
                        # Breadth-first traversal, recurse over the subpackages
                        # only after having processed the modules at the
                        # current level.
                        packages.append(module)
                    else:
                        register(module, extension_set)
            
            for package in packages:
                register(package, extension_set)
        
        
        extension_set = ExtensionSet()
        modules = gorilla.utils.uniquify(gorilla.utils.listify(
            packages_and_modules))
        for module in modules:
            if not isinstance(module, types.ModuleType):
                raise TypeError(
                    "The path '%s' isn't a valid package or module." % module)
            
            register(module, extension_set)
        
        if patch:
            extension_set.patch()
        
        return extension_set