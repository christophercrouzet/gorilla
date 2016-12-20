import gorilla

from tests.utils import tomodule


@gorilla.patch(tomodule, name='function1')
def function():
    """subpackage.module1.function"""
    return "subpackage.module1.function"


@gorilla.patch(tomodule.Class)
def unbound_method(self):
    """subpackage.module1.unbound_method"""
    return "subpackage.module1.unbound_method"


@gorilla.patch(tomodule.Class)
@classmethod
def unbound_class_method(cls):
    """subpackage.module1.unbound_class_method"""
    return "subpackage.module1.unbound_class_method"


@gorilla.patch(tomodule.Class)
@staticmethod
def unbound_static_method():
    """subpackage.module1.unbound_static_method"""
    return "subpackage.module1.unbound_static_method"


class Class(object):

    """subpackage.module1.Class"""

    class Inner(object):

        """subpackage.module1.Class.Inner"""

        def method(self):
            """subpackage.module1.Class.Inner.method"""
            return "subpackage.module1.Class.Inner.method"


    @gorilla.patch(tomodule.Class, name='value1')
    @property
    def value(self):
        """subpackage.module1.Class.value.getter"""
        return "subpackage.module1.Class.value.getter"

    @gorilla.patch(tomodule.Class, name='method1')
    def method(self):
        """subpackage.module1.Class.method"""
        return "subpackage.module1.Class.method"

    @classmethod
    def class_method(cls):
        """subpackage.module1.Class.class_method"""
        return "subpackage.module1.Class.class_method"

    @staticmethod
    def static_method():
        """subpackage.module1.Class.static_method"""
        return "subpackage.module1.Class.static_method"
