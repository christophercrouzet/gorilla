import gorilla._constants
import gorilla._utils
import gorilla.decorators

from . import guineapig


def decorator(value):
    def decorator(wrapped):
        data = gorilla._utils.get_decorator_data(wrapped)
        data['default'] = value
        return wrapped
    
    return decorator


def decorator_1(value):
    def decorator(wrapped):
        data = gorilla._utils.get_decorator_data(wrapped)
        data['first'] = value
        return wrapped
    
    return decorator


def decorator_2(value):
    def decorator(wrapped):
        data = gorilla._utils.get_decorator_data(wrapped)
        data['second'] = value
        return wrapped
    
    return decorator


def function():
    """Function docstring."""
    return


class Class(object):
    
    """Class docstring."""
    
    CONSTANT = True
    
    def __init__(self):
        self.value = True
    
    def __str__(self):
        return
    
    def __eq__(self, other):
        return
    
    def method(self):
        """Method docstring."""
        return
    
    @classmethod
    def class_method(cls):
        """Class method docstring."""
        return
    
    @staticmethod
    def static_method():
        """Static method docstring."""
        return
    
    @property
    def property(self, value):
        """Property docstring."""
        return


class DerivedClass(Class):
    
    """DerivedClass docstring."""
    
    def method(self):
        """Derived method docstring."""
        return
    
    def derived(self):
        """Derived method docstring."""
        return


class EmptyClass(object):
    
    """EmptyClass docstring."""
    pass


@gorilla.decorators.patch(guineapig)
def decorated_function(self):
    return


@gorilla.decorators.patch(guineapig)
class DecoratedClass(object):
    
    def undecorated_method(self):
        return
    
    @gorilla.decorators.patch(guineapig.GuineaPig)
    def decorated_method(self):
        return


class UndecoratedClass(object):
    
    class UndecoratedInnerClass(object):
        
        def undecorated_method(self):
            return
        
        @gorilla.decorators.patch(guineapig.GuineaPig.InnerClass)
        def decorated_method(self):
            return
    
    @gorilla.decorators.patch(guineapig.GuineaPig)
    class DecoratedInnerClass(object):
        
        def undecorated_method(self):
            return
        
        @gorilla.decorators.patch(guineapig.GuineaPig.InnerClass)
        def decorated_method(self):
            return
    
    def undecorated_method(self):
        return
    
    @gorilla.decorators.patch(guineapig.GuineaPig)
    def decorated_method(self):
        return
    