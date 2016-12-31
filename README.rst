Gorilla
=======

.. image:: https://img.shields.io/pypi/v/gorilla.svg
   :target: https://pypi.python.org/pypi/gorilla
   :alt: PyPI latest version

.. image:: https://readthedocs.org/projects/gorilla/badge/?version=latest
   :target: https://gorilla.readthedocs.io
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/l/gorilla.svg
   :target: https://pypi.python.org/pypi/gorilla
   :alt: License


Gorilla is a library that provides a convenient approach to monkey patching.

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


See the ``tutorial`` section from the documentation for more examples.


Documentation
-------------

See the `Tutorial`_ section from the documentation for more information and
examples on using Gorilla.


Installation
------------

See the `Installation`_ section from the documentation.


Documentation
-------------

Read the documentation online at <https://gorilla.readthedocs.io> or check its
source in the ``doc`` directory.


Running the Tests
-----------------

Tests are available in the ``tests`` directory and can be fired through the
``run.py`` file:

.. code-block:: bash

   $ python tests/run.py


It is also possible to run specific tests by passinga space-separated list of
partial names to match:

.. code-block:: bash

   $ python tests/run.py TestClass


Finally, each test file is standalone and can be directly executed.


Author
------

Christopher Crouzet
<`christophercrouzet.com <https://christophercrouzet.com>`_>


.. _Wikipedia's Monkey patch page: https://en.wikipedia.org/wiki/Monkey_patch
.. _Tutorial: https://gorilla.readthedocs.io/en/latest/tutorial.html
.. _Installation: https://gorilla.readthedocs.io/en/latest/installation.html
