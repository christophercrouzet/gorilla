"""
    gorilla.utils
    ~~~~~~~~~~~~~

    Utility functions.

    :copyright: Copyright 2014-2016 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import pkgutil
import sys
import types

import gorilla._constants
import gorilla._python
import gorilla._utils


def get_original_attribute(obj, name):
    """Retrieve an attribute overriden during the patching process.

    This method can be accessed from within an overriding function to call
    the original attribute and preserve the intended behavior.

    Parameters
    ----------
    obj : object
        Object owning the attribute to look for.
    name : str
        Name of the attribute to look for.

    Returns
    -------
    object
        The attribute found, None otherwise.
    """
    return getattr(obj, gorilla._constants.ORIGINAL % name, None)


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
    [list of] gorilla.extension.Extension
        Extensions found.

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

    def register(extensions, package_or_module, settings):
        local_extensions = list(
            gorilla._utils.extension_iterator(package_or_module))
        if settings:
            for extension in local_extensions:
                if extension.settings:
                    # Make sure that settings directly defined at the
                    # extension level overwrite the global settings.
                    compiled_settings = settings.copy()
                    compiled_settings.update(extension.settings)
                    extension.settings = compiled_settings
                else:
                    extension.settings = settings.copy()

        extensions.extend(gorilla._utils.listify(local_extensions))

        # The `__path__` attribute of a package might return a list of
        # paths if the package is referenced as a namespace.
        paths = getattr(package_or_module, '__path__', None)
        if not paths:
            return

        packages = []
        paths = gorilla._utils.uniquify(gorilla._utils.listify(paths))
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
                    register(extensions, module, settings)

        for package in packages:
            register(extensions, package, settings)

    if gorilla._utils.is_settings(settings):
        settings = settings.as_dict()

    extensions = []
    modules = gorilla._utils.uniquify(gorilla._utils.listify(
        packages_and_modules))
    for module in modules:
        if not isinstance(module, types.ModuleType):
            raise TypeError(
                "The path '%s' isn't a valid package or module." % module)

        register(extensions, module, settings)

    if patch:
        for extension in extensions:
            extension.patch()

    return extensions
