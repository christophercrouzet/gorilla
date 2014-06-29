import unittest
import sys

from gorilla.extension import Extension
from gorilla.extensionsregistrar import ExtensionsRegistrar

from . import data_extensionsregistrar
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
        extension1_method = Extension(extension1.method, guineapig.GuineaPig)
        extension1_method.name = 'needle_method'
        extension1_class_method = Extension(extension1.class_method, guineapig.GuineaPig)
        extension1_class_method.name = 'needle_class_method'
        extension1_class_method.apply = classmethod
        extension1_static_method = Extension(extension1.static_method, guineapig.GuineaPig)
        extension1_static_method.name = 'needle_static_method'
        extension1_static_method.apply = staticmethod
        extension1_value = Extension(extension1.value, guineapig.GuineaPig)
        extension1_value.name = 'needle_value'
        extension1_value.apply = property
        extension2_class = Extension(extension2.Class, guineapig)
        extension2_class.name = 'Needle'
        submodule_method = Extension(submodule.Class.__dict__['method'], guineapig.GuineaPig)
        submodule_method.name = 'needle_method'
        
        extensions = [extension1_method, extension1_class_method, extension1_static_method, extension1_value, extension2_class, submodule_method]
        
        extension_set = ExtensionsRegistrar.register_extensions(packages_and_modules=rootmodule)
        self.assert_true(_same_list_content(extension_set.extensions, extensions))
    
    def test_register_extensions_2(self):
        extension2_class = Extension(extension2.Class, guineapig)
        extension2_class.name = 'Needle'
        submodule_method = Extension(submodule.Class.__dict__['method'], guineapig.GuineaPig)
        submodule_method.name = 'needle_method'
        
        extensions = [extension2_class, submodule_method]
        
        extension_set = ExtensionsRegistrar.register_extensions(packages_and_modules=[submodule, extension2])
        self.assert_true(_same_list_content(extension_set.extensions, extensions))
    
    def test_register_extensions_3(self):
        extension1_method = Extension(extension1.method, guineapig.GuineaPig)
        extension1_method.name = 'needle_method'
        extension1_class_method = Extension(extension1.class_method, guineapig.GuineaPig)
        extension1_class_method.name = 'needle_class_method'
        extension1_class_method.apply = classmethod
        extension1_static_method = Extension(extension1.static_method, guineapig.GuineaPig)
        extension1_static_method.name = 'needle_static_method'
        extension1_static_method.apply = staticmethod
        extension1_value = Extension(extension1.value, guineapig.GuineaPig)
        extension1_value.name = 'needle_value'
        extension1_value.apply = property
        extension2_class = Extension(extension2.Class, guineapig)
        extension2_class.name = 'Needle'
        
        extensions = [extension1_method, extension1_class_method, extension1_static_method, extension1_value, extension2_class]
        
        extension_set = ExtensionsRegistrar.register_extensions(packages_and_modules=[rootmodule], recursive=False)
        self.assert_true(_same_list_content(extension_set.extensions, extensions))
    
    def test_register_extensions_4(self):
        settings = {'allow_overwriting': True, 'update_class': False}
        
        extension1_method = Extension(extension1.method, guineapig.GuineaPig)
        extension1_method.name = 'needle_method'
        extension1_method.settings = settings
        extension1_class_method = Extension(extension1.class_method, guineapig.GuineaPig)
        extension1_class_method.name = 'needle_class_method'
        extension1_class_method.apply = classmethod
        extension1_class_method.settings = settings
        extension1_static_method = Extension(extension1.static_method, guineapig.GuineaPig)
        extension1_static_method.name = 'needle_static_method'
        extension1_static_method.apply = staticmethod
        extension1_static_method.settings = settings
        extension1_value = Extension(extension1.value, guineapig.GuineaPig)
        extension1_value.name = 'needle_value'
        extension1_value.apply = property
        extension1_value.settings = settings
        extension2_class = Extension(extension2.Class, guineapig)
        extension2_class.name = 'Needle'
        extension2_class.settings = settings
        submodule_method = Extension(submodule.Class.__dict__['method'], guineapig.GuineaPig)
        submodule_method.name = 'needle_method'
        submodule_method.settings = settings
        
        extensions = [extension1_method, extension1_class_method, extension1_static_method, extension1_value, extension2_class, submodule_method]
        
        extension_set = ExtensionsRegistrar.register_extensions(packages_and_modules=rootmodule, settings=data_extensionsregistrar.ExtensionsSettings)
        self.assert_true(_same_list_content(extension_set.extensions, extensions))


if __name__ == '__main__':
    unittest.main()
