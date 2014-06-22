import sys
import unittest

import gorilla._constants
import gorilla._utils
from gorilla.extension import Extension

from .data_extension import guineapig, needles
from . import GorillaTestCase


def _dicts_equal(this, other):
    if set(this.keys()) != set(other.keys()):
        return False
    
    for key in this.keys():
        if this[key] != other[key]:
            this_function = gorilla._utils.get_underlying_object(this[key])
            other_function = gorilla._utils.get_underlying_object(other[key])
            if this_function == other_function:
                continue
            elif (hasattr(this[key], '__class__') and
                    hasattr(other[key], '__class__') and
                    this[key].__class__ == other[key].__class__):
                continue
            
            return False
    
    return True


class ExtensionTest(GorillaTestCase):
    
    def setup(self):
        global guineapig
        global needles
        guineapig = __import__('data_extension.guineapig', globals(), locals(), ['*'], 1)
        needles = __import__('data_extension.needles', globals(), locals(), ['*'], 1)
    
    def teardown(self):
        global guineapig
        global needles
        del sys.modules[needles.__name__]
        del sys.modules[guineapig.__name__]
    
    def test_patch_module_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig
        self.assert_raises(TypeError, Extension(object, target).patch)
    
    def test_patch_module_with_function_1(self):
        object = needles.function
        target = guineapig
        name = 'needle'
        original = None
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched(), "needle into guinea pig")
    
    def test_patch_module_with_function_2(self):
        object = needles.function
        target = guineapig
        name = object.__name__
        original = getattr(target, name, None)
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original(), "guinea pig")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "guineapig function.")
        self.assert_equal(patched(), "needle into guinea pig")
    
    def test_patch_module_with_class_1(self):
        object = needles.GuineaPig
        target = guineapig
        name = 'Needle'
        original = None
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched().THIS, "new guinea pig")
        self.assert_equal(patched().InnerClass().method(), "always more inner")
        self.assert_equal(patched()._value, "more awesome")
        self.assert_equal(patched().method(), "Everything is more awesome! This new guinea pig too.")
        self.assert_equal(patched().class_method(), "Classic new guinea pig but even more awesome nonetheless!")
        self.assert_equal(patched().static_method(), "Static new guinea pig but even more awesome nonetheless!")
        self.assert_equal(patched().value, "even more awesome")
    
    def test_patch_module_with_class_2(self):
        object = needles.GuineaPig
        target = guineapig
        name = object.__name__
        original = getattr(target, name, None)
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDict = original.__dict__.copy()
        
        diff = {}
        for attributeName, attribute in gorilla._utils.class_attribute_iterator(object):
            if hasattr(original, attributeName) and not isinstance(attribute, type):
                diff[gorilla._constants.ORIGINAL % attributeName] = getattr(original, attributeName)
        for attributeName, attribute in gorilla._utils.class_attribute_iterator(object):
            diff[attributeName] = attribute
        originalDict.update(diff)
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original().THIS, "guinea pig")
        self.assert_equal(original().InnerClass().method(), "inner")
        self.assert_equal(original().InnerClass()._initialized, True)
        self.assert_equal(original()._value, "awesome")
        self.assert_equal(original().method(), "Everything is awesome! This guinea pig too.")
        self.assert_equal(original().class_method(), "Classic guinea pig but awesome nonetheless!")
        self.assert_equal(original().static_method(), "Static guinea pig but awesome nonetheless!")
        self.assert_equal(original().value, "awesome")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is_not(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(_dicts_equal(original.__dict__, originalDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "GuineaPig class.")
        self.assert_equal(patched().THIS, "guinea pig")
        self.assert_equal(patched().InnerClass().method(), "always more inner")
        self.assert_equal(hasattr(patched().InnerClass(), '_initialized'), False)
        self.assert_equal(patched()._value, "more awesome")
        self.assert_equal(patched().method(), "Everything is more awesome! This new guinea pig too.")
        self.assert_equal(patched().class_method(), "Classic guinea pig but even more awesome nonetheless!")
        self.assert_equal(patched().static_method(), "Static new guinea pig but even more awesome nonetheless!")
        self.assert_equal(patched().value, "even more awesome")
        self.assert_equal(patched().InnerClass().method(), "always more inner")
    
    def test_patch_module_with_method_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['method']
        target = guineapig
        name = 'needle'
        original = None
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched(cls()), "Everything is more awesome! This new guinea pig too.")
    
    def test_patch_module_with_method_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['method']
        target = guineapig
        name = object.__name__
        original = getattr(target, name, None)
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original(cls()), "Everything is even more awesome! This new guinea pig too.")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "guineapig method.")
        self.assert_equal(patched(cls()), "Everything is more awesome! This new guinea pig too.")
    
    def test_patch_module_with_class_method_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['class_method']
        target = guineapig
        name = 'needle'
        original = None
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(gorilla._utils.get_underlying_object(patched).__doc__)
        self.assert_equal(gorilla._utils.get_underlying_object(patched)(cls), "Classic new guinea pig but even more awesome nonetheless!")
    
    def test_patch_module_with_class_method_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['class_method']
        target = guineapig
        name = gorilla._utils.get_underlying_object(object).__name__
        original = getattr(target, name, None)
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(gorilla._utils.get_underlying_object(original)(cls), "Classic guinea pig but even more awesome nonetheless!")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(gorilla._utils.get_underlying_object(patched).__doc__ == gorilla._utils.get_underlying_object(original).__doc__ == "guineapig class method.")
        self.assert_equal(gorilla._utils.get_underlying_object(patched)(cls), "Classic new guinea pig but even more awesome nonetheless!")
    
    def test_patch_module_with_static_method_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['static_method']
        target = guineapig
        name = 'needle'
        original = None
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(gorilla._utils.get_underlying_object(patched).__doc__)
        self.assert_equal(gorilla._utils.get_underlying_object(patched)(), "Static new guinea pig but even more awesome nonetheless!")
    
    def test_patch_module_with_static_method_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['static_method']
        target = guineapig
        name = gorilla._utils.get_underlying_object(object).__name__
        original = getattr(target, name, None)
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(gorilla._utils.get_underlying_object(original)(), "Static guinea pig but awesome nonetheless!")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(gorilla._utils.get_underlying_object(patched).__doc__ == gorilla._utils.get_underlying_object(original).__doc__ == "guineapig static method.")
        self.assert_equal(gorilla._utils.get_underlying_object(patched)(), "Static new guinea pig but even more awesome nonetheless!")
    
    def test_patch_module_with_property_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['value']
        target = guineapig
        name = 'needle'
        original = None
        object_dict = object.fget.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.fget.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched.fget(cls()), "even more awesome")
    
    def test_patch_module_with_property_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['value']
        target = guineapig
        name = object.fget.__name__
        original = getattr(target, name, None)
        object_dict = object.fget.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original.fget(cls()), "more awesome")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.fget.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.fget.__doc__ == original.__doc__ == "guineapig property.")
        self.assert_equal(patched.fget(cls()), "even more awesome")
    
    def test_patch_function_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_function_with_function(self):
        object = needles.function
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_function_with_class(self):
        object = needles.GuineaPig
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_function_with_method(self):
        object = needles.GuineaPig.method
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_function_with_class_method(self):
        object = needles.GuineaPig.class_method
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_function_with_static_method(self):
        object = needles.GuineaPig.static_method
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_function_with_property(self):
        object = needles.GuineaPig.value
        target = guineapig.function
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig.GuineaPig
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_with_function_1(self):
        object = needles.method
        target = guineapig.GuineaPig
        name = 'needle'
        original = None
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(gorilla._utils.get_underlying_object(patched), object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched(target()), "needle into guinea pig")
    
    def test_patch_class_with_function_2(self):
        object = needles.method
        target = guineapig.GuineaPig
        name = object.__name__
        original = target.__dict__['method']
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original(target()), "Everything is awesome! This guinea pig too.")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(gorilla._utils.get_underlying_object(patched), object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "GuineaPig method.")
        self.assert_equal(patched(target()), "needle into guinea pig")
    
    def test_patch_class_with_class_1(self):
        object = needles.GuineaPig.InnerClass
        target = guineapig.GuineaPig
        name = 'NeedleInnerClass'
        original = None
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched()._value, "more inner")
        self.assert_equal(patched().method(), "always more inner")
    
    def test_patch_class_with_class_2(self):
        object = needles.GuineaPig.InnerClass
        target = guineapig.GuineaPig
        name = object.__name__
        original = target.__dict__['InnerClass']
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original()._value, "inner")
        self.assert_equal(original().method(), "inner")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is_not(patched, object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "InnerClass class.")
        self.assert_equal(patched()._value, "more inner")
        self.assert_equal(patched().method(), "always more inner")
        
    def test_patch_class_with_method_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['method']
        target = guineapig.GuineaPig
        name = 'needle'
        original = None
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(gorilla._utils.get_underlying_object(patched), object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched(target()), "Everything is awesome! This new guinea pig too.")
    
    def test_patch_class_with_method_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['method']
        target = guineapig.GuineaPig
        name = object.__name__
        original = target.__dict__['method']
        object_dict = object.__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original(target()), "Everything is awesome! This guinea pig too.")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(gorilla._utils.get_underlying_object(patched), object)
        self.assert_true(_dicts_equal(object.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "GuineaPig method.")
        self.assert_equal(patched(target()), "Everything is awesome! This new guinea pig too.")
    
    def test_patch_class_with_class_method_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['class_method']
        target = guineapig.GuineaPig
        name = 'needle'
        original = None
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched.__func__, gorilla._utils.get_underlying_object(object))
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched(), "Static guinea pig but awesome nonetheless!")
    
    def test_patch_class_with_class_method_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['class_method']
        target = guineapig.GuineaPig
        name = gorilla._utils.get_underlying_object(object).__name__
        original = target.__dict__['class_method']
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original(), "Classic guinea pig but awesome nonetheless!")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(gorilla._utils.get_underlying_object(patched), gorilla._utils.get_underlying_object(object))
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "GuineaPig class method.")
        self.assert_equal(patched(), "Static guinea pig but awesome nonetheless!")
    
    def test_patch_class_with_static_method_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['static_method']
        target = guineapig.GuineaPig
        name = 'needle'
        original = None
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, gorilla._utils.get_underlying_object(object))
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched(), "Static new guinea pig but even more awesome nonetheless!")
    
    def test_patch_class_with_static_method_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['static_method']
        target = guineapig.GuineaPig
        name = gorilla._utils.get_underlying_object(object).__name__
        original = target.__dict__['static_method']
        object_dict = gorilla._utils.get_underlying_object(object).__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original(), "Static guinea pig but awesome nonetheless!")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, gorilla._utils.get_underlying_object(object))
        self.assert_true(_dicts_equal(gorilla._utils.get_underlying_object(object).__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.__doc__ == original.__doc__ == "GuineaPig static method.")
        self.assert_equal(patched(), "Static new guinea pig but even more awesome nonetheless!")
    
    def test_patch_class_with_property_1(self):
        cls = needles.GuineaPig
        object = cls.__dict__['value']
        target = guineapig.GuineaPig
        name = 'needle'
        original = None
        object_dict = object.fget.__dict__.copy()
        targetDict = target.__dict__.copy()
        
        targetDict.update({name: object})
        
        extension = Extension(object, target, name=name)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        self.assert_false(hasattr(target, name))
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.fget.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_is_none(patched.__doc__)
        self.assert_equal(patched.fget(target()), "even awesome")
    
    def test_patch_class_with_property_2(self):
        cls = needles.GuineaPig
        object = cls.__dict__['value']
        target = guineapig.GuineaPig
        name = object.fget.__name__
        original = target.__dict__['value']
        object_dict = object.fget.__dict__.copy()
        targetDict = target.__dict__.copy()
        originalDoc = getattr(original, '__doc__') if original else None
        
        targetDict.update({name: object, gorilla._constants.ORIGINAL % name: original})
        
        extension = Extension(object, target)
        self.assert_is(extension.object, object)
        self.assert_equal(extension.name, name)
        self.assert_is(extension.target, target)
        self.assert_is(extension.original, original)
        self.assert_equal(extension.apply, [])
        
        original = getattr(target, name)
        self.assert_equal(original.fget(target()), "awesome")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is(patched, object)
        self.assert_true(_dicts_equal(object.fget.__dict__, object_dict))
        self.assert_true(_dicts_equal(target.__dict__, targetDict))
        self.assert_true(patched.fget.__doc__ == original.__doc__ == "GuineaPig property.")
        self.assert_equal(patched.fget(target()), "even awesome")
    
    def test_patch_method_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig.GuineaPig.method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_method_with_function(self):
        object = needles.function
        target = guineapig.GuineaPig.method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_method_with_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig.method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_method_with_method(self):
        object = needles.GuineaPig.__dict__['method']
        target = guineapig.GuineaPig.method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_method_with_class_method(self):
        object = needles.GuineaPig.__dict__['class_method']
        target = guineapig.GuineaPig.method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_method_with_static_method(self):
        object = needles.GuineaPig.__dict__['static_method']
        target = guineapig.GuineaPig.method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_method_with_property(self):
        object = needles.GuineaPig.__dict__['value']
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_function(self):
        object = needles.function
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_method(self):
        object = needles.GuineaPig.__dict__['method']
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_class_method(self):
        object = needles.GuineaPig.__dict__['class_method']
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_static_method(self):
        object = needles.GuineaPig.__dict__['static_method']
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_class_method_with_property(self):
        object = needles.GuineaPig.__dict__['value']
        target = guineapig.GuineaPig.class_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_function(self):
        object = needles.function
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_method(self):
        object = needles.GuineaPig.__dict__['method']
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_class_method(self):
        object = needles.GuineaPig.__dict__['class_method']
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_static_method(self):
        object = needles.GuineaPig.__dict__['static_method']
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_static_method_with_property(self):
        object = needles.GuineaPig.__dict__['value']
        target = guineapig.GuineaPig.static_method
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_module(self):
        object = sys.modules[self.__module__]
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_function(self):
        object = needles.function
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_class(self):
        object = needles.GuineaPig
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_method(self):
        object = needles.GuineaPig.__dict__['method']
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_class_method(self):
        object = needles.GuineaPig.__dict__['class_method']
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_static_method(self):
        object = needles.GuineaPig.__dict__['static_method']
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_property_with_property(self):
        object = needles.GuineaPig.__dict__['value']
        target = guineapig.GuineaPig.value
        self.assert_raises(TypeError, gorilla.extension.Extension(object, target).patch)
    
    def test_patch_nested_classes_1(self):
        object = needles.Ancestor
        target = guineapig
        name = object.__name__
        
        extension = Extension(object, target)
        
        orginal = getattr(target, name)
        self.assert_equal(orginal().value, "guinea pig")
        self.assert_equal(orginal.Child().value, "guinea pig's child")
        self.assert_equal(orginal.Child.GrandChild().value, "guinea pig's grand child")
        
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is_not(patched, object)
        self.assert_equal(patched().value, "needle")
        self.assert_equal(patched.Child().value, "needle's child")
        self.assert_equal(patched.Child.GrandChild().value, "needle's grand child")
    
    def test_patch_nested_classes_2(self):
        object = needles.Ancestor
        target = guineapig
        name = object.__name__
        
        extension = Extension(object, target)
        
        original = getattr(target, name)
        self.assert_equal(original().value, "guinea pig")
        self.assert_equal(original.Child().value, "guinea pig's child")
        self.assert_equal(original.Child.GrandChild().value, "guinea pig's grand child")
        
        object.Child = gorilla.name('OtherChild')(object.__dict__['Child'])
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_is_not(patched, object)
        self.assert_equal(patched().value, "needle")
        self.assert_equal(patched.Child().value, "guinea pig's child")
        self.assert_equal(patched.Child.GrandChild().value, "guinea pig's grand child")
        self.assert_equal(patched.OtherChild().value, "needle's child")
        self.assert_equal(patched.OtherChild.GrandChild().value, "needle's grand child")
    
    def test_apply_class_method(self):
        object = needles.class_method
        target = guineapig.GuineaPig
        name = 'needle'
        apply = classmethod
        
        extension = Extension(object, target, name=name, apply=apply)
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_isinstance(target.__dict__[name], classmethod)
        self.assert_is(patched.__func__, object)
        self.assert_equal(patched(), "needle into guinea pig")
    
    def test_apply_static_method(self):
        object = needles.static_method
        target = guineapig.GuineaPig
        name = 'needle'
        apply = staticmethod
        
        extension = Extension(object, target, name=name, apply=apply)
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_isinstance(target.__dict__[name], staticmethod)
        self.assert_is(patched, object)
        self.assert_equal(patched(), "needle into new guinea pig")
    
    def test_apply_property(self):
        object = needles.value
        target = guineapig.GuineaPig
        name = 'needle'
        apply = property
        
        extension = Extension(object, target, name=name, apply=apply)
        extension.patch()
        
        patched = getattr(target, name)
        self.assert_isinstance(target.__dict__[name], property)
        self.assert_is(patched.fget, object)
        self.assert_equal(patched.fget(target()), "awesome")


if __name__ == '__main__':
    unittest.main()
