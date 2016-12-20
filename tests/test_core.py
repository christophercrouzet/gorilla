#!/usr/bin/env python

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import collections
import importlib
import itertools
import unittest
import sys

import gorilla

from tests._testcase import GorillaTestCase
from tests.core import frommodule, tomodule


_MODULES = [frommodule, tomodule]

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
        global frommodule, tomodule
        tomodule = importlib.import_module(tomodule.__name__)
        frommodule = importlib.import_module(frommodule.__name__)

    def tearDown(self):
        for module in [tomodule, frommodule]:
            if module.__name__ in sys.modules:
                del sys.modules[module.__name__]

    def test_apply_patch_no_hit(self):
        name = 'dummy'
        settings = gorilla.Settings()

        source_paths = [''] + _list_attribute_paths(frommodule)
        target_paths = _list_attribute_paths(tomodule)

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

            destination = _get_attribute_from_path(tomodule, destination_path)
            obj = _get_attribute_from_path(frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            gorilla.apply(patch)
            self.assertIs(destination, _get_attribute_from_path(tomodule, destination_path))

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

        source_paths = [''] + _list_attribute_paths(frommodule)
        target_paths = _list_attribute_paths(tomodule)
        combinations = itertools.product(source_paths, target_paths)
        for source_path, target_path in combinations:
            self.setUp()

            destination_path, name = _split_attribute_path(target_path)
            destination = _get_attribute_from_path(tomodule, destination_path)
            obj = _get_attribute_from_path(frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            self.assertRaises(RuntimeError, gorilla.apply, patch)

            self.tearDown()

    def test_apply_patch_with_hit_2(self):
        settings = gorilla.Settings(allow_hit=True)

        branch_count = 0

        source_paths = [''] + _list_attribute_paths(frommodule)
        target_paths = _list_attribute_paths(tomodule)
        combinations = itertools.product(source_paths, target_paths)
        for source_path, target_path in combinations:
            self.setUp()

            destination_path, name = _split_attribute_path(target_path)
            destination = _get_attribute_from_path(tomodule, destination_path)
            target = gorilla.get_attribute(destination, name)
            obj = _get_attribute_from_path(frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            gorilla.apply(patch)
            self.assertIs(destination, _get_attribute_from_path(tomodule, destination_path))

            result = gorilla.get_attribute(destination, name)
            self.assertIs(result, obj)

            # `gorilla.get_original_attribute` cannot be used here because it
            # could return a bounded method, which would not compare as
            # expected.
            original = gorilla.get_attribute(destination,
                                             '_gorilla_original_%s' % (name,))
            self.assertIs(original, target)
            self.assertIsNot(original, result)

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

        source_paths = [''] + _list_attribute_paths(frommodule)
        target_paths = _list_attribute_paths(tomodule)
        combinations = itertools.product(source_paths, target_paths)
        for source_path, target_path in combinations:
            self.setUp()

            destination_path, name = _split_attribute_path(target_path)
            destination = _get_attribute_from_path(tomodule, destination_path)
            obj = _get_attribute_from_path(frommodule, source_path)
            patch = gorilla.Patch(destination, name, obj, settings=settings)
            gorilla.apply(patch)
            self.assertIs(destination, _get_attribute_from_path(tomodule, destination_path))

            result = gorilla.get_attribute(destination, name)
            self.assertIs(result, obj)

            self.assertRaises(AttributeError, gorilla.get_original_attribute, destination, name)

            self.tearDown()


if __name__ == '__main__':
    unittest.main(verbosity=2)
