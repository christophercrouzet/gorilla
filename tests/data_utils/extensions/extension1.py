import gorilla.decorators

from .. import guineapig


@gorilla.decorators.patch(guineapig.GuineaPig, name="needle_method")
def method(self):
    return "needle into %s" % self.THIS


@gorilla.decorators.patch(guineapig.GuineaPig, name="needle_class_method", apply=classmethod)
def class_method(cls):
    return "needle into %s" % cls.THIS


@gorilla.decorators.patch(guineapig.GuineaPig, name="needle_static_method", apply=staticmethod)
def static_method():
    return "needle into %s" % GuineaPig.THIS


@gorilla.decorators.patch(guineapig.GuineaPig, name="needle_value", apply=property)
def value(self):
    return self._value
    