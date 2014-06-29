.. _faq:

FAQ
===

What's the motivation behind this library? In what is it different from a more conventional approach?
-----------------------------------------------------------------------------------------------------

   >>> import guineapig
   >>> def needle():
   ...     print("awesome")
   >>> guineapig.needle = needle


The library don't do much more than this exact use case. There isn't hundred
of ways of doing monkey patching after all.

Now, what if we had to patch a class method into an hypothetical
:class:`guineapig.GuineaPig` class?

   >>> import guineapig
   >>> class Needle(object):
   ...     @classmethod
   ...     def classic_needle(cls):
   ...         print("Patching %s is awesome" % cls.__name__)
   ...     print(classic_needle)
   ... print(Needle.classic_needle)
   <classmethod object at 0x10dd5c830>
   <bound method type.classic_needle of <class '__main__.Needle'>>


Note how both print statements don't print the same thing. The one nested
within the class outputs the ``classmethod`` object while the other returns an
object resulting from the Python's descriptor protocol.

So if the goal here is to preserve the class method decorator, then we need
to make sure that we write out the assignment 
``guineapig.GuineaPig.classic_needle = classic_needle`` within the class or
else we'd get an unexpected result. This is error-prone.

By using a decorator instead, it all becomes more intuitive and easy to debug.
If the decorator is written on top of ``@classmethod``, then the class method
gets patched. If it is written it below it, then only the underlying function
gets patched.

Furthermore, if we now have to patch 50 methods inside our target class 
:class:`guineapig.GuineaPig`, then instead of manually writing a monkey
patching assignment for each, we could instead regroup those 50 methods within
a single class and mark that entire class as being an extension.

   >>> import gorilla
   >>> import guineapig
   >>> @gorilla.patch(guineapig, name='GuineaPig')
   ... class Needle(object):
   ...     def needle_1(self):
   ...         print("First method")
   ...     def needle_2(self):
   ...         print("Second method")
   ...     def needle_3(self):
   ...         print("Third method")
   ...     # and so on...


Each method defined within the class :class:`Needle` gets individually
inserted in the :class:`guineapig.GuineaPig` class. If instead we would have
used an assignment such as ``guineapig.GuineaPig = Needle``, then we would have
had completely overriden the content of the original
:class:`guineapig.GuineaPig` class. Note that this behavior is still possible
by overidding the default settings from the class
:class:`~gorilla.settings.Settings`.

Another feature is that if a name clash is detected, then the original
attribute is saved under another name to remain accessible from within our
code.

   >>> import gorilla
   >>> from guineapig import GuineaPig
   >>> @gorilla.patch(GuineaPig)
   ... def needle(self, arg):
   ...     print(Patched "%s is awesome" % self.__class__.__name__)
   ...     # We're overriding an existing method here,
   ...     # preserve its original behavior.
   ...     return gorilla.get_original_attribute(self, 'needle')(arg)


In short there's nothing happening in this library that couldn't be done
differently. The goal here is to make the process convenient and robust,
without the user having to worry about eventual corner cases, while ensuring
that the code will remain portable across different versions of Python.
