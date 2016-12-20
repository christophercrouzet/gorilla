.. currentmodule:: gorilla

.. _overview:

Overview
========

Gorilla is a library providing a convenient approach to monkey patching.

The API revolves around the concept of patches, represented by the class
:class:`Patch`. This class can be used directly if the patching information are
only known at runtime but otherwise a set of decorators are available to make
the whole process more intuitive.

This recommended process consists in decorating a class or a descriptor with
the :func:`patch` decorator. This marks the decorated object as the attribute
value to use to patch a specified destination (either a module or a class). A
decorator :func:`patches` is also provided to create a patch for each member of
a class.

The objects marked with these two decorators are discoverable through the
:func:`find_patches` function and can be applied using the :func:`apply`
function.

When an attribute with the same name as the patch to apply already exists on
the destination, then a hit occurs which leads the existing attribute to be
optionally saved under another name and to become accessible through the
:func:`get_original_attribute` function. This ensures that the original
behaviour of an attribute can be preserved if needed.

The behaviour of the patching process can be modified for each patch by
overriding the default settings. See :class:`Patch`, and :class:`Settings`.

.. note::

   Both Python 2 and Python 3 versions are supported.
