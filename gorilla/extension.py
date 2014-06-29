"""
    gorilla.extension
    ~~~~~~~~~~~~~~~~~
    
    Main logic behind the patching process.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla._constants
import gorilla._utils
import gorilla.settings
import gorilla.utils
from gorilla._objecttype import ObjectType


class Extension(object):
    
    """Core of the patching process.
    
    It knows which code to use for patching, where to apply it, and how to
    do it.
    
    Two types of patching operations are permitted:
        
        * module targets can be patched with either functions or classes.
        * class targets can be patcged with either classes or class
          routines (``function``, ``method``, ``classmethod``,
          ``staticmethod``, ``property``).
    
    When an attribute with the same name as the extension is found on the
    target, then the existing attribute is saved under another name and
    becomes callable from within the extension's code through the
    `~gorilla.utils.get_original_attribute` function. This ensures that
    the original behavior of an attribute can be preserved if needed.
    
    One exception is when a class is to be patched in a target that already
    contains a class with the same name. In this case, the operation will
    recursively patch each attribute member.
    
    It is possible to apply callable objects to transform the decorated
    object during the patching process. This can be use for example to
    ensure that a function is applied as a static method in a class.
    
    By default, the bahavior of the patching process is dictated by the
    settings defined in the `~gorilla.settings.Settings` class. It's
    possible to override those by using the `settings` property.
    
    Note
    ----
        This class shouldn't be used directly but in the case where dynamic
        patching is required.
    """
        
    def __init__(self, object, target):
        """Constructor.
        
        Parameters
        ----------
        object : object
            Extension object to use as a patch. Either a class or
            a descriptor.
        target : object
            Target to patch. Either a module or a class.
        
        Note
        ----
            Because of the descriptor protocol [1]_, it is possible that
            the object returned by accessing a method with the ``.``
            delimiter such as ``MyClass.my_method`` might be different than
            if accessed through ``MyClass.__dict__['my_method']``. This is
            because in the former case, any decorator applied to the method
            might return a different object while in the latter case the
            full stack of decorators is returned, as internally stored by
            the owning object before any runtime operation is being done.
            
            >>> class MyClass(object):
            ...     @classmethod
            ...     def my_method(cls):
            ...         return
            >>> print(MyClass.my_method)
            <bound method type.my_method of <class '__main__.MyClass'>>
            >>> print(MyClass.__dict__['my_method'])
            <classmethod object at 0x1007d5a98>
            
            As a result, if you need to make a direct use of the class
            `Extension`, make sure that you pass a reference of the object
            to use as a patch from the ``__dict__`` attribute if you need
            to transfer all the decorators applied to it.
            
            >>> from gorilla.extension import Extension
            >>> import guineapig
            >>> Extension(Needle.__dict__['needle'], guineapig).patch()
        
        References
        ----------
        .. [1] The `Descriptor Protocol
               <https://docs.python.org/howto/descriptor.html#descriptor-protocol>`_
        """
        self._object = object
        self._target = target
        self._name = ''
        self._apply = []
        self._settings = {}
        self._original = None
        self._done = False
    
    @property
    def object(self):
        """Extension object to use as a patch."""
        return self._object
    
    @property
    def target(self):
        """Target to patch."""
        return self._target
    
    @property
    def name(self):
        """Name for the resulting attribute."""
        if self._name:
            return self._name
        
        underlying = gorilla._utils.get_underlying_object(self._object)
        return underlying.__name__
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def apply(self):
        """Callable objects to apply during the patching process."""
        return self._apply
    
    @apply.setter
    def apply(self, value):
        self._apply = gorilla.utils.listify(value)
    
    @property
    def settings(self):
        """Settings to use during the patching operation.
        
        Those settings override the default settings defined in the class
        `~gorilla.settings.Settings` as well as any setting coming from the
        `~gorilla.extensionsregistrar.ExtensionsRegistrar.register_extensions`
        function.
        
        Either a `~gorilla.settings.Settings` or a `dict` are accepted as
        input but the value returned is always a `dict`.
        """
        return self._settings
    
    @settings.setter
    def settings(self, value):
        if gorilla._utils.is_settings(value):
            self._settings = value.as_dict()
        else:
            self._settings = value
    
    @property
    def original(self):
        """Attribute from the target to be overriden.
        
        Return None if no attributes are to be overriden.
        """
        if hasattr(self._target, '__dict__'):
            return self._target.__dict__.get(self.name, None)
        
        return getattr(self._target, self.name, None)
    
    @property
    def done(self):
        """True if the patch has already been applied."""
        return self._done
    
    def get_compiled_settings(self):
        """Compile a valid dictionary of settings.
        
        Any missing attribute from the settings property is completed
        with the defaults taken from `~gorilla.settings.Settings`.
        
        Returns
        -------
        dict
            The settings property completed with any missing attribute.
        """
        incomplete = any(attribute not in self._settings for attribute
                         in gorilla.settings.Settings._attributes)
        if not incomplete:
            return self._settings.copy()
        
        compiled_settings = gorilla.settings.Settings.as_dict()
        compiled_settings.update(self._settings)
        return compiled_settings
    
    def patch(self):
        """Patch the extension to the specified target.
        
        Raises
        ------
        TypeError
            The object and/or target types are not suitable for patching.
        
        RuntimeError
            Overwriting an existing attribute is not allowed when the settings
            `allow_overwriting` is set to True.
        """
        if self._done:
            return
        
        settings = self.get_compiled_settings()
        
        object = self._object
        for item in reversed(self._apply):
            object = item(object)
        
        extension_name = self.name
        original = self.original
        object_type = self._get_object_type(object)
        target_type = self._get_target_type(self._target)
        if (target_type not in (ObjectType.module, ObjectType.cls) or
                object_type not in (ObjectType.cls, ObjectType.descriptor)):
            raise TypeError("Cannot patch a `%s` with a `%s`." % (
                type(self._target).__name__, type(object).__name))
        
        if original:
            if not settings['allow_overwriting']:
                raise RuntimeError("An attribute named '%s' already exists on "
                                   "the target '%s'." % (
                                       original.__name__,
                                       self._target.__name__))
            
            original_type = ObjectType.get(original)
            if object_type == original_type == ObjectType.cls:
                if settings['update_class']:
                    # An existing class has to be patched with another class.
                    # Recursively go through each attribute member.
                    attributes = gorilla._utils.class_attribute_iterator(
                        object)
                    for name, attribute in attributes:
                        data = gorilla._utils.get_decorator_data(attribute)
                        name = data['name'] if 'name' in data else name
                        apply = data.get('apply', [])
                        extension = self.__class__(attribute, original)
                        extension.name = name
                        extension.apply = apply
                        extension.patch()
                    
                    return
            elif original_type != object_type:
                raise TypeError("Expected to patch a `%s` named `%s` "
                                "but found a `%s` instead." % (
                                    type(object).__name__,
                                    extension_name,
                                    type(original).__name__))
            
            # Rename the original attribute to keep a copy of it.
            original_name = gorilla._constants.ORIGINAL % extension_name
            if not hasattr(self._target, original_name):
                setattr(self._target, original_name, original)
        
        # Replace any empty docstring with the original one. Python 2 doesn't
        # allow to write the docstring of a class so we skip it.
        if (original and
                (not gorilla._python.PY2 or object_type != ObjectType.cls)):
            underlying = gorilla._utils.get_underlying_object(object)
            if not getattr(underlying, '__doc__', None):
                setattr(underlying, '__doc__',
                        gorilla._utils.get_underlying_object(original).__doc__)
        
        # Do the actual patching.
        setattr(self._target, extension_name, object)
        self._done = True
    
    @staticmethod
    def _get_object_type(object):
        object_type = ObjectType.get(object)
        if not object_type in (ObjectType.cls, ObjectType.descriptor):
            raise TypeError("Expected a `class`, a `function`, a `method` or "
                            "a `property` but got a `%s` instead." %
                            type(object).__name__)
        
        return object_type
    
    @staticmethod
    def _get_target_type(target):
        target_type = ObjectType.get(target)
        if target_type not in (ObjectType.module, ObjectType.cls):
            raise TypeError("Expected a `module` or a `class` but "
                            "got a `%s` instead." % type(target).__name__)
        
        return target_type
