from . import guineapig


def function():
    return "needle into %s" % guineapig.GuineaPig.THIS


def method(self):
    return "needle into %s" % self.THIS


def class_method(cls):
    return "needle into %s" % cls.THIS


def static_method():
    return "needle into %s" % GuineaPig.THIS


def value(self):
    return self._value


class GuineaPig(object):
    
    # This shouldn't have any effect: variables are not overridable.
    THIS = "new %s" % guineapig.GuineaPig.THIS
    
    class InnerClass(object):
        def __init__(self):
            self._value = "more inner"
        
        def method(self):
            return "always %s" % self._value
    
    def __init__(self, *args, **kwargs):
        self._value = "more awesome"
    
    def method(self):
        return "Everything is %s! This %s too." % (self._value, GuineaPig.THIS)
    
    @classmethod
    def class_method(cls):
        return cls.static_method().replace("Static %s" % GuineaPig.THIS, "Classic %s" % cls.THIS)
    
    @staticmethod
    def static_method():
        return "Static %s but even more awesome nonetheless!" % GuineaPig.THIS
    
    @property
    def value(self):
        return "even %s" % self._value


class Ancestor(object):
    
    class Child(object):
        
        class GrandChild(object):
            
            def __init__(self):
                self.value = "needle's grand child"
    
        def __init__(self):
            self.value = "needle's child"
    
    def __init__(self):
        self.value = "needle"
