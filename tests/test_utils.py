#!/usr/bin/env python

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import importlib
import sys

import gorilla

from tests._testcase import GorillaTestCase
import tests.utils
from tests.utils import frommodule
from tests.utils import tomodule
from tests.utils import subpackage
from tests.utils.subpackage import module1
from tests.utils.subpackage import module2


if sys.version_info[0] == 2:
    def _iteritems(d, **kwargs):
        return d.iteritems(**kwargs)

    def _unfold(obj):
        return obj.__func__
else:
    def _iteritems(d, **kwargs):
        return iter(d.items(**kwargs))

    def _unfold(obj):
        return obj


class UtilsTest(GorillaTestCase):

    def setUp(self):
        global frommodule, tomodule, subpackage, module1, module2
        tomodule = importlib.import_module(tomodule.__name__)
        frommodule = importlib.import_module(frommodule.__name__)
        subpackage = importlib.import_module(subpackage.__name__)
        module1 = importlib.import_module(module1.__name__)
        module2 = importlib.import_module(module2.__name__)

    def tearDown(self):
        for module in [tomodule, frommodule, subpackage, module1, module2]:
            if module.__name__ in sys.modules:
                del sys.modules[module.__name__]

    def test_create_patches_1(self):
        destination = tomodule
        obj = frommodule
        patches = gorilla.create_patches(destination, obj,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'function', gorilla.get_attribute(obj, 'function')),
            gorilla.Patch(destination, 'global_variable', gorilla.get_attribute(obj, 'global_variable')),
            gorilla.Patch(destination, 'unbound_class_method', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_method', gorilla.get_attribute(obj, 'unbound_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method')),
            gorilla.Patch(destination.Child, 'STATIC_VALUE', gorilla.get_attribute(obj.Child, 'STATIC_VALUE')),
            gorilla.Patch(destination.Child, 'child_value', gorilla.get_attribute(obj.Child, 'child_value')),
            gorilla.Patch(destination.Child, 'from_value', gorilla.get_attribute(obj.Child, 'from_value')),
            gorilla.Patch(destination.Child, 'instance_value', gorilla.get_attribute(obj.Child, 'instance_value')),
            gorilla.Patch(destination.Child, 'method', gorilla.get_attribute(obj.Child, 'method')),
            gorilla.Patch(destination.Child, 'parent_value', gorilla.get_attribute(obj.Child, 'parent_value')),
            gorilla.Patch(destination.Child, 'to_value', gorilla.get_attribute(obj.Child, 'to_value')),
            gorilla.Patch(destination.Class, 'STATIC_VALUE', gorilla.get_attribute(obj.Class, 'STATIC_VALUE')),
            gorilla.Patch(destination.Class, 'class_method', gorilla.get_attribute(obj.Class, 'class_method')),
            gorilla.Patch(destination.Class, 'method', gorilla.get_attribute(obj.Class, 'method')),
            gorilla.Patch(destination.Class, 'static_method', gorilla.get_attribute(obj.Class, 'static_method')),
            gorilla.Patch(destination.Class, 'value', gorilla.get_attribute(obj.Class, 'value')),
            gorilla.Patch(destination.Parent, 'STATIC_VALUE', gorilla.get_attribute(obj.Parent, 'STATIC_VALUE')),
            gorilla.Patch(destination.Parent, 'from_value', gorilla.get_attribute(obj.Parent, 'from_value')),
            gorilla.Patch(destination.Parent, 'instance_value', gorilla.get_attribute(obj.Parent, 'instance_value')),
            gorilla.Patch(destination.Parent, 'method', gorilla.get_attribute(obj.Parent, 'method')),
            gorilla.Patch(destination.Parent, 'parent_value', gorilla.get_attribute(obj.Parent, 'parent_value')),
            gorilla.Patch(destination.Parent, 'to_value', gorilla.get_attribute(obj.Parent, 'to_value')),
            gorilla.Patch(destination.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Class.Inner, 'method', gorilla.get_attribute(obj.Class.Inner, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Class
        obj = frommodule.Class
        patches = gorilla.create_patches(destination, obj,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value')),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Parent
        obj = frommodule.Parent
        patches = gorilla.create_patches(destination, obj,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'from_value', gorilla.get_attribute(obj, 'from_value')),
            gorilla.Patch(destination, 'instance_value', gorilla.get_attribute(obj, 'instance_value')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'parent_value', gorilla.get_attribute(obj, 'parent_value')),
            gorilla.Patch(destination, 'to_value', gorilla.get_attribute(obj, 'to_value')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Child
        obj = frommodule.Child
        patches = gorilla.create_patches(destination, obj,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'child_value', gorilla.get_attribute(obj, 'child_value')),
            gorilla.Patch(destination, 'from_value', gorilla.get_attribute(obj, 'from_value')),
            gorilla.Patch(destination, 'instance_value', gorilla.get_attribute(obj, 'instance_value')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'parent_value', gorilla.get_attribute(obj, 'parent_value')),
            gorilla.Patch(destination, 'to_value', gorilla.get_attribute(obj, 'to_value')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_2(self):
        destination = tomodule
        obj = frommodule
        patches = gorilla.create_patches(destination, obj, recursive=False,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'Child', gorilla.get_attribute(obj, 'Child')),
            gorilla.Patch(destination, 'Class', gorilla.get_attribute(obj, 'Class')),
            gorilla.Patch(destination, 'Parent', gorilla.get_attribute(obj, 'Parent')),
            gorilla.Patch(destination, 'function', gorilla.get_attribute(obj, 'function')),
            gorilla.Patch(destination, 'global_variable', gorilla.get_attribute(obj, 'global_variable')),
            gorilla.Patch(destination, 'unbound_class_method', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_method', gorilla.get_attribute(obj, 'unbound_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Class
        obj = frommodule.Class
        patches = gorilla.create_patches(destination, obj, recursive=False,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'Inner', gorilla.get_attribute(obj, 'Inner')),
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Parent
        obj = frommodule.Parent
        patches = gorilla.create_patches(destination, obj, recursive=False,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'from_value', gorilla.get_attribute(obj, 'from_value')),
            gorilla.Patch(destination, 'instance_value', gorilla.get_attribute(obj, 'instance_value')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'parent_value', gorilla.get_attribute(obj, 'parent_value')),
            gorilla.Patch(destination, 'to_value', gorilla.get_attribute(obj, 'to_value')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Child
        obj = frommodule.Child
        patches = gorilla.create_patches(destination, obj, recursive=False,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'child_value', gorilla.get_attribute(obj, 'child_value')),
            gorilla.Patch(destination, 'from_value', gorilla.get_attribute(obj, 'from_value')),
            gorilla.Patch(destination, 'instance_value', gorilla.get_attribute(obj, 'instance_value')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'parent_value', gorilla.get_attribute(obj, 'parent_value')),
            gorilla.Patch(destination, 'to_value', gorilla.get_attribute(obj, 'to_value')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_3(self):
        def filter(name, value):
            return 'method' in name

        destination = tomodule
        obj = frommodule
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'unbound_class_method', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_method', gorilla.get_attribute(obj, 'unbound_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Class
        obj = frommodule.Class
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Parent
        obj = frommodule.Parent
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Child
        obj = frommodule.Child
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_4(self):
        def filter(name, value):
            return 'method' in name

        destination = tomodule
        obj = frommodule
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'function', gorilla.get_attribute(obj, 'function')),
            gorilla.Patch(destination, 'whatever', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method'), settings=gorilla.Settings(allow_hit=True))
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Class
        obj = frommodule.Class
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'whatever', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Parent
        obj = frommodule.Parent
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = tomodule.Child
        obj = frommodule.Child
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_5(self):
        destination = tomodule
        obj = frommodule

        gorilla.name('function')(gorilla.get_attribute(obj, 'Class'))
        gorilla.name('dummy_1')(gorilla.get_attribute(obj, 'Parent'))
        gorilla.name('dummy_2')(gorilla.get_attribute(obj, 'Child'))
        patches = gorilla.create_patches(destination, obj)

        expected_patches = [
            gorilla.Patch(destination, 'dummy_2', gorilla.get_attribute(obj, 'Child')),
            gorilla.Patch(destination, 'function', gorilla.get_attribute(obj, 'Class')),
            gorilla.Patch(destination, 'dummy_1', gorilla.get_attribute(obj, 'Parent')),
            gorilla.Patch(destination, 'function', gorilla.get_attribute(obj, 'function')),
            gorilla.Patch(destination, 'global_variable', gorilla.get_attribute(obj, 'global_variable')),
            gorilla.Patch(destination, 'whatever', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method'), settings=gorilla.Settings(allow_hit=True)),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_6(self):
        destination = tomodule.Class
        obj = frommodule.Class
        patches = gorilla.create_patches(destination, obj, filter=None,
                                         recursive=False, use_decorators=False)

        expected_patches = [
            gorilla.Patch(destination, name, value)
            for name, value in sorted(_iteritems(obj.__dict__))]

        self.assertEqual(patches, expected_patches)

    def test_find_patches_1(self):
        patches = gorilla.find_patches([tests.utils])
        expected_patches = [
            gorilla.Patch(tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class, 'class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            gorilla.Patch(tomodule.Class, 'whatever', gorilla.get_attribute(frommodule.Class, 'method')),
            gorilla.Patch(tomodule.Parent, 'value', gorilla.get_attribute(frommodule.Class, 'value')),
            gorilla.Patch(tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class.Inner, 'method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
            gorilla.Patch(tomodule, 'function', gorilla.get_attribute(frommodule, 'function')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
            gorilla.Patch(tomodule, 'function0', gorilla.get_attribute(subpackage, 'function')),
            gorilla.Patch(tomodule, 'function1', gorilla.get_attribute(module1, 'function')),
            gorilla.Patch(tomodule.Class, 'unbound_class_method', gorilla.get_attribute(module1, 'unbound_class_method')),
            gorilla.Patch(tomodule.Class, 'unbound_method', gorilla.get_attribute(module1, 'unbound_method')),
            gorilla.Patch(tomodule.Class, 'unbound_static_method', gorilla.get_attribute(module1, 'unbound_static_method')),
            gorilla.Patch(tomodule.Class, 'method1', gorilla.get_attribute(module1.Class, 'method')),
            gorilla.Patch(tomodule.Class, 'value1', gorilla.get_attribute(module1.Class, 'value')),
            gorilla.Patch(tomodule.Class, 'class_method2', gorilla.get_attribute(module2.Class, 'class_method')),
            gorilla.Patch(tomodule.Class, 'static_method2', gorilla.get_attribute(module2.Class, 'static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        patches = gorilla.find_patches([tests.utils], recursive=False)
        expected_patches = [
            gorilla.Patch(tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class, 'class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            gorilla.Patch(tomodule.Class, 'whatever', gorilla.get_attribute(frommodule.Class, 'method')),
            gorilla.Patch(tomodule.Parent, 'value', gorilla.get_attribute(frommodule.Class, 'value')),
            gorilla.Patch(tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class.Inner, 'method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
            gorilla.Patch(tomodule, 'function', gorilla.get_attribute(frommodule, 'function')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_find_patches_2(self):
        self.tearDown()

        patches = gorilla.find_patches([tests.utils])

        global frommodule, tomodule, subpackage, module1, module2
        frommodule = sys.modules[frommodule.__name__]
        tommodule = sys.modules[tomodule.__name__]
        subpackage = sys.modules[subpackage.__name__]
        module1 = sys.modules[module1.__name__]
        module2 = sys.modules[module2.__name__]

        expected_patches = [
            gorilla.Patch(tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class, 'class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            gorilla.Patch(tomodule.Class, 'whatever', gorilla.get_attribute(frommodule.Class, 'method')),
            gorilla.Patch(tomodule.Parent, 'value', gorilla.get_attribute(frommodule.Class, 'value')),
            gorilla.Patch(tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class.Inner, 'method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
            gorilla.Patch(tomodule, 'function', gorilla.get_attribute(frommodule, 'function')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
            gorilla.Patch(tomodule, 'function0', gorilla.get_attribute(subpackage, 'function')),
            gorilla.Patch(tomodule, 'function1', gorilla.get_attribute(module1, 'function')),
            gorilla.Patch(tomodule.Class, 'unbound_class_method', gorilla.get_attribute(module1, 'unbound_class_method')),
            gorilla.Patch(tomodule.Class, 'unbound_method', gorilla.get_attribute(module1, 'unbound_method')),
            gorilla.Patch(tomodule.Class, 'unbound_static_method', gorilla.get_attribute(module1, 'unbound_static_method')),
            gorilla.Patch(tomodule.Class, 'method1', gorilla.get_attribute(module1.Class, 'method')),
            gorilla.Patch(tomodule.Class, 'value1', gorilla.get_attribute(module1.Class, 'value')),
            gorilla.Patch(tomodule.Class, 'class_method2', gorilla.get_attribute(module2.Class, 'class_method')),
            gorilla.Patch(tomodule.Class, 'static_method2', gorilla.get_attribute(module2.Class, 'static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        patches = gorilla.find_patches([tests.utils], recursive=False)
        expected_patches = [
            gorilla.Patch(tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class, 'class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            gorilla.Patch(tomodule.Class, 'whatever', gorilla.get_attribute(frommodule.Class, 'method')),
            gorilla.Patch(tomodule.Parent, 'value', gorilla.get_attribute(frommodule.Class, 'value')),
            gorilla.Patch(tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(tomodule.Class.Inner, 'method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
            gorilla.Patch(tomodule, 'function', gorilla.get_attribute(frommodule, 'function')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
            gorilla.Patch(tomodule.Parent, 'method', gorilla.get_attribute(frommodule.Parent, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_get_attribute(self):
        self.assertIs(gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE'), frommodule.Class.__dict__['STATIC_VALUE'])
        self.assertIs(gorilla.get_attribute(frommodule.Class, '__init__'), frommodule.Class.__dict__['__init__'])
        self.assertIs(gorilla.get_attribute(frommodule.Class, 'value'), frommodule.Class.__dict__['value'])
        self.assertIs(gorilla.get_attribute(frommodule.Class, 'method'), frommodule.Class.__dict__['method'])
        self.assertIs(gorilla.get_attribute(frommodule.Class, 'class_method'), frommodule.Class.__dict__['class_method'])
        self.assertIs(gorilla.get_attribute(frommodule.Class, 'static_method'), frommodule.Class.__dict__['static_method'])
        self.assertIs(gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE'), frommodule.Parent.__dict__['STATIC_VALUE'])
        self.assertIs(gorilla.get_attribute(frommodule.Parent, '__init__'), frommodule.Parent.__dict__['__init__'])
        self.assertIs(gorilla.get_attribute(frommodule.Parent, 'method'), frommodule.Parent.__dict__['method'])
        self.assertIs(gorilla.get_attribute(frommodule.Child, 'STATIC_VALUE'), frommodule.Parent.__dict__['STATIC_VALUE'])
        self.assertIs(gorilla.get_attribute(frommodule.Child, '__init__'), frommodule.Child.__dict__['__init__'])
        self.assertIs(gorilla.get_attribute(frommodule.Child, 'method'), frommodule.Parent.__dict__['method'])

    def test_get_original_attribute(self):
        destination = tomodule.Class
        name = 'method'
        target = gorilla.get_attribute(destination, name)
        obj = gorilla.get_attribute(frommodule, 'unbound_method')
        settings = gorilla.Settings(allow_hit=True)
        patch = gorilla.Patch(destination, name, obj, settings=settings)

        gorilla.apply(patch)
        self.assertIs(_unfold(gorilla.get_original_attribute(destination, name)), target)

        gorilla.apply(patch)
        self.assertIs(_unfold(gorilla.get_original_attribute(destination, name)), target)

    def test_get_members_1(self):
        members = gorilla._get_members(frommodule)
        expected_members = [
            ('Child', gorilla.get_attribute(frommodule, 'Child')),
            ('Class', gorilla.get_attribute(frommodule, 'Class')),
            ('Parent', gorilla.get_attribute(frommodule, 'Parent')),
            ('function', gorilla.get_attribute(frommodule, 'function')),
            ('global_variable', gorilla.get_attribute(frommodule, 'global_variable')),
            ('unbound_class_method', gorilla.get_attribute(frommodule, 'unbound_class_method')),
            ('unbound_method', gorilla.get_attribute(frommodule, 'unbound_method')),
            ('unbound_static_method', gorilla.get_attribute(frommodule, 'unbound_static_method')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE')),
            ('child_value', gorilla.get_attribute(frommodule.Child, 'child_value')),
            ('from_value', gorilla.get_attribute(frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(frommodule.Parent, 'to_value')),
            ('Inner', frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(frommodule.Parent, 'to_value')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(frommodule.Class)
        expected_members = [
            ('Inner', frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(frommodule.Parent)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(frommodule.Parent, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(frommodule.Child)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE')),
            ('child_value', gorilla.get_attribute(frommodule.Child, 'child_value')),
            ('from_value', gorilla.get_attribute(frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(frommodule.Parent, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

    def test_get_members_2(self):
        members = gorilla._get_members(frommodule, traverse_bases=False)
        expected_members = [
            ('Child', gorilla.get_attribute(frommodule, 'Child')),
            ('Class', gorilla.get_attribute(frommodule, 'Class')),
            ('Parent', gorilla.get_attribute(frommodule, 'Parent')),
            ('function', gorilla.get_attribute(frommodule, 'function')),
            ('global_variable', gorilla.get_attribute(frommodule, 'global_variable')),
            ('unbound_class_method', gorilla.get_attribute(frommodule, 'unbound_class_method')),
            ('unbound_method', gorilla.get_attribute(frommodule, 'unbound_method')),
            ('unbound_static_method', gorilla.get_attribute(frommodule, 'unbound_static_method')),
            ('child_value', gorilla.get_attribute(frommodule.Child, 'child_value')),
            ('Inner', frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(frommodule.Parent, 'to_value')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(frommodule.Class, traverse_bases=False)
        expected_members = [
            ('Inner', frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(frommodule.Parent, traverse_bases=False)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(frommodule.Parent, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(frommodule.Child, traverse_bases=False)
        expected_members = [
            ('child_value', gorilla.get_attribute(frommodule.Child, 'child_value')),
        ]
        self.assertEqual(members, expected_members)

    def test_get_members_3(self):
        obj = frommodule
        members = gorilla._get_members(obj, recursive=False)
        expected_members = [
            ('Child', gorilla.get_attribute(obj, 'Child')),
            ('Class', gorilla.get_attribute(obj, 'Class')),
            ('Parent', gorilla.get_attribute(obj, 'Parent')),
            ('function', gorilla.get_attribute(obj, 'function')),
            ('global_variable', gorilla.get_attribute(obj, 'global_variable')),
            ('unbound_class_method', gorilla.get_attribute(obj, 'unbound_class_method')),
            ('unbound_method', gorilla.get_attribute(obj, 'unbound_method')),
            ('unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method')),
        ]
        self.assertEqual(members, expected_members)

        obj = frommodule.Class
        members = gorilla._get_members(obj, recursive=False)
        expected_members = [
            ('Inner', gorilla.get_attribute(obj, 'Inner')),
            ('STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(obj, 'class_method')),
            ('method', gorilla.get_attribute(obj, 'method')),
            ('static_method', gorilla.get_attribute(obj, 'static_method')),
            ('value', gorilla.get_attribute(obj, 'value')),
        ]
        self.assertEqual(members, expected_members)

        obj = frommodule.Parent
        members = gorilla._get_members(obj, recursive=False)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(obj, 'from_value')),
            ('instance_value', gorilla.get_attribute(obj, 'instance_value')),
            ('method', gorilla.get_attribute(obj, 'method')),
            ('parent_value', gorilla.get_attribute(obj, 'parent_value')),
            ('to_value', gorilla.get_attribute(obj, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

        obj = frommodule.Child
        members = gorilla._get_members(obj, recursive=False)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            ('child_value', gorilla.get_attribute(obj, 'child_value')),
            ('from_value', gorilla.get_attribute(obj, 'from_value')),
            ('instance_value', gorilla.get_attribute(obj, 'instance_value')),
            ('method', gorilla.get_attribute(obj, 'method')),
            ('parent_value', gorilla.get_attribute(obj, 'parent_value')),
            ('to_value', gorilla.get_attribute(obj, 'to_value')),
        ]
        self.assertEqual(members, expected_members)


if __name__ == '__main__':
    from tests.run import run
    run('__main__')
