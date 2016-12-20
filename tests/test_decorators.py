#!/usr/bin/env python

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import importlib
import unittest
import sys

import gorilla

from tests._testcase import GorillaTestCase
from tests.decorators import frommodule, tomodule


class DecoratorsTest(GorillaTestCase):

    def setUp(self):
        global frommodule, tomodule
        tomodule = importlib.import_module(tomodule.__name__)
        frommodule = importlib.import_module(frommodule.__name__)

    def tearDown(self):
        for module in [tomodule, frommodule]:
            if module.__name__ in sys.modules:
                del sys.modules[module.__name__]

    def test_patch_decorator_on_function(self):
        destination = tomodule
        obj = gorilla.get_attribute(frommodule, 'function')

        self.assertIs(gorilla.patch(destination)(obj), obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
        expected_patches = [
            (destination, 'function', obj),
        ]
        self.assertEqual(decorator_data.patches, [gorilla.Patch(destination, name, obj) for destination, name, obj in expected_patches])

    def test_patch_decorator_on_class(self):
        destination = tomodule
        obj = frommodule.Class

        self.assertIs(gorilla.patch(destination)(obj), obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
        expected_patches = [
            (destination, 'Class', obj),
        ]
        self.assertEqual(decorator_data.patches, [gorilla.Patch(destination, name, obj) for destination, name, obj in expected_patches])

    def test_patches_decorator_on_class(self):
        destination = tomodule.Class
        obj = frommodule.Class

        self.assertIs(gorilla.patches(destination)(obj), obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
        expected_patches = [
            (destination, 'STATIC_VALUE', obj),
            (destination, 'class_method', obj),
            (destination, 'method', obj),
            (destination, 'static_method', obj),
            (destination, 'value', obj),
            (destination.Inner, 'STATIC_VALUE', obj.Inner),
            (destination.Inner, 'method', obj.Inner),
        ]
        self.assertEqual(decorator_data.patches, [gorilla.Patch(destination, name, gorilla.get_attribute(source, name)) for destination, name, source in expected_patches])

    def test_destination_decorator(self):
        destination = tomodule.Class
        obj = frommodule.Class

        destination_override = tomodule.Parent
        gorilla.destination(destination_override)(gorilla.get_attribute(obj, 'class_method'))
        gorilla.destination(destination_override)(gorilla.get_attribute(obj, 'method'))
        gorilla.destination(destination_override)(gorilla.get_attribute(obj, 'value'))
        gorilla.patches(destination)(obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
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
        destination = tomodule.Class
        obj = frommodule.Class

        name_override = 'whatever'
        gorilla.name(name_override)(gorilla.get_attribute(obj, 'class_method'))
        gorilla.name(name_override)(gorilla.get_attribute(obj, 'static_method'))
        gorilla.name(name_override)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination)(obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
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

    def test_settings_decorator(self):
        destination = tomodule.Class
        obj = frommodule.Class

        settings_override = {'allow_hit': True}
        gorilla.settings(**settings_override)(gorilla.get_attribute(obj, 'static_method'))
        gorilla.settings(**settings_override)(gorilla.get_attribute(obj, 'value'))
        gorilla.settings(**settings_override)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination)(obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
        expected_patches = [
            gorilla.Patch(destination, 'STATIC_VALUE', gorilla.get_attribute(obj, 'STATIC_VALUE')),
            gorilla.Patch(destination, 'class_method', gorilla.get_attribute(obj, 'class_method')),
            gorilla.Patch(destination, 'method', gorilla.get_attribute(obj, 'method')),
            gorilla.Patch(destination, 'static_method', gorilla.get_attribute(obj, 'static_method'), settings=gorilla.Settings(allow_hit=True)),
            gorilla.Patch(destination, 'value', gorilla.get_attribute(obj, 'value'), settings=gorilla.Settings(allow_hit=True)),
            gorilla.Patch(destination.Inner, 'STATIC_VALUE', gorilla.get_attribute(obj.Inner, 'STATIC_VALUE')),
            gorilla.Patch(destination.Inner, 'method', gorilla.get_attribute(obj.Inner, 'method'), settings=gorilla.Settings(allow_hit=True)),
        ]
        self.assertEqual(decorator_data.patches, expected_patches)

    def test_filter_decorator(self):
        destination = tomodule.Class
        obj = frommodule.Class

        settings_override = {'allow_hit': True}
        gorilla.filter(True)(gorilla.get_attribute(obj, '__init__'))
        gorilla.filter(False)(gorilla.get_attribute(obj, 'class_method'))
        gorilla.filter(False)(gorilla.get_attribute(obj.Inner, 'method'))
        gorilla.patches(destination)(obj)

        decorator_data = getattr(obj, '_gorilla_decorator_data')
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
    unittest.main(verbosity=2)
