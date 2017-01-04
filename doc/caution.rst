.. currentmodule:: gorilla

.. _caution:

A Word of Caution
=================

The process of Monkey Patching is at the same time both incredibly powerful
*and* dangerous. It makes it easy to improve things on the surface but makes it
even easier to cause troubles if done inappropriately.

Mostly, inserting new attributes by prefixing their name to avoid (future?)
name clashes is *usually* fine, but **replacing existing attributes should be
avoided like the plague** unless you really have to and know what you are
doing. That is, if you do not want ending up being fired because you broke
everyone else's code.

As a safety measure, Gorilla has its :attr:`Settings.allow_hit` attribute set
to ``False`` by default, which raises an exception whenever it detects an
attempt at overwriting an existing attribute.

If you still want to go ahead with allowing hits, a second measure enabled
by default through the :attr:`Settings.store_hit` attribute is to store the
overwriten attribute under a different name to have it still accessible using
the function :func:`get_original_attribute`.

But still, avoid it if you can.

You've been warned.
