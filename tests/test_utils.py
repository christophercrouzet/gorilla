import os
import sys
import unittest

import gorilla._python
import gorilla._utils
import gorilla.decorators
import gorilla.utils
from gorilla.extension import Extension

from .data_utils import data, guineapig
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
        guineapig = __import__('data_utils.guineapig', globals(), locals(), ['*'], 1)
        data = __import__('data_utils.data', globals(), locals(), ['*'], 1)
        self.sys_path = list(sys.path)
    
    def teardown(self):
        global data
        global guineapig
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
        self.assert_equal(gorilla.utils.listify(None), [])
        self.assert_equal(gorilla.utils.listify(''), [])
        self.assert_equal(gorilla.utils.listify([]), [])
        self.assert_equal(gorilla.utils.listify(()), [])
        
        self.assert_equal(gorilla.utils.listify(None, valid=(None, )), [None])
        self.assert_equal(gorilla.utils.listify(None, valid=[None]), [None])
        self.assert_equal(gorilla.utils.listify('', valid=('')), [''])
        
        self.assert_equal(gorilla.utils.listify('abc'), ['abc'])
        self.assert_equal(gorilla.utils.listify((True, False)), [True, False])
    
    def test_uniquify(self):
        self.assert_equal(gorilla.utils.uniquify([]), [])
        self.assert_equal(gorilla.utils.uniquify([None]), [None])
        self.assert_equal(gorilla.utils.uniquify('abc'), ['a', 'b', 'c'])
        self.assert_equal(gorilla.utils.uniquify(['a', 'b', 'c']), ['a', 'b', 'c'])
        self.assert_equal(gorilla.utils.uniquify(('a', 'b', 'c')), ['a', 'b', 'c'])
        
        self.assert_equal(gorilla.utils.uniquify(['a', 'a', 'b', 'b', 'c', 'c']), ['a', 'b', 'c'])
        self.assert_equal(gorilla.utils.uniquify(['a', 'b', 'c', 'c', 'b', 'a']), ['a', 'b', 'c'])
        self.assert_equal(gorilla.utils.uniquify(['c', 'b', 'a']), ['c', 'b', 'a'])
        self.assert_equal(gorilla.utils.uniquify(['c', 'c', 'b', 'b', 'a', 'a']), ['c', 'b', 'a'])
        self.assert_equal(gorilla.utils.uniquify(['c', 'b', 'a', 'a', 'b', 'c']), ['c', 'b', 'a'])
        self.assert_equal(gorilla.utils.uniquify([9, 4, 2, 85, 86, 4, 28]), [9, 4, 2, 85, 86, 28])


if __name__ == '__main__':
    unittest.main()
