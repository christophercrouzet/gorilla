Gorilla
=======

Gorilla is a library that provides a convenient approach to monkey patching.

Defining a function ``needle()`` as being an extension for a module
``guineapig`` is as easy as:

    >>> import gorilla
    >>> import guineapig
    >>> @gorilla.patch(guineapig)
    ... def needle():
    ...     print("awesome")


Marking a class ``GuineaPig`` to be patched with a class of our own is no sweat
either:

    >>> import gorilla
    >>> import guineapig
    >>> @patch(guineapig, name='GuineaPig')
    ... class Needle(object):
    ...     def needle(self, arg):
    ...         print("Patching %s is awesome" % self.__class__.__name__")
    ...     
    ...     @classmethod
    ...     def classic_needle(cls):
    ...     print("Patching %s is awesome" % cls.__name__")


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


.. _GitHub project page: https://github.com/christophercrouzet/gorilla
