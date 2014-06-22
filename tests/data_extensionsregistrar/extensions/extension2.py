import gorilla.decorators

from .. import guineapig


@gorilla.decorators.patch(guineapig, name="Needle")
class Class(object):
    
    # This shouldn't have any effect: variables are not overridable.
    THIS = "new %s" % guineapig.GuineaPig.THIS
    
    def __init__(self, *args, **kwargs):
        self._value = "more awesome"
    
    def method(self):
        return "Everything is %s! This %s too." % (self._value, self.THIS)
    
    @classmethod
    def class_method(cls):
        return cls.static_method().replace("Static %s" % GuineaPig.THIS, "Classic %s" % cls.THIS)
    
    @staticmethod
    def static_method():
        return "Static %s but even more awesome nonetheless!" % GuineaPig.THIS
    
    @property
    def value(self):
        return "even %s" % self._value
