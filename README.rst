Gorilla
=======

.. image:: https://img.shields.io/travis/christophercrouzet/gorilla/master.svg
   :target: https://travis-ci.org/christophercrouzet/gorilla
   :alt: Build status

.. image:: https://img.shields.io/coveralls/christophercrouzet/gorilla/master.svg
   :target: https://coveralls.io/r/christophercrouzet/gorilla
   :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/gorilla.svg
   :target: https://pypi.python.org/pypi/gorilla
   :alt: PyPI latest version

.. image:: https://readthedocs.org/projects/gorilla/badge/?version=latest
   :target: https://gorilla.readthedocs.io
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/l/gorilla.svg
   :target: https://pypi.python.org/pypi/gorilla
   :alt: License


Gorilla is a Python library that provides a convenient approach to monkey
patching.

Monkey patching is the process of **modifying module and class attributes at
runtime** with the purpose of replacing or extending third-party code.

Although *not* a recommended practice, it is sometimes useful to fix or modify
the behaviour of a piece of code from a third-party library, or to extend its
public interface while making the additions feel like they are built-in into
the library.

The Python language makes monkey patching extremely easy but the advantages of
Gorilla are multiple, not only in assuring a **consistent behaviour** on both
Python 2 and Python 3 versions, but also in preventing common source of errors,
and making the process both **intuitive and convenient** even when faced with
*large* numbers of patches to create.


Features
--------

* intuitive and convenient decorator approach to create patches.
* can create patches for all class or module members at once.
* compatible with both Python 2 and Python 3.
* customizable behaviour.


Usage
-----

Thanks to the dynamic nature of Python that makes monkey patching possible, the
process happens at runtime without ever having to directly modify the source
code of the third-party library:

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


The code above creates two patches, one for each member of the class
``MyClass``, but does not apply them yet. In other words, they define the
information required to carry on the operation but are not yet inserted into
the specified destination class ``destination.Class``.

Such patches created with the decorators can then be automatically retrieved by
recursively scanning a package or a module, then applied:

.. code-block:: python

   >>> import gorilla
   >>> import mypackage
   >>> patches = gorilla.find_patches([mypackage])
   >>> for patch in patches:
   ...     gorilla.apply(patch)


See the `Tutorial`_ section from the documentation for more detailed examples
and explanations on how to use Gorilla.


Documentation
-------------

Read the documentation online at `gorilla.readthedocs.io`_ or check its source
in the ``doc`` directory.


Out There
---------

Projects using Gorilla include:

* `bana <https://github.com/christophercrouzet/bana>`_
* `mlflow <https://github.com/mlflow/mlflow>`_


Author
------

Christopher Crouzet
<`christophercrouzet.com <https://christophercrouzet.com>`_>


.. _gorilla.readthedocs.io: https://gorilla.readthedocs.io
.. _Tutorial: https://gorilla.readthedocs.io/en/latest/tutorial.html
