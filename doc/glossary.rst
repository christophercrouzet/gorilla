.. _glossary:

Glossary
========

.. glossary::
   
   descriptor
      A Python object that has at least a ``__get__`` attribute defined.
      Those include classes, functions, methods, properties and decorators
      such as ``classmethod``, ``staticmethod`` and the ones defined in
      the :mod:`gorilla.decorators` module. See `Descriptor HowTo Guide`_.
   
   extension
      Either a class or a :term:`descriptor` object that is to be used to
      :term:`patch` a specified target.
   
   monkey patching
      Operation that takes an :term:`object` (either a class or a
      :term:`descriptor`) and inserts it into a target object (either a
      module or a class). This results in one or multiple new
      attributes being defined and callable from within the target object.
   
   object
      Gorilla recognizes 3 types of Python objects that are suitable either
      as :term:`extension`\ s or as patching targets: modules, classes and
      :term:`descriptor`\ s.
   
   patch
      See :term:`monkey patching`.


.. _Descriptor HowTo Guide: https://docs.python.org/howto/descriptor.html
