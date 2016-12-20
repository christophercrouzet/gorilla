__all__ = ['global_variable', 'function', 'Class', 'Parent', 'Child']


#: tomodule.global_variable
global_variable = "tomodule.global_variable"


def function():
    """tomodule.function"""
    return "tomodule.function (%s)" % (Class.STATIC_VALUE,)


class Class(object):

    """tomodule.Class"""

    __all__ = ['STATIC_VALUE', 'Inner', '__init__', 'value', 'method',
               'class_method', 'static_method']

    STATIC_VALUE = "tomodule.Class.STATIC_VALUE"

    class Inner(object):

        """tomodule.Class.Inner"""

        __all__ = ['STATIC_VALUE', '__init__', 'method']

        STATIC_VALUE = "tomodule.Class.Inner.STATIC_VALUE"

        def __init__(self):
            """tomodule.Class.Inner.__init__"""
            self.instance_value = "tomodule.Class.Inner.instance_value"

        def method(self):
            """tomodule.Class.Inner.method"""
            return "tomodule.Class.Inner.method (%s)" % (
                self.instance_value,)


    def __init__(self):
        """tomodule.Class.__init__"""
        self.instance_value = "tomodule.Class.instance_value"

    @property
    def value(self):
        """tomodule.Class.value.getter"""
        return "tomodule.Class.value.getter (%s)" % (self.instance_value,)

    @value.setter
    def value(self, value):
        """tomodule.Class.value.setter"""
        self.instance_value = value

    def method(self):
        """tomodule.Class.method"""
        return "tomodule.Class.method (%s, %s)" % (self.STATIC_VALUE,
                                                   self.instance_value)

    @classmethod
    def class_method(cls):
        """tomodule.Class.class_method"""
        return "tomodule.Class.class_method (%s)" % (cls.STATIC_VALUE,)

    @staticmethod
    def static_method():
        """tomodule.Class.static_method"""
        return "tomodule.Class.static_method (%s)" % (Class.STATIC_VALUE,)


class Parent(object):

    """tomodule.Parent"""

    __all__ = ['STATIC_VALUE', '__init__', 'method']
    __slots__ = ('instance_value', 'parent_value', 'to_value',)

    STATIC_VALUE = "tomodule.Parent.STATIC_VALUE"

    def __init__(self):
        """tomodule.Parent.__init__"""
        self.instance_value = "tomodule.Parent.instance_value"
        self.parent_value = "tomodule.Parent.parent_value"

    def method(self):
        """tomodule.Parent.method"""
        return "tomodule.Parent.method (%s)" % (self.instance_value,)


class Child(Parent):

    """tomodule.Child"""

    __all__ = ['__init__', 'method']
    __slots__ = ('child_value',)

    def __init__(self):
        """tomodule.Child.__init__"""
        super(type(self), self).__init__()
        self.child_value = "tomodule.Child.child_value"
