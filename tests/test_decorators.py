import sys
import unittest

import gorilla._constants
import gorilla._utils
import gorilla.decorators
from gorilla.extension import Extension

from .data_decorators import data, guineapig, needles
from . import GorillaTestCase


class DecoratorsTest(GorillaTestCase):
    
    def setup(self):
        global needles
        global guineapig
        guineapig = __import__('data_decorators.guineapig', globals(), locals(), ['*'], 1)
        needles = __import__('data_decorators.needles', globals(), locals(), ['*'], 1)
    
    def teardown(self):
        global needles
        global guineapig
        del sys.modules[needles.__name__]
        del sys.modules[guineapig.__name__]
    
    def test_patch_decorator_on_function(self):
        object = needles.function
        target = guineapig.GuineaPig
        name = 'needle'
        apply = data.decorator
        extension = Extension(object, target, name=name, apply=apply)
        
        decorated = gorilla.decorators.patch(target, name=name, apply=apply)(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        self.assert_equal(extensions[0], extension)
    
    def test_patch_decorator_on_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig
        name = 'Needle'
        apply = data.decorator
        extension = Extension(object, target, name=name, apply=apply)
        
        decorated = gorilla.decorators.patch(target, name=name, apply=apply)(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        self.assert_equal(extensions[0], extension)
    
    def test_patch_decorator_on_method(self):
        object = needles.GuineaPig.method
        target = guineapig.GuineaPig
        name = 'needle'
        apply = data.decorator
        extension = Extension(object, target, name=name, apply=apply)
        
        decorated = gorilla.decorators.patch(target, name=name, apply=apply)(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        self.assert_equal(extensions[0], extension)
    
    def test_patch_decorator_on_class_method(self):
        object = needles.GuineaPig.class_method
        target = guineapig.GuineaPig
        name = 'needle'
        apply = data.decorator
        extension = Extension(object, target, name=name, apply=apply)
        
        decorated = gorilla.decorators.patch(target, name=name, apply=apply)(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        self.assert_equal(extensions[0], extension)
    
    def test_patch_decorator_on_static_method(self):
        object = needles.GuineaPig.static_method
        target = guineapig.GuineaPig
        name = 'needle'
        apply = data.decorator
        extension = Extension(object, target, name=name, apply=apply)
        
        decorated = gorilla.decorators.patch(target, name=name, apply=apply)(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        self.assert_equal(extensions[0], extension)
    
    def test_patch_decorator_on_property(self):
        object = needles.GuineaPig.value
        target = guineapig.GuineaPig
        name = 'needle'
        apply = data.decorator
        extension = Extension(object, target, name=name, apply=apply)
        
        decorated = gorilla.decorators.patch(target, name=name, apply=apply)(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        self.assert_equal(extensions[0], extension)
    
    def test_name_decorator_on_function(self):
        object = needles.function
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.name(name)(object)
        name_data = gorilla._utils.get_decorator_data(decorated).get('name', '')
        self.assert_equal(name_data, name)
    
    def test_name_decorator_on_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig
        name = 'Needle'
        
        decorated = gorilla.decorators.name(name)(object)
        name_data = gorilla._utils.get_decorator_data(decorated).get('name', '')
        self.assert_equal(name_data, name)
    
    def test_name_decorator_on_method(self):
        object = needles.GuineaPig.method
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.name(name)(object)
        name_data = gorilla._utils.get_decorator_data(decorated).get('name', '')
        self.assert_equal(name_data, name)
    
    def test_name_decorator_on_class_method(self):
        object = needles.GuineaPig.class_method
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.name(name)(object)
        name_data = gorilla._utils.get_decorator_data(decorated).get('name', '')
        self.assert_equal(name_data, name)
    
    def test_name_decorator_on_static_method(self):
        object = needles.GuineaPig.static_method
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.name(name)(object)
        name_data = gorilla._utils.get_decorator_data(decorated).get('name', '')
        self.assert_equal(name_data, name)
    
    def test_name_decorator_on_property(self):
        object = needles.GuineaPig.value
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.name(name)(object)
        name_data = gorilla._utils.get_decorator_data(decorated).get('name', '')
        self.assert_equal(name_data, name)
    
    def test_apply_decorator_on_function(self):
        object = needles.function
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(apply)(object)
        apply_data = gorilla._utils.get_decorator_data(decorated).get('apply', '')
        self.assert_equal(apply_data, [apply])
    
    def test_apply_decorator_on_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(apply)(object)
        apply_data = gorilla._utils.get_decorator_data(decorated).get('apply', '')
        self.assert_equal(apply_data, [apply])
    
    def test_apply_decorator_on_method(self):
        object = needles.GuineaPig.method
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(apply)(object)
        apply_data = gorilla._utils.get_decorator_data(decorated).get('apply', '')
        self.assert_equal(apply_data, [apply])
    
    def test_apply_decorator_on_class_method(self):
        object = needles.GuineaPig.class_method
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(apply)(object)
        apply_data = gorilla._utils.get_decorator_data(decorated).get('apply', '')
        self.assert_equal(apply_data, [apply])
    
    def test_apply_decorator_on_static_method(self):
        object = needles.GuineaPig.static_method
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(apply)(object)
        apply_data = gorilla._utils.get_decorator_data(decorated).get('apply', '')
        self.assert_equal(apply_data, [apply])
    
    def test_apply_decorator_on_property(self):
        object = needles.GuineaPig.value
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(apply)(object)
        apply_data = gorilla._utils.get_decorator_data(decorated).get('apply', '')
        self.assert_equal(apply_data, [apply])
    
    def test_apply_decorator_append(self):
        object = needles.function
        target = guineapig.GuineaPig
        apply = staticmethod
        
        decorated = gorilla.decorators.apply(apply, append=True)(gorilla.decorators.patch(target, apply=classmethod)(object))
        extensions = gorilla._utils.get_decorator_data(decorated).get('extensions')
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        
        decorated_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('apply', decorated_data)
        self.assert_equal(extensions[0].apply, [classmethod, apply])
    
    def test_apply_decorator_prepend(self):
        object = needles.function
        target = guineapig.GuineaPig
        apply = staticmethod
        
        decorated = gorilla.decorators.apply(apply, prepend=True)(gorilla.decorators.patch(target, apply=classmethod)(object))
        extensions = gorilla._utils.get_decorator_data(decorated).get('extensions')
        self.assert_equal(len(extensions), 1)
        self.assert_isinstance(extensions[0], gorilla.extension.Extension)
        
        decorated_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('apply', decorated_data)
        self.assert_equal(extensions[0].apply, [apply, classmethod])
    
    def test_stack_patch_on_name(self):
        object = needles.function
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.patch(target, name=name)(gorilla.decorators.name('whatever')(object))
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_equal(decorator_data.get('name', ''), 'whatever')
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(extensions[0].name, name)
    
    def test_stack_name_on_patch(self):
        object = needles.function
        target = guineapig.GuineaPig
        name = 'needle'
        
        decorated = gorilla.decorators.name('whatever')(gorilla.decorators.patch(target, name=name)(object))
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(extensions[0].name, 'whatever')
    
    def test_stack_patch_on_apply(self):
        object = needles.function
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.patch(target, apply=apply)(gorilla.decorators.apply(classmethod)(object))
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_equal(decorator_data['apply'], [classmethod])
        
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(extensions[0].apply, [apply])
    
    def test_stack_apply_on_patch(self):
        object = needles.function
        target = guineapig.GuineaPig
        apply = data.decorator
        
        decorated = gorilla.decorators.apply(classmethod)(gorilla.decorators.patch(target, apply=apply)(object))
        decorator_data = gorilla._utils.get_decorator_data(decorated)
        self.assert_not_in('name', decorator_data)
        self.assert_not_in('apply', decorator_data)
        
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(extensions[0].apply, [classmethod])
    
    def test_decorator_mashup(self):
        object = needles.function
        target = guineapig.GuineaPig
        
        decorated_1 = gorilla.decorators.name('decorator_1')(object)
        decorator_data = gorilla._utils.get_decorator_data(decorated_1)
        self.assert_equal(decorator_data.get('name', ''), 'decorator_1')
        self.assert_not_in('extensions', decorator_data)
        
        decorated_2 = gorilla.decorators.name('decorator_2')(gorilla.decorators.patch(target)(decorated_1))
        decorator_data = gorilla._utils.get_decorator_data(decorated_2)
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(decorator_data.get('name', ''), 'decorator_1')
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 1)
        self.assert_equal(extensions[0].name, 'decorator_2')
        
        decorated_3 = gorilla.decorators.name('decorator_3')(gorilla.decorators.patch(target)(decorated_2))
        decorator_data = gorilla._utils.get_decorator_data(decorated_3)
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(decorator_data.get('name', ''), 'decorator_1')
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 2)
        self.assert_equal(extensions[0].name, 'decorator_3')
        self.assert_equal(extensions[1].name, 'decorator_2')
        
        decorated_4 = gorilla.decorators.name('decorator_4')(decorated_3)
        decorator_data = gorilla._utils.get_decorator_data(decorated_4)
        extensions = decorator_data.get('extensions', [])
        self.assert_equal(decorator_data.get('name', ''), 'decorator_1')
        self.assert_is_not_none(extensions)
        self.assert_equal(len(extensions), 2)
        self.assert_equal(extensions[0].name, 'decorator_4')
        self.assert_equal(extensions[1].name, 'decorator_2')
        return


if __name__ == '__main__':
    unittest.main()
