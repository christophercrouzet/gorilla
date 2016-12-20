Gorilla
=======

Gorilla is a library providing a convenient approach to monkey patching.

Monkey patching is the process of modifying modules and classes attributes at
runtime with the purpose of replacing of extending third-party code. See
`Wikipedia's Monkey patch page`_ for a more complete definition.


Features
--------

* creation of patches using decorators.
* creation of batches of patches using the members of either classes or
  modules.
* warns when patching an existing attribute and/or store the overriden
  attribute to make it accessible.
* customizable behaviour.
* allows the dynamic creation of patches at runtime.
* compatible with both Python 2 and Python 3.


Usage
-----

Marking a function ``my_function()`` as being a patch for a module
``destination`` is as easy as:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patch(destination)
   ... def my_function():
   ...     print("Hello world!")


Marking a class ``destination.Class`` to be patched with the members of another
class is no sweat either:

.. code-block:: python

   >>> import gorilla
   >>> import destination
   >>> @gorilla.patches(destination.Class)
   ... class MyClass(object):
   ...     def method(self):
   ...         print("Hello")
   ...     @classmethod
   ...     def class_method(cls):
   ...         print("world!")


See the ``overview`` and ``tutorial`` sections of the documentation for more
details.


Documentation
-------------

Read the documentation online at <http://gorilla.readthedocs.org> or check
their source from the ``doc`` folder.

The documentation can be built in different formats using Sphinx.


Running the Tests
-----------------

A suite of unit tests is available from the ``tests`` directory. You can run it
by firing:

.. code-block:: bash

   $ python tests/run.py


To run specific tests, it is possible to pass names to match in the command
line.

.. code-block:: bash

   $ python tests/run.py TestCase test_my_code


This command will run all the tests within the ``TestCase`` class as well as
the individual tests which contains ``test_my_code`` in their name.


Get the Source
--------------

The source code is available from the `GitHub project page`_.


Contributing
------------

Found a bug or got a feature request? Don't keep it for yourself, log a new
issue on `GitHub <https://github.com/christophercrouzet/gorilla/issues>`_.


Author
------

Christopher Crouzet
<`christophercrouzet.com <http://christophercrouzet.com>`_>


.. _Wikipedia's Monkey patch page: https://en.wikipedia.org/wiki/Monkey_patch
.. _GitHub project page: https://github.com/christophercrouzet/gorilla
