#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import importlib
import os
import sys

_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))

import gorilla

import tests.utils as _utils
import tests.utils.frommodule as _frommodule
import tests.utils.tomodule as _tomodule
import tests.utils.subpackage as _subpackage
import tests.utils.subpackage.module1 as _module1
import tests.utils.subpackage.module2 as _module2
from tests._testcase import GorillaTestCase


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


_MODULES = [
    ('_utils', _utils.__name__),
    ('_frommodule', _frommodule.__name__),
    ('_tomodule', _tomodule.__name__),
    ('_subpackage', _subpackage.__name__),
    ('_module1', _module1.__name__),
    ('_module2', _module2.__name__),
]


class UtilsTest(GorillaTestCase):

    def setUp(self):
        for module, path in _MODULES:
            globals()[module] = importlib.import_module(path)

    def tearDown(self):
        for module, path in _MODULES:
            if path in sys.modules:
                del sys.modules[path]

    def test_create_patches_1(self):
        destination = _tomodule
        obj = _frommodule
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

        destination = _tomodule.Class
        obj = _frommodule.Class
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

        destination = _tomodule.Parent
        obj = _frommodule.Parent
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

        destination = _tomodule.Child
        obj = _frommodule.Child
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
        destination = _tomodule
        obj = _frommodule
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

        destination = _tomodule.Class
        obj = _frommodule.Class
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

        destination = _tomodule.Parent
        obj = _frommodule.Parent
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

        destination = _tomodule.Child
        obj = _frommodule.Child
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

        destination = _tomodule
        obj = _frommodule
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'unbound_class_method', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_method', gorilla.get_attribute(obj, 'unbound_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = _tomodule.Class
        obj = _frommodule.Class
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = _tomodule.Parent
        obj = _frommodule.Parent
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = _tomodule.Child
        obj = _frommodule.Child
        patches = gorilla.create_patches(destination, obj, filter=filter,
                                         use_decorators=False)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_4(self):
        def filter(name, value):
            return 'method' in name

        destination = _tomodule
        obj = _frommodule
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'function', gorilla.get_attribute(obj, 'function')),
            gorilla.Patch(destination, 'whatever', gorilla.get_attribute(obj, 'unbound_class_method')),
            gorilla.Patch(destination, 'unbound_static_method', gorilla.get_attribute(obj, 'unbound_static_method'), settings=gorilla.Settings(allow_hit=True))
        ]
        self.assertEqual(patches, expected_patches)

        destination = _tomodule.Class
        obj = _frommodule.Class
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'whatever', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = _tomodule.Parent
        obj = _frommodule.Parent
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

        destination = _tomodule.Child
        obj = _frommodule.Child
        patches = gorilla.create_patches(destination, obj, filter=filter)
        expected_patches = [
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_create_patches_5(self):
        destination = _tomodule
        obj = _frommodule

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
        destination = _tomodule.Class
        obj = _frommodule.Class
        patches = gorilla.create_patches(destination, obj, filter=None,
                                         recursive=False, use_decorators=False)

        expected_patches = [
            gorilla.Patch(destination, name, value)
            for name, value in sorted(_iteritems(obj.__dict__))]

        self.assertEqual(patches, expected_patches)

    def test_find_patches_1(self):
        patches = gorilla.find_patches([_utils])
        expected_patches = [
            gorilla.Patch(_tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class, 'class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            gorilla.Patch(_tomodule.Class, 'whatever', gorilla.get_attribute(_frommodule.Class, 'method')),
            gorilla.Patch(_tomodule.Parent, 'value', gorilla.get_attribute(_frommodule.Class, 'value')),
            gorilla.Patch(_tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class.Inner, 'method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
            gorilla.Patch(_tomodule, 'function', gorilla.get_attribute(_frommodule, 'function')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            gorilla.Patch(_tomodule, 'function0', gorilla.get_attribute(_subpackage, 'function')),
            gorilla.Patch(_tomodule, 'function1', gorilla.get_attribute(_module1, 'function')),
            gorilla.Patch(_tomodule.Class, 'unbound_class_method', gorilla.get_attribute(_module1, 'unbound_class_method')),
            gorilla.Patch(_tomodule.Class, 'unbound_method', gorilla.get_attribute(_module1, 'unbound_method')),
            gorilla.Patch(_tomodule.Class, 'unbound_static_method', gorilla.get_attribute(_module1, 'unbound_static_method')),
            gorilla.Patch(_tomodule.Class, 'method1', gorilla.get_attribute(_module1.Class, 'method')),
            gorilla.Patch(_tomodule.Class, 'value1', gorilla.get_attribute(_module1.Class, 'value')),
            gorilla.Patch(_tomodule.Class, 'class_method2', gorilla.get_attribute(_module2.Class, 'class_method')),
            gorilla.Patch(_tomodule.Class, 'static_method2', gorilla.get_attribute(_module2.Class, 'static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        patches = gorilla.find_patches([_utils], recursive=False)
        expected_patches = [
            gorilla.Patch(_tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class, 'class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            gorilla.Patch(_tomodule.Class, 'whatever', gorilla.get_attribute(_frommodule.Class, 'method')),
            gorilla.Patch(_tomodule.Parent, 'value', gorilla.get_attribute(_frommodule.Class, 'value')),
            gorilla.Patch(_tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class.Inner, 'method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
            gorilla.Patch(_tomodule, 'function', gorilla.get_attribute(_frommodule, 'function')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_find_patches_2(self):
        global _utils
        self.tearDown()
        _utils = importlib.import_module(_utils.__name__)

        patches = gorilla.find_patches([_utils])
        self.setUp()

        expected_patches = [
            gorilla.Patch(_tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class, 'class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            gorilla.Patch(_tomodule.Class, 'whatever', gorilla.get_attribute(_frommodule.Class, 'method')),
            gorilla.Patch(_tomodule.Parent, 'value', gorilla.get_attribute(_frommodule.Class, 'value')),
            gorilla.Patch(_tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class.Inner, 'method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
            gorilla.Patch(_tomodule, 'function', gorilla.get_attribute(_frommodule, 'function')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            gorilla.Patch(_tomodule, 'function0', gorilla.get_attribute(_subpackage, 'function')),
            gorilla.Patch(_tomodule, 'function1', gorilla.get_attribute(_module1, 'function')),
            gorilla.Patch(_tomodule.Class, 'unbound_class_method', gorilla.get_attribute(_module1, 'unbound_class_method')),
            gorilla.Patch(_tomodule.Class, 'unbound_method', gorilla.get_attribute(_module1, 'unbound_method')),
            gorilla.Patch(_tomodule.Class, 'unbound_static_method', gorilla.get_attribute(_module1, 'unbound_static_method')),
            gorilla.Patch(_tomodule.Class, 'method1', gorilla.get_attribute(_module1.Class, 'method')),
            gorilla.Patch(_tomodule.Class, 'value1', gorilla.get_attribute(_module1.Class, 'value')),
            gorilla.Patch(_tomodule.Class, 'class_method2', gorilla.get_attribute(_module2.Class, 'class_method')),
            gorilla.Patch(_tomodule.Class, 'static_method2', gorilla.get_attribute(_module2.Class, 'static_method')),
        ]
        self.assertEqual(patches, expected_patches)

        patches = gorilla.find_patches([_utils], recursive=False)
        expected_patches = [
            gorilla.Patch(_tomodule.Class, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class, 'class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            gorilla.Patch(_tomodule.Class, 'whatever', gorilla.get_attribute(_frommodule.Class, 'method')),
            gorilla.Patch(_tomodule.Parent, 'value', gorilla.get_attribute(_frommodule.Class, 'value')),
            gorilla.Patch(_tomodule.Class.Inner, 'STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            gorilla.Patch(_tomodule.Class.Inner, 'method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
            gorilla.Patch(_tomodule, 'function', gorilla.get_attribute(_frommodule, 'function')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            gorilla.Patch(_tomodule.Parent, 'method', gorilla.get_attribute(_frommodule.Parent, 'method')),
        ]
        self.assertEqual(patches, expected_patches)

    def test_get_attribute(self):
        self.assertIs(gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE'), _frommodule.Class.__dict__['STATIC_VALUE'])
        self.assertIs(gorilla.get_attribute(_frommodule.Class, '__init__'), _frommodule.Class.__dict__['__init__'])
        self.assertIs(gorilla.get_attribute(_frommodule.Class, 'value'), _frommodule.Class.__dict__['value'])
        self.assertIs(gorilla.get_attribute(_frommodule.Class, 'method'), _frommodule.Class.__dict__['method'])
        self.assertIs(gorilla.get_attribute(_frommodule.Class, 'class_method'), _frommodule.Class.__dict__['class_method'])
        self.assertIs(gorilla.get_attribute(_frommodule.Class, 'static_method'), _frommodule.Class.__dict__['static_method'])
        self.assertIs(gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE'), _frommodule.Parent.__dict__['STATIC_VALUE'])
        self.assertIs(gorilla.get_attribute(_frommodule.Parent, '__init__'), _frommodule.Parent.__dict__['__init__'])
        self.assertIs(gorilla.get_attribute(_frommodule.Parent, 'method'), _frommodule.Parent.__dict__['method'])
        self.assertIs(gorilla.get_attribute(_frommodule.Child, 'STATIC_VALUE'), _frommodule.Parent.__dict__['STATIC_VALUE'])
        self.assertIs(gorilla.get_attribute(_frommodule.Child, '__init__'), _frommodule.Child.__dict__['__init__'])
        self.assertIs(gorilla.get_attribute(_frommodule.Child, 'method'), _frommodule.Parent.__dict__['method'])

    def test_get_original_attribute(self):
        destination = _tomodule.Class
        name = 'method'
        target = gorilla.get_attribute(destination, name)
        obj = gorilla.get_attribute(_frommodule, 'unbound_method')
        settings = gorilla.Settings(allow_hit=True)
        patch = gorilla.Patch(destination, name, obj, settings=settings)

        gorilla.apply(patch)
        self.assertIs(_unfold(gorilla.get_original_attribute(destination, name)), target)

    def test__get_members_1(self):
        members = gorilla._get_members(_frommodule)
        expected_members = [
            ('Child', gorilla.get_attribute(_frommodule, 'Child')),
            ('Class', gorilla.get_attribute(_frommodule, 'Class')),
            ('Parent', gorilla.get_attribute(_frommodule, 'Parent')),
            ('function', gorilla.get_attribute(_frommodule, 'function')),
            ('global_variable', gorilla.get_attribute(_frommodule, 'global_variable')),
            ('unbound_class_method', gorilla.get_attribute(_frommodule, 'unbound_class_method')),
            ('unbound_method', gorilla.get_attribute(_frommodule, 'unbound_method')),
            ('unbound_static_method', gorilla.get_attribute(_frommodule, 'unbound_static_method')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE')),
            ('child_value', gorilla.get_attribute(_frommodule.Child, 'child_value')),
            ('from_value', gorilla.get_attribute(_frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(_frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(_frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(_frommodule.Parent, 'to_value')),
            ('Inner', _frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(_frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(_frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(_frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(_frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(_frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(_frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(_frommodule.Parent, 'to_value')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(_frommodule.Class)
        expected_members = [
            ('Inner', _frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(_frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(_frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(_frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(_frommodule.Parent)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(_frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(_frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(_frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(_frommodule.Parent, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(_frommodule.Child)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE')),
            ('child_value', gorilla.get_attribute(_frommodule.Child, 'child_value')),
            ('from_value', gorilla.get_attribute(_frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(_frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(_frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(_frommodule.Parent, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

    def test__get_members_2(self):
        members = gorilla._get_members(_frommodule, traverse_bases=False)
        expected_members = [
            ('Child', gorilla.get_attribute(_frommodule, 'Child')),
            ('Class', gorilla.get_attribute(_frommodule, 'Class')),
            ('Parent', gorilla.get_attribute(_frommodule, 'Parent')),
            ('function', gorilla.get_attribute(_frommodule, 'function')),
            ('global_variable', gorilla.get_attribute(_frommodule, 'global_variable')),
            ('unbound_class_method', gorilla.get_attribute(_frommodule, 'unbound_class_method')),
            ('unbound_method', gorilla.get_attribute(_frommodule, 'unbound_method')),
            ('unbound_static_method', gorilla.get_attribute(_frommodule, 'unbound_static_method')),
            ('child_value', gorilla.get_attribute(_frommodule.Child, 'child_value')),
            ('Inner', _frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(_frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(_frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(_frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(_frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(_frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(_frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(_frommodule.Parent, 'to_value')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(_frommodule.Class, traverse_bases=False)
        expected_members = [
            ('Inner', _frommodule.Class.Inner),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class, 'STATIC_VALUE')),
            ('class_method', gorilla.get_attribute(_frommodule.Class, 'class_method')),
            ('method', gorilla.get_attribute(_frommodule.Class, 'method')),
            ('static_method', gorilla.get_attribute(_frommodule.Class, 'static_method')),
            ('value', gorilla.get_attribute(_frommodule.Class, 'value')),
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Class.Inner, 'STATIC_VALUE')),
            ('method', gorilla.get_attribute(_frommodule.Class.Inner, 'method')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(_frommodule.Parent, traverse_bases=False)
        expected_members = [
            ('STATIC_VALUE', gorilla.get_attribute(_frommodule.Parent, 'STATIC_VALUE')),
            ('from_value', gorilla.get_attribute(_frommodule.Parent, 'from_value')),
            ('instance_value', gorilla.get_attribute(_frommodule.Parent, 'instance_value')),
            ('method', gorilla.get_attribute(_frommodule.Parent, 'method')),
            ('parent_value', gorilla.get_attribute(_frommodule.Parent, 'parent_value')),
            ('to_value', gorilla.get_attribute(_frommodule.Parent, 'to_value')),
        ]
        self.assertEqual(members, expected_members)

        members = gorilla._get_members(_frommodule.Child, traverse_bases=False)
        expected_members = [
            ('child_value', gorilla.get_attribute(_frommodule.Child, 'child_value')),
        ]
        self.assertEqual(members, expected_members)

    def test__get_members_3(self):
        obj = _frommodule
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

        obj = _frommodule.Class
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

        obj = _frommodule.Parent
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

        obj = _frommodule.Child
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
