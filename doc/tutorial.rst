.. _tutorial:

Tutorial
========

The standard approach for :term:`patch`\ ing some external code is to be done
in 2 steps:
   
   * marking the :ref:`descriptor extensions <marking_descriptor_extensions>`
     and/or the :ref:`class extensions <marking_class_extensions>` with the
     :func:`~gorilla.decorators.patch` decorator.
   * :ref:`registering and applying the patches
     <registering_and_applying_the_patches>` through the
     :class:`~gorilla.extensionsregistrar.ExtensionsRegistrar` class.

The other option is to directly use the :class:`~gorilla.extension.Extension`
class if :ref:`dynamic patching <patching_dynamically>` is required.


.. _marking_descriptor_extensions:

Marking Descriptor Extensions
-----------------------------

Using a function :func:`needle` that we've created to patch a 3rd party
module goes as follows:

   >>> import gorilla
   >>> import guineapig
   >>> @gorilla.patch(guineapig)
   ... def needle():
   ...     print("awesome")

After applying the patch, this will have for effect to make the function
:func:`needle` available from within the module :mod:`guineapig`. Indeed,
a call to ``guineapig.needle()`` will print ``awesome``.

Changing the name of the function at runtime can be done via the parameter
`name`.

   >>> import gorilla
   >>> import guineapig
   >>> @gorilla.patch(guineapig, name='bigger_needle')
   ... def needle():
   ...     print("awesome")

The function :func:`needle` will now be accessible through a call to
``guineapig.bigger_needle()``.

Patching it into an existing class is only a matter of getting
the patch decorator to refer to the appropriate target.

   >>> import gorilla
   >>> from guineapig import GuineaPig
   >>> @gorilla.patch(GuineaPig)
   ... def needle(self):
   ...     print("Patching %s is awesome" % self.__class__.__name__)

By default, functions are inserted into classes as methods. The first attribute
of a such method (usually named `self` by convention) will refer to
the instance of the target class.

Adding such functions as class methods instead requires to add the
:func:`classmethod` descriptor into the list of callable objects to apply.

   >>> import gorilla
   >>> from guineapig import GuineaPig
   >>> @gorilla.patch(GuineaPig, apply=classmethod)
   ... def needle(cls):
   ...     print("Patching %s is awesome" % cls.__name__)

If there was to be a method named `needle` already existing in the
target class, then the patching process would override the original attribute
only after making a copy of it. This way, it remains accessible from within
our code with the help of the :func:`~gorilla.utils.get_original_attribute`
function.

   >>> import gorilla
   >>> from guineapig import GuineaPig
   >>> @gorilla.patch(GuineaPig)
   ... def needle(self, arg):
   ...     print(Patched "%s is awesome" % self.__class__.__name__)
   ...     # We're overriding an existing method here,
   ...     # preserve its original behavior.
   ...     return gorilla.get_original_attribute(self, 'needle')(arg)

.. note::
    
   The mechanism of saving an attribute to be overriden under another name
   also works if the target is a module.

Now this would quickly become cumbersome if it wasn't possible to
patch a class as a whole.


.. _marking_class_extensions:

Marking Class Extensions
------------------------

   >>> import gorilla
   >>> import guineapig
   >>> @patch(guineapig)
   ... class Needle(object):
   ...     def needle(self, arg):
   ...         print("Patching %s is awesome" % self.__class__.__name__)
   ...     
   ...     @classmethod
   ...     def classic_needle(cls):
   ...     print("Patching %s is awesome" % cls.__name__)
   ...     
   ...     @staticmethod
   ...     def static_needle():
   ...         print("awesome")

If no attribute named `Needle` were to be found in the target
module, then the class would simply be inserted as is. Otherwise,
each member from the class :class:`Needle` gets individually patched
into the target class found.

The members of :class:`Needle` are transferred over while preserving
their names as well as any decorators applied to them. This
behavior can be overrided by applying the decorators
:func:`~gorilla.decorators.name` and :func:`~gorilla.decorators.apply` on
each member.

   >>> import gorilla
   >>> import guineapig
   >>> @patch(guineapig, name='GuineaPig')
   ... class Needle(object):
   ...     @gorilla.name('bigger_needle')
   ...     def needle(self, arg):
   ...         print("Patching %s is awesome" % self.__class__.__name__)
   ...     
   ...     @gorilla.apply(classmethod)
   ...     def classic_needle(cls):
   ...     print("Patching %s is awesome" % cls.__name__)

The :meth:`needle` method can now be fired through a call to
``GuineaPig().bigger_needle()`` while the method ``classic_needle``
will be made a class method.


.. _stack_ordering:

Stack Ordering
--------------
    
The order in which the decorators are applied *does* matter. The
:func:`~gorilla.decorators.patch` decorator can only be aware of
the decorators defined below it.

   >>> import gorilla
   >>> from guineapig import GuineaPig
   ... class Needle(object):
   ...     @patch(GuineaPig)
   ...     @staticmethod
   ...     def needle_1():
   ...         print("awesome")
   ...     
   ...     @staticmethod
   ...     @patch(GuineaPig)
   ...     def needle_2():
   ...         print("awesome")

Here, the class :class:`GuineaPig` will be patched with the static method
:func:`Needle.needle_1` and a normal method :meth:`Needle.needle_2`. The
patching of the latter method will result in an invalid method definition
since it is missing the mandatory first argument referring to the class
instance.

Following the same logic, the :func:`~gorilla.decorators.name` and the
:func:`~gorilla.decorators.apply` decorators can override the values of a
:func:`~gorilla.decorators.patch` decorator only if they're applied on top of
it.

   >>> import gorilla
   >>> import guineapig
   >>> @gorilla.name('bigger_needle')
   ... @gorilla.patch(guineapig)
   ... def needle():
   ...     print("awesome")


.. _registering_and_applying_the_patches:

Registering and Applying the Patches
------------------------------------

Once that the extensions are marked, the next step is to apply them before
we can actually use them. This is easily achieved with the help of the
:meth:`~gorilla.extensionsregistrar.ExtensionsRegistrar.register_extensions`
class method.

   >>> from gorilla.extensionsregistrar import ExtensionsRegistrar
   >>> import extensionspackage
   >>> ExtensionsRegistrar.register_extensions(extensionspackage, patch=True)

For a given package ``extensionspackage``, the class method
:func:`~gorilla.extensionsregistrar.ExtensionsRegistrar.register_extensions`
scans recursively all the nested packages and modules and returns a
:class:`~gorilla.extensionset.ExtensionSet`

See the :ref:`bananas` section to see some examples of real-world
implementations.


.. _patching_dynamically:

Patching Dynamically
--------------------

In the case where patches need to be applied dynamically, meaning that the
extension objects and/or targets are only to be known at runtime, then it is
possible to make use of the :class:`~gorilla.extension.Extension` class.

   >>> from gorilla.extension import Extension
   >>> import guineapig
   ... def needle():
   ...     print("awesome")
   >>> Extension(needle, guineapig).patch()

.. note::
    
   Special precaution is advised when directly dealing with the
   :class:`~gorilla.extension.Extension` class. See the class
   :class:`~gorilla.extension.Extension` for more details.
