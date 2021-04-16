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

import tests.decorators as _decorators
import tests.decorators.frommodule as _frommodule
import tests.decorators.tomodule as _tomodule
from tests._testcase import GorillaTestCase


_MODULES = [
    ('_decorators', _decorators.__name__),
    ('_frommodule', _frommodule.__name__),
    ('_tomodule', _tomodule.__name__),
]


class DecoratorsTest(GorillaTestCase):

    def setUp(self):
        for module, path in _MODULES:
            globals()[module] = importlib.import_module(path)

    def tearDown(self):
        for module, path in _MODULES:
            if path in sys.modules:
                del sys.modules[path]

    def test_patch_decorator_on_function(self):
        destination = _tomodule
        obj = gorilla.get_attribute(_frommodule, 'function')

        self.assertIs(gorilla.patch(destination)(obj), obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'function', obj),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_patch_decorator_on_class(self):
        destination = _tomodule
        obj = _frommodule.Class

        self.assertIs(gorilla.patch(destination)(obj), obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'Class', obj),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_patch_decorator(self):
        destination = _tomodule
        obj = gorilla.get_attribute(_frommodule, 'function')

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        self.assertIs(gorilla.patch(destination, settings=settings)(obj), obj)
        settings.allow_hit = False
        settings.store_hit = False

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'function', obj, gorilla.Settings(allow_hit=True, store_hit=True)),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_patches_decorator_on_class(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        self.assertIs(gorilla.patches(destination)(obj), obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value')),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method')),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_patches_decorator(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        self.assertIs(gorilla.patches(destination, settings=settings)(obj), obj)
        settings.allow_hit = False
        settings.store_hit = False

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method'), settings=gorilla.Settings(allow_hit=True, store_hit=True)),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_destination_decorator(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        destination_override = _tomodule.Parent
        gorilla.destination(destination_override)(gorilla.get_attribute(obj, 'class_method'))
        gorilla.destination(destination_override)(gorilla.get_attribute(obj, 'method'))
        gorilla.destination(destination_override)(gorilla.get_attribute(obj, 'value'))
        gorilla.patches(destination)(obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination_override, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination_override, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
            gorilla.Patch(destination_override, 'value', gorilla.get_attribute(obj, 'value')),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method')),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_name_decorator(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        name_override = 'whatever'
        gorilla.name(name_override)(gorilla.get_attribute(obj, 'class_method'))
        gorilla.name(name_override)(gorilla.get_attribute(obj, 'static_method'))
        gorilla.name(name_override)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination)(obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, name_override, gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, name_override, gorilla.get_attribute(obj, 'static_method')),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value')),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Inner, name_override, gorilla.get_attribute(obj.Inner, 'method')),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_settings_decorator_1(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        gorilla.settings(some_value=123)(gorilla.get_attribute(obj, 'method'))
        gorilla.settings(allow_hit=True)(gorilla.get_attribute(obj, 'static_method'))
        gorilla.settings(store_hit=False)(gorilla.get_attribute(obj, 'value'))
        gorilla.settings(allow_hit=True, store_hit=False)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination)(obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method'), settings=gorilla.Settings(some_value=123)),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method'), settings=gorilla.Settings(allow_hit=True)),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value'), settings=gorilla.Settings(store_hit=False)),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method'), settings=gorilla.Settings(allow_hit=True, store_hit=False)),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_settings_decorator_2(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        gorilla.settings(some_value=123)(gorilla.get_attribute(obj, 'method'))
        gorilla.settings(allow_hit=False)(gorilla.get_attribute(obj, 'static_method'))
        gorilla.settings(store_hit=True)(gorilla.get_attribute(obj, 'value'))
        gorilla.settings(allow_hit=False, store_hit=True)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination, settings=gorilla.Settings(allow_hit=True, store_hit=False))(obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE'), settings=gorilla.Settings(allow_hit=True, store_hit=False)),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method'), settings=gorilla.Settings(allow_hit=True, store_hit=False)),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method'), settings=gorilla.Settings(allow_hit=True, some_value=123, store_hit=False)),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method'), settings=gorilla.Settings(store_hit=False)),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value'), settings=gorilla.Settings(allow_hit=True)),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE'), settings=gorilla.Settings(allow_hit=True, store_hit=False)),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method'), settings=gorilla.Settings(allow_hit=False, store_hit=True)),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_filter_decorator(self):
        destination = _tomodule.Class
        obj = _frommodule.Class

        gorilla.filter(True)(gorilla.get_attribute(obj, '__init__'))
        gorilla.filter(False)(gorilla.get_attribute(obj, 'class_method'))
        gorilla.filter(False)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination)(obj)

        decorator_data = gorilla.get_decorator_data(obj)
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, '__init__', gorilla.get_attribute(obj, '__init__')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method')),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value')),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)


if __name__ == '__main__':
    from tests.run import run
    run('__main__')
