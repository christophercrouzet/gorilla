import unittest

import gorilla._objecttype

from .data_objecttype import data
from . import GorillaTestCase


class ObjectTypeTest(GorillaTestCase):

    def test_object_types(self):
        self.assert_equal(gorilla._objecttype.get(data), gorilla._objecttype.MODULE)

        self.assert_equal(gorilla._objecttype.get(data.function_1), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.function_2), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.function_3), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.function_4), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.class_method_1), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.class_method_2), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.class_method_3), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.class_method_4), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.class_method_5), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.class_method_6), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.class_method_7), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.static_method_1), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.static_method_2), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.static_method_3), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.static_method_4), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.static_method_5), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.static_method_6), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.static_method_7), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.property_1), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.property_2), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.property_3), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.property_4), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.property_5), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.property_6), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.property_7), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.Class_1), gorilla._objecttype.CLASS)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.__init__), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.__dict__['__init__']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.__dict__['method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.class_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.__dict__['class_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.static_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.__dict__['static_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.property), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_1.__dict__['property']), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.Class_2), gorilla._objecttype.CLASS)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.__init__), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.__dict__['__init__']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.__dict__['method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.class_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.__dict__['class_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.static_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.__dict__['static_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.property), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_2.__dict__['property']), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.Class_3), gorilla._objecttype.CLASS)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.__init__), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.__dict__['__init__']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.__dict__['method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.class_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.__dict__['class_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.static_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.__dict__['static_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.property), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_3.__dict__['property']), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.Class_4), gorilla._objecttype.CLASS)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.__init__), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.__dict__['__init__']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.__dict__['method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.class_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.__dict__['class_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.static_method), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.__dict__['static_method']), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.property), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.Class_4.__dict__['property']), gorilla._objecttype.DESCRIPTOR)

        self.assert_equal(gorilla._objecttype.get(data.EmptyClass_1), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.EmptyClass_2), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.EmptyClass_3), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.EmptyClass_4), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.EmptyClass_5), gorilla._objecttype.DESCRIPTOR)
        self.assert_equal(gorilla._objecttype.get(data.EmptyClass_6), gorilla._objecttype.CLASS)


if __name__ == '__main__':
    unittest.main()
