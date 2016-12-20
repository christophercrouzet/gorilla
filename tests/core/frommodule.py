import gorilla

from tests.core import tomodule


__all__ = ['global_variable', 'function', 'unbound_method',
           'unbound_class_method', 'unbound_static_method', 'Class', 'Parent',
           'Child']


#: frommodule.global_variable
global_variable = "frommodule.global_variable"


def function():
    """frommodule.function"""
    return "frommodule.function (%s)" % (Class.STATIC_VALUE,)


def unbound_method(self):
    """frommodule.unbound_method"""
    return "frommodule.unbound_method (%s, %s)" % (
        self.STATIC_VALUE, self.instance_value)


@classmethod
def unbound_class_method(cls):
    """frommodule.unbound_class_method"""
    return "frommodule.unbound_class_method (%s)" % (cls.STATIC_VALUE,)


@staticmethod
def unbound_static_method():
    """frommodule.unbound_static_method"""
    return "frommodule.unbound_static_method (%s)" % (Class.STATIC_VALUE,)


class Class(object):

    """frommodule.Class"""

    __all__ = ['STATIC_VALUE', 'Inner', '__init__', 'value', 'method',
               'class_method', 'static_method']

    STATIC_VALUE = "frommodule.Class.STATIC_VALUE"

    class Inner(object):

        """frommodule.Class.Inner"""

        __all__ = ['STATIC_VALUE', '__init__', 'method']

        STATIC_VALUE = "frommodule.Class.Inner.STATIC_VALUE"

        def __init__(self):
            """frommodule.Class.Inner.__init__"""
            self.instance_value = "frommodule.Class.Inner.instance_value"

        def method(self):
            """frommodule.Class.Inner.method"""
            return "frommodule.Class.Inner.method (%s)" % (
                self.instance_value,)


    def __init__(self):
        """frommodule.Class.__init__"""
        gorilla.get_original_attribute(self, '__init__')()
        self.stored_init_instance_value = self.instance_value
        self.instance_value = "frommodule.Class.instance_value"

    @property
    def value(self):
        """frommodule.Class.value.getter"""
        return "frommodule.Class.value.getter (%s)" % (self.instance_value,)

    @value.setter
    def value(self, value):
        """frommodule.Class.value.setter"""
        self.instance_value = value

    def method(self):
        """frommodule.Class.method"""
        return "frommodule.Class.method (%s, %s)" % (self.STATIC_VALUE,
                                                     self.instance_value)

    @classmethod
    def class_method(cls):
        """frommodule.Class.class_method"""
        return "frommodule.Class.class_method (%s)" % (cls.STATIC_VALUE,)

    @staticmethod
    def static_method():
        """frommodule.Class.static_method"""
        return "frommodule.Class.static_method (%s)" % (Class.STATIC_VALUE,)


class Parent(object):

    """frommodule.Parent"""

    __all__ = ['STATIC_VALUE', '__init__', 'method']
    __slots__ = tomodule.Parent.__slots__ + ('from_value',)

    STATIC_VALUE = "frommodule.Parent.STATIC_VALUE"

    def __init__(self):
        """frommodule.Parent.__init__"""
        self.instance_value = "frommodule.Parent.instance_value"
        self.parent_value = "frommodule.Parent.parent_value"
        self.to_value = "frommodule.Parent.to_value"
        self.from_value = "frommodule.Parent.from_value"

    def method(self):
        """frommodule.Parent.method"""
        return "frommodule.Parent.method (%s)" % (self.instance_value,)


class Child(Parent):

    """frommodule.Child"""

    __all__ = ['__init__', 'method']
    __slots__ = ('child_value',)

    def __init__(self):
        """frommodule.Child.__init__"""
        super(type(self), self).__init__()
        self.child_value = "frommodule.Child.child_value"
