.. _reference:

Reference
=========

The module :mod:`gorilla.decorators` contains everything to mark some code
as being :term:`extension`\ s to use to :term:`patch` a specified target.

If using the decorators approach, the extensions can be automatically
registered and applied using the
:class:`~gorilla.extensionsregistrar.ExtensionsRegistrar` class.

Applying patches dynamically can be done by directly using the core class
:class:`~gorilla.extension.Extension`.

Any function utilies that may help with writing extensions are available in the
:mod:`gorilla.utils` module.


.. toctree::
   :maxdepth: 2
   
   decorators
   extensions
   settings
   utils
