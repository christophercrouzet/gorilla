import unittest

from gorilla._objecttype import ObjectType

from .data_objecttype import data
from . import GorillaTestCase


class ObjectTypeTest(GorillaTestCase):
    
    def test_object_types(self):
        self.assert_equal(ObjectType.get(data), ObjectType.MODULE)
        
        self.assert_equal(ObjectType.get(data.function_1), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.function_2), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.function_3), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.function_4), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.class_method_1), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.class_method_2), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.class_method_3), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.class_method_4), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.class_method_5), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.class_method_6), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.class_method_7), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.static_method_1), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.static_method_2), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.static_method_3), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.static_method_4), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.static_method_5), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.static_method_6), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.static_method_7), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.property_1), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.property_2), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.property_3), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.property_4), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.property_5), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.property_6), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.property_7), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.Class_1), ObjectType.CLASS)
        self.assert_equal(ObjectType.get(data.Class_1.__init__), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.__dict__['__init__']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.__dict__['method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.class_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.__dict__['class_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.static_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.__dict__['static_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.property), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_1.__dict__['property']), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.Class_2), ObjectType.CLASS)
        self.assert_equal(ObjectType.get(data.Class_2.__init__), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.__dict__['__init__']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.__dict__['method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.class_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.__dict__['class_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.static_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.__dict__['static_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.property), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_2.__dict__['property']), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.Class_3), ObjectType.CLASS)
        self.assert_equal(ObjectType.get(data.Class_3.__init__), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.__dict__['__init__']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.__dict__['method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.class_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.__dict__['class_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.static_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.__dict__['static_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.property), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_3.__dict__['property']), ObjectType.DESCRIPTOR)
        
        self.assert_equal(ObjectType.get(data.Class_4), ObjectType.CLASS)
        self.assert_equal(ObjectType.get(data.Class_4.__init__), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.__dict__['__init__']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.__dict__['method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.class_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.__dict__['class_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.static_method), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.__dict__['static_method']), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.property), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.Class_4.__dict__['property']), ObjectType.DESCRIPTOR)
    
        self.assert_equal(ObjectType.get(data.EmptyClass_1), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.EmptyClass_2), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.EmptyClass_3), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.EmptyClass_4), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.EmptyClass_5), ObjectType.DESCRIPTOR)
        self.assert_equal(ObjectType.get(data.EmptyClass_6), ObjectType.CLASS)


if __name__ == '__main__':
    unittest.main()
