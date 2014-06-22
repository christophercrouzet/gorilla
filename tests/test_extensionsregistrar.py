from __future__ import print_function

import unittest
import sys

from gorilla.extension import Extension
from gorilla.extensionsregistrar import ExtensionsRegistrar

from .data_extensionsregistrar import guineapig
from .data_extensionsregistrar import extensions as rootmodule
from .data_extensionsregistrar.extensions import extension1, extension2
from .data_extensionsregistrar.extensions.subpackage import extension as submodule
from . import GorillaTestCase


def _same_list_content(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    
    for item_1 in list_1:
        for item_2 in list_2:
            if (item_1.__dict__ == item_2.__dict__ and
                    item_1.name == item_2.name and
                    item_1.original == item_2.original):
                break
        else:
            return False
    
    return True


class ExtensionsRegistrarTest(GorillaTestCase):
    
    def setup(self):
        global guineapig
        global rootmodule
        global extension1
        global extension2
        global submodule
        guineapig = __import__('data_extensionsregistrar.guineapig', globals(), locals(), ['*'], 1)
        rootmodule = __import__('data_extensionsregistrar.extensions', globals(), locals(), ['*'], 1)
        extension1 = __import__('data_extensionsregistrar.extensions.extension1', globals(), locals(), ['*'], 1)
        extension2 = __import__('data_extensionsregistrar.extensions.extension2', globals(), locals(), ['*'], 1)
        submodule = __import__('data_extensionsregistrar.extensions.subpackage.extension', globals(), locals(), ['*'], 1)
    
    def teardown(self):
        global guineapig
        global rootmodule
        global extension1
        global extension2
        global submodule
        del sys.modules[submodule.__name__]
        del sys.modules[extension2.__name__]
        del sys.modules[extension1.__name__]
        del sys.modules[rootmodule.__name__]
        del sys.modules[guineapig.__name__]
    
    def test_register_extensions_1(self):
        extensions = [
            Extension(extension1.method, guineapig.GuineaPig, name="needle_method"),
            Extension(extension1.class_method, guineapig.GuineaPig, name="needle_class_method", apply=classmethod),
            Extension(extension1.static_method, guineapig.GuineaPig, name="needle_static_method", apply=staticmethod),
            Extension(extension1.value, guineapig.GuineaPig, name="needle_value", apply=property),
            Extension(extension2.Class, guineapig, name="Needle"),
            Extension(submodule.Class.__dict__['method'], guineapig.GuineaPig, name="needle_method")
        ]
        
        extension_sets = ExtensionsRegistrar.register_extensions(packages_and_modules=rootmodule)
        registered_extensions = [extension for extension_set in extension_sets for extension in extension_set.extensions]
        self.assert_true(_same_list_content(registered_extensions, extensions))
    
    def test_register_extensions_2(self):
        extensions = [
            Extension(extension2.Class, guineapig, name="Needle"),
            Extension(submodule.Class.__dict__['method'], guineapig.GuineaPig, name="needle_method")
        ]
        
        extension_sets = ExtensionsRegistrar.register_extensions(packages_and_modules=[submodule, extension2])
        registered_extensions = [extension for extension_set in extension_sets for extension in extension_set.extensions]
        self.assert_true(_same_list_content(registered_extensions, extensions))


if __name__ == '__main__':
    unittest.main()
