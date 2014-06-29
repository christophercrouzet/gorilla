.. _overview:

Overview
========

Gorilla is a library that provides a convenient approach to
:term:`monkey patching`.

The API revolves around the concept of
:term:`extension`\ s, represented by the class
:class:`~gorilla.extension.Extension`. This class is useful to be used directly
if the patching details are to be only known at runtime but otherwise a set of
decorators are available to make the whole process straightforward.

This process consists in decorating a class or a :term:`descriptor`
with the :func:`~gorilla.decorators.patch` decorator. This marks that object as
being an :term:`extension` to use to :term:`patch` a specified target
(either a module or a class).

The :term:`extension`\ s marked with the :func:`~gorilla.decorators.patch`
decorator are discoverable with the help of the
:meth:`~gorilla.extensionsregistrar.ExtensionsRegistrar.register_extensions`
class method. A breadth-first scan is performed recursively on the packages
and modules provided to find any extension defined.

When an attribute with the same name as the :term:`extension` to apply
already exists on the target, then the existing attribute is saved under
another name and becomes callable from within the extension's code through the
:func:`~gorilla.utils.get_original_attribute` function. This ensures that the
original behavior of an attribute can be preserved if needed.

The behavior of the patching process can be changed by overriding the default
settings to be found in the class :class:`~gorilla.settings.Settings`. See
:class:`~gorilla.extension.Extension` and
:func:`~gorilla.extensionsregistrar.ExtensionsRegistrar.register_extensions`.

.. note::
   
   The supported versions of Python are 2.6, 2.7, 3.3 and 3.4.
