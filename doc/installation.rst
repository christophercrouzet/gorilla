.. _installation:

Installation
============

Gorilla doesn't have any requirement outside of the Python interpreter. Any of
the following Python versions is supported: 2.7, 3.3, 3.4, 3.5, and 3.6.


Installing pip
--------------

The recommended [1]_ approach for installing a Python package such as Gorilla
is to use |pip|_, a package manager for projects written in Python. If ``pip``
is not already installed on your system, you can do so by following these
steps:

    1. Download `get-pip.py`_.
    2. Run ``python get-pip.py`` in a shell.


.. note::

   The installation commands described in this page might require ``sudo``
   privileges to run successfully.


System-Wide Installation
------------------------

Installing globally the most recent version of Gorilla can be done with
``pip``:

.. code-block:: bash

   $ pip install gorilla


Or using |easy_install|_ (provided with |setuptools|_):

.. code-block:: bash

   $ easy_install gorilla


Virtualenv
----------

If you'd rather make Gorilla only available for your specific project, an
alternative approach is to use |virtualenv|_. First, make sure that it is
installed:

.. code-block:: bash

   $ pip install virtualenv


Then, an isolated environment needs to be created for your project before
installing Gorilla in there:

.. code-block:: bash

   $ mkdir myproject
   $ cd myproject
   $ virtualenv env
   New python executable in /path/to/myproject/env/bin/python
   Installing setuptools, pip, wheel...done.
   $ source env/bin/activate
   $ pip install gorilla


At this point, Gorilla is available for the project ``myproject`` as long as
the virtual environment is activated.

To exit the virtual environment, run:

.. code-block:: bash

   $ deactivate


.. note::

   Instead of having to activate the virtual environment, it is also possible
   to directly use the ``env/bin/python``, ``env/bin/pip``, and the other
   executables found in the folder ``env/bin``.


.. note::

   For Windows, some code samples might not work out of the box. Mainly,
   activating ``virtualenv`` is done by running the command
   ``env\Scripts\activate`` instead.


Development Version
-------------------

To stay cutting edge with the latest development progresses, it is possible to
directly retrieve the source from the repository with the help of `Git`_:

.. code-block:: bash

   $ git clone https://github.com/christophercrouzet/gorilla.git
   $ cd gorilla
   $ pip install --editable .[dev]


.. note::

   The ``[dev]`` part installs additional dependencies required to assist
   development on Gorilla.

----

.. [1] See the `Python Packaging User Guide`_

.. |easy_install| replace:: ``easy_install``
.. |get-pip.py| replace:: ``get-pip.py``
.. |pip| replace:: ``pip``
.. |setuptools| replace:: ``setuptools``
.. |virtualenv| replace:: ``virtualenv``

.. _easy_install: https://setuptools.readthedocs.io/en/latest/easy_install.html
.. _get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
.. _Git: https://git-scm.com
.. _pip: https://pip.pypa.io
.. _Python Packaging User Guide: https://packaging.python.org/current/
.. _setuptools: https://github.com/pypa/setuptools
.. _virtualenv: https://virtualenv.pypa.io
