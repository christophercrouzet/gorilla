import sys
import unittest

import gorilla._python
import gorilla._utils
import gorilla.utils
from gorilla.extension import Extension

from . import data_utils
from .data_utils import data, guineapig
from .data_utils import extensions as rootmodule
from .data_utils.extensions import extension1, extension2
from .data_utils.extensions.subpackage import extension as submodule
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


class UtilsTest(GorillaTestCase):
    
    def setup(self):
        global data
        global guineapig
        global rootmodule
        global extension1
        global extension2
        global submodule
        guineapig = __import__('data_utils.guineapig', globals(), locals(), ['*'], 1)
        data = __import__('data_utils.data', globals(), locals(), ['*'], 1)
        rootmodule = __import__('data_utils.extensions', globals(), locals(), ['*'], 1)
        extension1 = __import__('data_utils.extensions.extension1', globals(), locals(), ['*'], 1)
        extension2 = __import__('data_utils.extensions.extension2', globals(), locals(), ['*'], 1)
        submodule = __import__('data_utils.extensions.subpackage.extension', globals(), locals(), ['*'], 1)
        self.sys_path = list(sys.path)
    
    def teardown(self):
        global data
        global guineapig
        global rootmodule
        global extension1
        global extension2
        global submodule
        del sys.modules[submodule.__name__]
        del sys.modules[extension2.__name__]
        del sys.modules[extension1.__name__]
        del sys.modules[rootmodule.__name__]
        del sys.modules[data.__name__]
        del sys.modules[guineapig.__name__]
        sys.path[:] = self.sys_path
    
    def test_class_attribute_iterator(self):
        object = data.EmptyClass
        attributes = []
        self.assert_equal(list(gorilla._utils.class_attribute_iterator(object)), attributes)
        
        object = data.Class
        attributes = [
            ('__init__', object.__dict__['__init__']),
            ('__str__', object.__dict__['__str__']),
            ('__eq__', object.__dict__['__eq__']),
            ('method', object.__dict__['method']),
            ('class_method', object.__dict__['class_method']),
            ('static_method', object.__dict__['static_method']),
            ('property', object.__dict__['property'])
        ]
        self.assert_equal(list(gorilla._utils.class_attribute_iterator(object)).sort(), attributes.sort())
        
        object = data.DerivedClass
        base = data.Class
        attributes = [
            ('method', object.__dict__['method']),
            ('derived', object.__dict__['derived']),
            ('class_method', base.__dict__['class_method']),
            ('static_method', base.__dict__['static_method']),
            ('property', base.__dict__['property'])
        ]
        self.assert_equal(list(gorilla._utils.class_attribute_iterator(object)).sort(), attributes.sort())
    
    def test_extension_iterator(self):
        extensions = [
            Extension(data.decorated_function, guineapig),
            Extension(data.DecoratedClass, guineapig),
            Extension(data.DecoratedClass.__dict__['decorated_method'], guineapig.GuineaPig),
            Extension(data.UndecoratedClass.UndecoratedInnerClass.__dict__['decorated_method'], guineapig.GuineaPig.InnerClass),
            Extension(data.UndecoratedClass.DecoratedInnerClass, guineapig.GuineaPig),
            Extension(data.UndecoratedClass.DecoratedInnerClass.__dict__['decorated_method'], guineapig.GuineaPig.InnerClass),
            Extension(data.UndecoratedClass.__dict__['decorated_method'], guineapig.GuineaPig)
        ]
        discovered_extensions = list(gorilla._utils.extension_iterator(data))
        self.assert_true(_same_list_content(discovered_extensions, extensions))
    
    def test_get_decorator_data_1(self):
        decorated = data.decorator('value')(data.function)
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'default': 'value'})
        
    def test_get_decorator_data_2(self):
        decorated = data.decorator_1('value')(data.function)
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'first': 'value'})
        
    def test_get_decorator_data_3(self):
        decorated = data.decorator_2('value')(data.function)
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'second': 'value'})
    
    def test_get_decorator_data_4(self):
        decorated = data.decorator_1('value_1')(data.decorator_2('value_2')(data.function))
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'first': 'value_1', 'second': 'value_2'})
    
    def test_get_decorator_data_5(self):
        decorated = data.decorator_2('value_2')(data.decorator_1('value_1')(data.function))
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'first': 'value_1', 'second': 'value_2'})
    
    def test_get_decorator_data_6(self):
        decorated = data.decorator('value_a')(data.decorator('value_b')(data.function))
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'default': 'value_a'})
    
    def test_get_decorator_data_7(self):
        decorated = data.decorator('value_b')(data.decorator('value_a')(data.function))
        self.assert_equal(gorilla._utils.get_decorator_data(decorated), {'default': 'value_b'})
    
    def test_get_underlying_object(self):
        object = data.function
        underlying_object = object
        self.assert_is(gorilla._utils.get_underlying_object(object), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(classmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(staticmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(property(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(object)), underlying_object)
        if gorilla._python.VERSION >= (2, 7):
            self.assert_is(gorilla._utils.get_underlying_object(classmethod(staticmethod(property(data.decorator('value')(object))))), underlying_object)
        else:
            self.assert_is(gorilla._utils.get_underlying_object(staticmethod(property(data.decorator('value')(object)))), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(property(staticmethod(classmethod(object))))), underlying_object)
        
        object = data.Class.method
        underlying_object = object.__func__ if hasattr(object, '__func__') else object
        self.assert_is(gorilla._utils.get_underlying_object(object), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(classmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(staticmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(property(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(object)), underlying_object)
        if gorilla._python.VERSION >= (2, 7):
            self.assert_is(gorilla._utils.get_underlying_object(classmethod(staticmethod(property(data.decorator('value')(object))))), underlying_object)
        else:
            self.assert_is(gorilla._utils.get_underlying_object(staticmethod(property(data.decorator('value')(object)))), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(property(staticmethod(classmethod(object))))), underlying_object)
        
        object = data.Class.class_method
        underlying_object = object.__func__
        self.assert_is(gorilla._utils.get_underlying_object(object), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(classmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(staticmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(property(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(object)), underlying_object)
        if gorilla._python.VERSION >= (2, 7):
            self.assert_is(gorilla._utils.get_underlying_object(classmethod(staticmethod(property(data.decorator('value')(object))))), underlying_object)
        else:
            self.assert_is(gorilla._utils.get_underlying_object(staticmethod(property(data.decorator('value')(object)))), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(property(staticmethod(classmethod(object))))), underlying_object)
        
        object = data.Class.static_method
        underlying_object = object
        self.assert_is(gorilla._utils.get_underlying_object(object), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(classmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(staticmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(property(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(object)), underlying_object)
        if gorilla._python.VERSION >= (2, 7):
            self.assert_is(gorilla._utils.get_underlying_object(classmethod(staticmethod(property(data.decorator('value')(object))))), underlying_object)
        else:
            self.assert_is(gorilla._utils.get_underlying_object(staticmethod(property(data.decorator('value')(object)))), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(property(staticmethod(classmethod(object))))), underlying_object)
        
        object = data.Class.property
        underlying_object = object.fget
        self.assert_is(gorilla._utils.get_underlying_object(object), underlying_object)
        if gorilla._python.VERSION >= (2, 7):
            self.assert_is(gorilla._utils.get_underlying_object(classmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(staticmethod(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(property(object)), underlying_object)
        self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(object)), underlying_object)
        if gorilla._python.VERSION >= (2, 7):
            self.assert_is(gorilla._utils.get_underlying_object(classmethod(staticmethod(property(data.decorator('value')(object))))), underlying_object)
            self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(property(staticmethod(classmethod(object))))), underlying_object)
        else:
            self.assert_is(gorilla._utils.get_underlying_object(staticmethod(property(data.decorator('value')(object)))), underlying_object)
            self.assert_is(gorilla._utils.get_underlying_object(data.decorator('value')(property(staticmethod(object)))), underlying_object)
    
    def test_listify(self):
        self.assert_equal(gorilla._utils.listify(None), [])
        self.assert_equal(gorilla._utils.listify(''), [])
        self.assert_equal(gorilla._utils.listify([]), [])
        self.assert_equal(gorilla._utils.listify(()), [])
        
        self.assert_equal(gorilla._utils.listify(None, valid=(None, )), [None])
        self.assert_equal(gorilla._utils.listify(None, valid=[None]), [None])
        self.assert_equal(gorilla._utils.listify('', valid=('')), [''])
        
        self.assert_equal(gorilla._utils.listify('abc'), ['abc'])
        self.assert_equal(gorilla._utils.listify((True, False)), [True, False])
    
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
        
        registered_extensions = gorilla.utils.register_extensions(packages_and_modules=rootmodule)
        self.assert_true(_same_list_content(registered_extensions, extensions))
    
    def test_register_extensions_2(self):
        extension2_class = Extension(extension2.Class, guineapig)
        extension2_class.name = 'Needle'
        submodule_method = Extension(submodule.Class.__dict__['method'], guineapig.GuineaPig)
        submodule_method.name = 'needle_method'
        
        extensions = [extension2_class, submodule_method]
        
        registered_extensions = gorilla.utils.register_extensions(packages_and_modules=[submodule, extension2])
        self.assert_true(_same_list_content(registered_extensions, extensions))
    
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
        
        registered_extensions = gorilla.utils.register_extensions(packages_and_modules=[rootmodule], recursive=False)
        self.assert_true(_same_list_content(registered_extensions, extensions))
    
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
        
        registered_extensions = gorilla.utils.register_extensions(packages_and_modules=rootmodule, settings=data_utils.ExtensionsSettings)
        self.assert_true(_same_list_content(registered_extensions, extensions))
        
    def test_uniquify(self):
        self.assert_equal(gorilla._utils.uniquify([]), [])
        self.assert_equal(gorilla._utils.uniquify([None]), [None])
        self.assert_equal(gorilla._utils.uniquify('abc'), ['a', 'b', 'c'])
        self.assert_equal(gorilla._utils.uniquify(['a', 'b', 'c']), ['a', 'b', 'c'])
        self.assert_equal(gorilla._utils.uniquify(('a', 'b', 'c')), ['a', 'b', 'c'])
        
        self.assert_equal(gorilla._utils.uniquify(['a', 'a', 'b', 'b', 'c', 'c']), ['a', 'b', 'c'])
        self.assert_equal(gorilla._utils.uniquify(['a', 'b', 'c', 'c', 'b', 'a']), ['a', 'b', 'c'])
        self.assert_equal(gorilla._utils.uniquify(['c', 'b', 'a']), ['c', 'b', 'a'])
        self.assert_equal(gorilla._utils.uniquify(['c', 'c', 'b', 'b', 'a', 'a']), ['c', 'b', 'a'])
        self.assert_equal(gorilla._utils.uniquify(['c', 'b', 'a', 'a', 'b', 'c']), ['c', 'b', 'a'])
        self.assert_equal(gorilla._utils.uniquify([9, 4, 2, 85, 86, 4, 28]), [9, 4, 2, 85, 86, 28])


if __name__ == '__main__':
    unittest.main()
