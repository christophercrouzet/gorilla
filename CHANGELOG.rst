Changelog
=========

Version numbers comply with the `Sementic Versioning Specification (SemVer)`_.


`Unreleased`_
-------------


`v0.4.0`_ (2021-04-17)
----------------------

Added
^^^^^

* Implement a new public function to revert a patch.
* Support applying stacks of patches.
* Include the utf-8 shebang to all source files.
* Enforce Python 3 compatibility with the ``__future__`` module.
* Testing with Python versions 3.7, 3,8, and 3.9.
* Set the ``__all__`` attribute.
* Make use of styling and linting tools.


Removed
^^^^^^^

* Testing with Python version 3.3.
* Testing of the representation outputs.


Changed
^^^^^^^

* Update the setup file.
* Rework the project's metadata.
* Shorten docstrings for non-public functions.
* Make minor tweaks to the code.
* Use the ‘new’ string formatting method.
* Update the contact's email.


Fixed
^^^^^

* Fix ``__weakref__`` showing up in the doc.
* Fix the changelog reference.


`v0.3.0`_ (2017-01-18)
----------------------

Added
^^^^^

* Add the decorator data to the public interface.
* Add support for coverage and tox.
* Add continuous integration with Travis and coveralls.
* Add a few bling-bling badges to the readme.
* Add a Makefile to regroup common actions for developers.


Changed
^^^^^^^

* Improve the documentation.
* Improve the unit testing workflow.
* Remove the ``__slots__`` attribute from the ``Settings`` and ``Patch``
  classes.
* Refocus the content of the readme.
* Define the 'long_description' and 'extras_require' metadata to setuptools'
  setup.
* Update the documentation's Makefile with a simpler template.
* Rework the '.gitignore' files.
* Rename the changelog to 'CHANGELOG'!
* Make minor tweaks to the code.


Fixed
^^^^^

* Fix the settings not being properly inherited.
* Fix the decorator data not supporting class inheritance.


`v0.2.0`_ (2016-12-20)
----------------------

Changed
^^^^^^^

* Rewrite everything from scratch. Changes are not backwards compatible.


`v0.1.0`_ (2014-06-29)
----------------------

Added
^^^^^

* Add settings to modify the behaviour of the patching process.
* Added a FAQ section to the doc.


Changed
^^^^^^^

* Refactor the class ``ExtensionSet`` towards using an ``add()`` method.
* Clean-up the ``Extension.__init__()`` method from the parameters not required
  to construct the class.
* Get the ``ExtensionsRegistrar.register_extensions()`` function to return a
  single ``ExtensionSet`` object.
* Make minor tweaks to the code and documentation.


v0.0.1 (2014-06-21)
-------------------

* Initial release.


.. _Sementic Versioning Specification (SemVer): http://semver.org
.. _Unreleased: https://github.com/christophercrouzet/gorilla/compare/v0.3.0...HEAD
.. _v0.4.0: https://github.com/christophercrouzet/gorilla/compare/v0.3.0...v0.4.0
.. _v0.3.0: https://github.com/christophercrouzet/gorilla/compare/v0.2.0...v0.3.0
.. _v0.2.0: https://github.com/christophercrouzet/gorilla/compare/v0.1.0...v0.2.0
.. _v0.1.0: https://github.com/christophercrouzet/gorilla/compare/v0.0.1...v0.1.0
