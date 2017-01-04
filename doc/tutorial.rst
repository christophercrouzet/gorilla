.. currentmodule:: gorilla

.. _tutorial:

Tutorial
========

In the end Gorilla is nothing more than a fancy wrapper around Python's
|setattr()|_ function and thus requires to define patches, represented by the
class :class:`Patch`, containing the destination object, the attribute name at
the destination, and the actual value to set.

The :class:`Patch` class can be used directly if the patching information are
only known at runtime, as described in the section :ref:`dynamic_patching`, but
otherwise a set of decorators are available to make the whole process more
intuitive and convenient.

The recommended approach involving decorators is to be done in two steps:

   * create a :ref:`single patch <create_single_patch>` with the :func:`patch`
     decorator and/or :ref:`multiple patches <create_multiple_patches>` using
     :func:`patches`.
   * :ref:`find and apply the patches <find_and_apply_patches>` through the
     :func:`find_patches` and :func:`apply` functions.


.. _create_single_patch:

Creating a Single Patch
-----------------------

In order to make a function ``my_function()`` available from within a
third-party module ``destination``, the first step is to create a new patch by
decorating our function:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patch(destination)
   ... def my_function():
   ...     print("Hello world!")


This step only creates the :class:`Patch` object containing the patch
information but does not inject the function into the destination module just
yet. The :func:`apply` function needs to be called for that to happen, as shown
in the section :ref:`find_and_apply_patches`.

The defaut behaviour is for the patch to inject the function at the destination
using the name of the decorated object, that is ``'my_function'``. If a
different name is desired but changing the function name is not possible, then
it can be done via the parameter `name`:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patch(destination, name='better_function')
   ... def my_function():
   ...     print("Hello world!")


After applying the patch, the function will become accessible through a call to
``destination.better_function()``.

A patch's destination can not only be a module as shown above, but also an
existing class:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patch(destination.Class)
   ... def my_method(self):
   ...     print("Hello")
   >>> @gorilla.patch(destination.Class)
   ... @classmethod
   ... def my_class_method(cls):
   ...     print("world!")


.. _create_multiple_patches:

Creating Multiple Patches at Once
---------------------------------

As the number of patches grows, the process of defining a decorator for each
individual patch can quickly become cumbersome. Instead, another decorator
:func:`patches` is available to create a batch of patches
(tongue-twister challenge: repeat "batch of patches" 10 times):

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patches(destination.Class)
   ... class MyClass(object):
   ...     def method(self):
   ...         print("Hello")
   ...     @classmethod
   ...     def class_method(cls):
   ...         print("world")
   ...     @staticmethod
   ...     def static_method():
   ...         print("!")


The :func:`patches` decorator iterates through all the members of the
decorated class, by default filtered using the :func:`default_filter` function,
while creating a patch for each of them.

Each patch created in this manner inherits the properties defined by the root
decorator but it is still possible to override them using any of the
:func:`destination`, :func:`name`, :func:`settings`, and :func:`filter`
modifier decorators:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patches(destination.Class)
   ... class MyClass(object):
   ...     @gorilla.name('better_method')
   ...     def method(self):
   ...         print("Hello")
   ...     @gorilla.settings(allow_hit=True)
   ...     @classmethod
   ...     def class_method(cls):
   ...         print("world")
   ...     @gorilla.filter(False)
   ...     @staticmethod
   ...     def static_method():
   ...         print("!")


In the example above, the method's name is overriden to ``'better_method'``,
the class method is allowed to overwrite an attribute with the same name at the
destination, and the static method is to be filtered out during the discovery
process described in :ref:`find_and_apply_patches`, leading to no patch being
created for it.

.. note::

   The same operation can also be used to create a patch for each member of a
   module but, since it is not possible to decorate a module, the function
   :func:`create_patches` needs to be directly used instead.


.. _overwrite_attributes:

Overwriting Attributes at the Destination
-----------------------------------------

If there was to be an attribute at the patch's destination already existing
with the patch's name, then the patching process can optionally override the
original attribute after storing a copy of it. This way, the original attribtue
remains accessible from within our code with the help of the
:func:`get_original_attribute` function:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> settings = gorilla.Settings(allow_hit=True)
   >>> @gorilla.patch(destination, settings=settings)
   ... def function():
   ...     print("Hello world!")
   ...     # We're overwriting an existing function here,
   ...     # preserve its original behaviour.
   ...     original = gorilla.get_original_attribute(destination, 'function')
   ...     return original()


.. note::

   The default settings of a patch do not allow attributes at the destination
   to be overwritten. For such a behaviour, the attribute
   :attr:`Settings.allow_hit` needs to be set to ``True``.


.. _stack_ordering:

Stack Ordering
--------------

The order in which the decorators are applied *does* matter. The
:func:`patch` decorator can only be aware of the decorators defined below it.

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patch(destination.Class)
   ... @staticmethod
   ... def my_static_method_1():
   ...     print("Hello")
   >>> @staticmethod
   ... @gorilla.patch(destination.Class)
   ... def my_static_method_2():
   ...     print("world!")


Here, only the static method ``my_static_method_1()`` will be injected as
expected with the decorator ``staticmethod`` while the other one will result
in an invalid definition since it will be interpreted as a standard method but
doesn't define any parameter referring to the class object such as ``self``.


.. _find_and_apply_patches:

Finding and Applying the Patches
--------------------------------

Once that the patches are created with the help of the decorators, the next
step is to (recursively) scan the modules and packages to retrieve them. This
is easily achieved with the :func:`find_patches` function.

Finally, each patch can be applied using the :func:`apply` function.

.. code-block:: python

   >>> import gorilla
   >>> import mypackage
   >>> patches = gorilla.find_patches([mypackage])
   >>> for patch in patches:
   ...     gorilla.apply(patch)


.. _dynamic_patching:

Dynamic Patching
----------------

In the case where patches need to be created dynamically, meaning that the
patch source objects and/or destinations are not known until runtime, then it
is possible to directly use the :class:`Patch` class.

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> def my_function():
   ...     print("Hello world!")
   >>> patch = gorilla.Patch(destination, 'better_function', my_function)
   >>> gorilla.apply(patch)


.. note::

   Special precaution is advised when directly setting the :attr:`Patch.obj`
   attribute. See the warning note in the class :class:`Patch` for more
   details.


.. |setattr()| replace:: ``setattr()``

.. _setattr(): https://docs.python.org/library/functions.html#setattr
