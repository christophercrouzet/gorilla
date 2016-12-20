import gorilla

from tests.utils import tomodule


def function():
    """subpackage.module2.function"""
    return "subpackage.module2.function"


def unbound_method(self):
    """subpackage.module2.unbound_method"""
    return "subpackage.module2.unbound_method"


@classmethod
def unbound_class_method(cls):
    """subpackage.module2.unbound_class_method"""
    return "subpackage.module2.unbound_class_method"


@staticmethod
def unbound_static_method():
    """subpackage.module2.unbound_static_method"""
    return "subpackage.module2.unbound_static_method"


class Class(object):

    """subpackage.module2.Class"""

    class Inner(object):

        """subpackage.module2.Class.Inner"""

        def method(self):
            """subpackage.module2.Class.Inner.method"""
            return "subpackage.module2.Class.Inner.method"


    @property
    def value(self):
        """subpackage.module2.Class.value.getter"""
        return "subpackage.module2.Class.value.getter"

    def method(self):
        """subpackage.module2.Class.method"""
        return "subpackage.module2.Class.method"

    @gorilla.patch(tomodule.Class, name='class_method2')
    @classmethod
    def class_method(cls):
        """subpackage.module2.Class.class_method"""
        return "subpackage.module2.Class.class_method"

    @gorilla.patch(tomodule.Class, name='static_method2')
    @staticmethod
    def static_method():
        """subpackage.module2.Class.static_method"""
        return "subpackage.module2.Class.static_method"
