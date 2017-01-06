.. _tests:

Running the Tests
=================

After making any code change in Gorilla, tests need to be evaluated to ensure
that the library still behaves as expected.

.. note::

   Some of the commands below are wrapped into ``make`` targets for
   convenience, see the file ``Makefile``.


unittest
--------

The tests are written using Python's built-in |unittest|_ module. They are
available in the ``tests`` directory and can be fired through the
``tests/run.py`` file:

.. code-block:: bash

   $ python tests/run.py


It is possible to run specific tests by passing a space-separated list of
partial names to match:

.. code-block:: bash

   $ python tests/run.py ThisTestClass and_that_function


The ``unittest``'s command line interface is also supported:

.. code-block:: bash

   $ python -m unittest discover -s tests -v


Finally, each test file is a **standalone** and can be directly executed.


tox
---

Test environments have been set-up with |tox|_ to allow testing Gorilla against
each supported version of Python:

.. code-block:: bash

   $ tox


coverage
--------

The package |coverage|_ is used to help localize code snippets that could
benefit from having some more testing:

.. code-block:: bash

   $ coverage run --source gorilla -m unittest discover -s tests
   $ coverage report
   $ coverage html


In no way should ``coverage`` be a race to the 100% mark since it is *not*
always meaningful to cover each single line of code. Furthermore, **having some
code fully covered isn't synonym to having quality tests**. This is our
responsability, as developers, to write each test properly regardless of the
coverage status.


.. |coverage| replace:: ``coverage``
.. |tox| replace:: ``tox``
.. |unittest| replace:: ``unittest``

.. _coverage: https://coverage.readthedocs.io
.. _tox: https://tox.readthedocs.io
.. _unittest: https://docs.python.org/library/unittest.html
