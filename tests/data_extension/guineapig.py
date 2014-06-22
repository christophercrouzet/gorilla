def function():
    """guineapig function."""
    return GuineaPig.THIS


def method(self):
    """guineapig method."""
    return "Everything is %s! This %s too." % (self.value, self.THIS)


@classmethod
def class_method(cls):
    """guineapig class method."""
    return cls.static_method().replace("Static %s" % cls.THIS, "Classic %s" % GuineaPig.THIS)


@staticmethod
def static_method():
    """guineapig static method."""
    return "Static %s but awesome nonetheless!" % GuineaPig.THIS


@property
def value(self):
    """guineapig property."""
    return self._value


class GuineaPig(object):
    
    """GuineaPig class."""
    
    THIS = "guinea pig"
    
    class InnerClass(object):
        
        """InnerClass class."""
        
        def __init__(self):
            self._value = "inner"
            self._initialized = True
        
        def method(self):
            return self._value
    
    def __init__(self):
        """GuineaPig init."""
        self._value = "awesome"
        self._initialized = True
    
    def method(self):
        """GuineaPig method."""
        return "Everything is %s! This %s too." % (self.value, self.THIS)
    
    @classmethod
    def class_method(cls):
        """GuineaPig class method."""
        return cls.static_method().replace("Static %s" % cls.THIS, "Classic %s" % GuineaPig.THIS)
    
    @staticmethod
    def static_method():
        """GuineaPig static method."""
        return "Static %s but awesome nonetheless!" % GuineaPig.THIS
    
    @property
    def value(self):
        """GuineaPig property."""
        return self._value


class Ancestor(object):
    
    class Child(object):
        
        class GrandChild(object):
            
            def __init__(self):
                self.value = "guinea pig's grand child"
    
        def __init__(self):
            self.value = "guinea pig's child"
    
    def __init__(self):
        self.value = "guinea pig"


class Empty(object):
    pass
