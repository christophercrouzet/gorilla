#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import collections
import importlib
import itertools
import os
import sys

_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))

import gorilla

import tests.core as _core
import tests.core.frommodule as _frommodule
import tests.core.tomodule as _tomodule
from tests._testcase import GorillaTestCase


_MODULES = [
    ('_core', _core.__name__),
    ('_frommodule', _frommodule.__name__),
    ('_tomodule', _tomodule.__name__),
]

_CLS_REFERENCES = {
    'Class': 'Class',
    'Class.Inner': 'Class.Inner',
    'Parent': 'Parent',
    'Child': 'Parent',
}


def _list_attribute_paths(obj):
    attributes = []
    stack = collections.deque(((obj, []),))
    while stack:
        obj, parent_path = stack.popleft()
        for attribute in getattr(obj, '__all__', []):
            path = parent_path + [attribute]
            stack.append((getattr(obj, attribute), path))
            attributes.append('.'.join(path))

    return attributes


def _get_attribute_from_path(module, path):
    if path == '':
        return module

    obj = module
    for part in path.split('.'):
        obj = gorilla.get_attribute(obj, part)

    return obj


def _split_attribute_path(path):
    parts = path.split('.')
    return ('.'.join(parts[:-1]), parts[-1])


class CoreTest(GorillaTestCase):

    def setUp(self):
        for module, path in _MODULES:
            globals()[module] = importlib.import_module(path)

    def tearDown(self):
        for module, path in _MODULES:
            if path in sys.modules:
                del sys.modules[path]

    def test_settings(self):
        settings_1 = gorilla.Settings()
        settings_2 = gorilla.Settings(allow_hit=False, store_hit=True)
        self.assertEqual(settings_1, settings_2)
        self.assertNotEqual(settings_1, {'allow_hit': False, 'store_hit': True})

        settings_1.allow_hit = True
        self.assertNotEqual(settings_1, settings_2)

        settings_2.allow_hit = True
        self.assertEqual(settings_1, settings_2)

        settings_1.some_value = 123
        self.assertNotEqual(settings_1, settings_2)

        settings_2.some_value = 123
        self.assertEqual(settings_1, settings_2)

    def test_patch(self):
        patch_1 = gorilla.Patch(_tomodule, 'dummy', _frommodule.function)
        patch_2 = gorilla.Patch(_tomodule, 'dummy', _frommodule.function, settings=None)
        self.assertEqual(patch_1, patch_2)
        self.assertNotEqual(patch_1, {'destination': _tomodule, 'name': 'dummy', 'obj': _frommodule.function, 'settings': None})

        patch_1.name = 'function'
        self.assertNotEqual(patch_1, patch_2)

        patch_2.name = 'function'
        self.assertEqual(patch_1, patch_2)

        patch_1.some_value = 123
        self.assertNotEqual(patch_1, patch_2)

        patch_2.some_value = 123
        self.assertEqual(patch_1, patch_2)

    def test_apply_patch_no_hit(self):
        name = 'dummy'
        settings = gorilla.Settings()

        source_paths = [''] + _list_attribute_paths(_frommodule)
        target_paths = _list_attribute_paths(_tomodule)

        branch_count = 0

        # Retrieve the destinations in two passes instead of directly using a
        # set in order to preserve the ordering.
        seen = set()
        destination_paths = [_split_attribute_path(path)[0]
                             for path in target_paths]
        destination_paths = [path for path in destination_paths
                             if path not in seen and seen.add(path) is None]
        combinations = itertools.product(source_paths, destination_paths)
        for source_path, destination_path in combinations:
            self.setUp()

            destination = _get_attribute_from_path(_tomodule, destination_path)
            obj = _get_attribute_from_path(_frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            gorilla.apply(patch)
            self.assertIs(destination, _get_attribute_from_path(_tomodule, destination_path))

            result = gorilla.get_attribute(destination, name)
            self.assertIs(result, obj)

            if source_path == '':
                branch_count += 1
                self.assertEqual(result.global_variable, "frommodule.global_variable")
                self.assertEqual(result.function(), "frommodule.function (frommodule.Class.STATIC_VALUE)")
                self.assertEqual(result.Class.STATIC_VALUE, "frommodule.Class.STATIC_VALUE")
                self.assertEqual(result.Class.Inner.STATIC_VALUE, "frommodule.Class.Inner.STATIC_VALUE")
                self.assertEqual(result.Parent.STATIC_VALUE, "frommodule.Parent.STATIC_VALUE")
                self.assertEqual(result.Child.STATIC_VALUE, "frommodule.Parent.STATIC_VALUE")
            elif source_path == 'global_variable':
                branch_count += 1
                self.assertEqual(result, "frommodule.global_variable")
            elif source_path == 'function':
                branch_count += 1
                self.assertEqual(result(), "frommodule.function (frommodule.Class.STATIC_VALUE)")
            elif source_path == 'unbound_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.unbound_method (tomodule.%s.STATIC_VALUE, tomodule.%s.instance_value)" % ((_CLS_REFERENCES[destination_path],) * 2))
            elif source_path == 'unbound_class_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.unbound_class_method (tomodule.%s.STATIC_VALUE)" % (_CLS_REFERENCES[destination_path],))
            elif source_path == 'unbound_static_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.unbound_static_method (frommodule.Class.STATIC_VALUE)")
            elif source_path == 'Class':
                branch_count += 1
                self.assertEqual(result.STATIC_VALUE, "frommodule.Class.STATIC_VALUE")
            elif source_path == 'Class.Inner':
                branch_count += 1
                self.assertEqual(result.STATIC_VALUE, "frommodule.Class.Inner.STATIC_VALUE")
            elif source_path == 'Class.value':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    instance = destination()
                    self.assertEqual(getattr(instance, name), "frommodule.Class.value.getter (tomodule.%s.instance_value)"  % (_CLS_REFERENCES[destination_path],))
                    setattr(instance, name, 'hello')
                    self.assertEqual(getattr(instance, name), "frommodule.Class.value.getter (hello)")
            elif source_path == 'Class.method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.Class.method (tomodule.%s.STATIC_VALUE, tomodule.%s.instance_value)" % ((_CLS_REFERENCES[destination_path],) * 2))
            elif source_path == 'Class.class_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.Class.class_method (tomodule.%s.STATIC_VALUE)" % (_CLS_REFERENCES[destination_path],))
            elif source_path == 'Class.static_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.Class.static_method (frommodule.Class.STATIC_VALUE)")
            elif source_path == 'Parent':
                branch_count += 1
                self.assertEqual(result.__slots__, ('instance_value', 'parent_value', 'to_value', 'from_value'))
                self.assertEqual(result().parent_value, "frommodule.Parent.parent_value")
                self.assertEqual(result().method(), "frommodule.Parent.method (frommodule.Parent.instance_value)")
            elif source_path == 'Parent.method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.Parent.method (tomodule.%s.instance_value)" % (_CLS_REFERENCES[destination_path],))
            elif source_path == 'Child':
                branch_count += 1
                self.assertEqual(result.__slots__, ('child_value',))
                self.assertEqual(result().parent_value, "frommodule.Parent.parent_value")
                self.assertEqual(result().child_value, "frommodule.Child.child_value")
                self.assertEqual(result().method(), "frommodule.Parent.method (frommodule.Parent.instance_value)")
            elif source_path == 'Child.method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.Parent.method (tomodule.%s.instance_value)" % (_CLS_REFERENCES[destination_path],))

            self.tearDown()

        # Make sure that all test branches are covered.
        self.assertEqual(branch_count, 116)

    def test_apply_patch_with_hit_1(self):
        settings = gorilla.Settings()

        source_paths = [''] + _list_attribute_paths(_frommodule)
        target_paths = _list_attribute_paths(_tomodule)
        combinations = itertools.product(source_paths, target_paths)
        for source_path, target_path in combinations:
            self.setUp()

            destination_path, name = _split_attribute_path(target_path)
            destination = _get_attribute_from_path(_tomodule, destination_path)
            obj = _get_attribute_from_path(_frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            self.assertRaises(RuntimeError, gorilla.apply, patch)

            self.tearDown()

    def test_apply_patch_with_hit_2(self):
        settings = gorilla.Settings(allow_hit=True)

        branch_count = 0

        source_paths = [''] + _list_attribute_paths(_frommodule)
        target_paths = _list_attribute_paths(_tomodule)
        combinations = itertools.product(source_paths, target_paths)
        for source_path, target_path in combinations:
            self.setUp()

            destination_path, name = _split_attribute_path(target_path)
            destination = _get_attribute_from_path(_tomodule, destination_path)
            target = gorilla.get_attribute(destination, name)
            obj = _get_attribute_from_path(_frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            gorilla.apply(patch)
            self.assertIs(destination, _get_attribute_from_path(_tomodule, destination_path))

            result = gorilla.get_attribute(destination, name)
            self.assertIs(result, obj)

            if source_path == '':
                branch_count += 1
                self.assertEqual(result.global_variable, "frommodule.global_variable")
                self.assertEqual(result.function(), "frommodule.function (frommodule.Class.STATIC_VALUE)")
                self.assertEqual(result.Class.STATIC_VALUE, "frommodule.Class.STATIC_VALUE")
                self.assertEqual(result.Class.Inner.STATIC_VALUE, "frommodule.Class.Inner.STATIC_VALUE")
                self.assertEqual(result.Parent.STATIC_VALUE, "frommodule.Parent.STATIC_VALUE")
                self.assertEqual(result.Child.STATIC_VALUE, "frommodule.Parent.STATIC_VALUE")
            elif source_path == 'global_variable':
                branch_count += 1
                self.assertEqual(result, "frommodule.global_variable")
                if destination_path in _CLS_REFERENCES and name in ('STATIC_VALUE',):
                    branch_count += 1
                    self.assertEqual(destination.STATIC_VALUE, "frommodule.global_variable")

                if target_path == 'Class.STATIC_VALUE':
                    branch_count += 1
                    self.assertEqual(destination.class_method(), "tomodule.Class.class_method (frommodule.global_variable)")
                    self.assertEqual(destination.static_method(), "tomodule.Class.static_method (frommodule.global_variable)")
            elif source_path == 'function':
                branch_count += 1
                self.assertEqual(result(), "frommodule.function (frommodule.Class.STATIC_VALUE)")
            elif source_path == 'unbound_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('STATIC_VALUE', '__init__'):
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.unbound_method (tomodule.%s.STATIC_VALUE, tomodule.%s.instance_value)" % ((_CLS_REFERENCES[destination_path],) * 2))
            elif source_path == 'unbound_class_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('STATIC_VALUE',):
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.unbound_class_method (tomodule.%s.STATIC_VALUE)" % (_CLS_REFERENCES[destination_path],))
            elif source_path == 'unbound_static_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.unbound_static_method (frommodule.Class.STATIC_VALUE)")
            elif source_path == 'Class':
                branch_count += 1
                self.assertEqual(result.STATIC_VALUE, "frommodule.Class.STATIC_VALUE")
            elif source_path == 'Class.Inner':
                branch_count += 1
                self.assertEqual(result.STATIC_VALUE, "frommodule.Class.Inner.STATIC_VALUE")
            elif source_path == 'Class.value':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('__init__',):
                    branch_count += 1
                    instance = destination()
                    self.assertEqual(getattr(instance, name), "frommodule.Class.value.getter (tomodule.%s.instance_value)"  % (_CLS_REFERENCES[destination_path],))
                    setattr(instance, name, 'hello')
                    self.assertEqual(getattr(instance, name), "frommodule.Class.value.getter (hello)")
            elif source_path == 'Class.method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('STATIC_VALUE', '__init__'):
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.Class.method (tomodule.%s.STATIC_VALUE, tomodule.%s.instance_value)" % ((_CLS_REFERENCES[destination_path],) * 2))
            elif source_path == 'Class.class_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('STATIC_VALUE',):
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.Class.class_method (tomodule.%s.STATIC_VALUE)" % (_CLS_REFERENCES[destination_path],))
            elif source_path == 'Class.static_method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES:
                    branch_count += 1
                    self.assertEqual(getattr(destination, name)(), "frommodule.Class.static_method (frommodule.Class.STATIC_VALUE)")
            elif source_path == 'Parent':
                branch_count += 1
                self.assertEqual(result.__slots__, ('instance_value', 'parent_value', 'to_value', 'from_value'))
                self.assertEqual(result().parent_value, "frommodule.Parent.parent_value")
                self.assertEqual(result().method(), "frommodule.Parent.method (frommodule.Parent.instance_value)")
            elif source_path == 'Parent.method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('__init__',):
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.Parent.method (tomodule.%s.instance_value)" % (_CLS_REFERENCES[destination_path],))
            elif source_path == 'Child':
                branch_count += 1
                self.assertEqual(result.__slots__, ('child_value',))
                self.assertEqual(result().parent_value, "frommodule.Parent.parent_value")
                self.assertEqual(result().child_value, "frommodule.Child.child_value")
                self.assertEqual(result().method(), "frommodule.Parent.method (frommodule.Parent.instance_value)")
            elif source_path == 'Child.method':
                branch_count += 1
                if destination_path in _CLS_REFERENCES and name not in ('__init__',):
                    branch_count += 1
                    self.assertEqual(getattr(destination(), name)(), "frommodule.Parent.method (tomodule.%s.instance_value)" % (_CLS_REFERENCES[destination_path],))

            self.tearDown()

        # Make sure that all test branches are covered.
        self.assertEqual(branch_count, 427)

    def test_apply_patch_with_hit_3(self):
        settings = gorilla.Settings(allow_hit=True, store_hit=False)

        source_paths = [''] + _list_attribute_paths(_frommodule)
        target_paths = _list_attribute_paths(_tomodule)
        combinations = itertools.product(source_paths, target_paths)
        for source_path, target_path in combinations:
            self.setUp()

            destination_path, name = _split_attribute_path(target_path)
            destination = _get_attribute_from_path(_tomodule, destination_path)
            obj = _get_attribute_from_path(_frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            gorilla.apply(patch)
            self.assertIs(destination, _get_attribute_from_path(_tomodule, destination_path))

            result = gorilla.get_attribute(destination, name)
            self.assertIs(result, obj)

            self.assertRaises(AttributeError, gorilla.get_original_attribute, destination, name)

            self.tearDown()

    def test_revert_patch(self):
        self.setUp()

        settings = gorilla.Settings(allow_hit=True)
        destination = _tomodule
        obj = _frommodule.global_variable

        patch = gorilla.Patch(destination, 'dummy', obj, settings=settings)
        gorilla.apply(patch)
        self.assertEqual(_tomodule.dummy, "frommodule.global_variable")
        gorilla.revert(patch)
        self.assertRaises(AttributeError, getattr, _tomodule, 'dummy')


        patch = gorilla.Patch(destination, 'global_variable', obj, settings=settings)
        gorilla.apply(patch)
        self.assertEqual(_tomodule.global_variable, "frommodule.global_variable")
        gorilla.revert(patch)
        self.assertEqual(_tomodule.global_variable, "tomodule.global_variable")

        self.tearDown()

    def test_stack_patches(self):
        self.setUp()

        settings = gorilla.Settings(allow_hit=True)
        destination = _tomodule

        patch = gorilla.Patch(_tomodule, 'stack', _frommodule.stack_1, settings=settings)
        gorilla.apply(patch, id='first')

        patch = gorilla.Patch(_tomodule, 'stack', _frommodule.stack_2, settings=settings)
        gorilla.apply(patch, id='second')

        self.assertEqual(_tomodule.stack(), ("blue", "white", "red"))

        self.tearDown()


if __name__ == '__main__':
    from tests.run import run
    run('__main__')
