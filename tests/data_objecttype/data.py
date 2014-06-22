import types


def bad_decorator_1(wrapped):
    def wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    
    return wrapper


class bad_decorator_2(object):
    
    def __init__(self, wrapped):
        self.wrapped = wrapped
    
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


def good_decorator(wrapped):
    return wrapped


def function_1():
    return


@bad_decorator_1
def function_2():
    return


@bad_decorator_2
def function_3():
    return


@good_decorator
def function_4():
    return


@classmethod
def class_method_1():
    return


@bad_decorator_1
@classmethod
def class_method_2():
    return


@bad_decorator_2
@classmethod
def class_method_3():
    return


@good_decorator
@classmethod
def class_method_4():
    return


@classmethod
@bad_decorator_1
def class_method_5():
    return


@classmethod
@bad_decorator_2
def class_method_6():
    return


@classmethod
@good_decorator
def class_method_7():
    return


@staticmethod
def static_method_1():
    return


@bad_decorator_1
@staticmethod
def static_method_2():
    return


@bad_decorator_2
@staticmethod
def static_method_3():
    return


@good_decorator
@staticmethod
def static_method_4():
    return


@staticmethod
@bad_decorator_1
def static_method_5():
    return


@staticmethod
@bad_decorator_2
def static_method_6():
    return


@staticmethod
@good_decorator
def static_method_7():
    return


@property
def property_1():
    return


@bad_decorator_1
@property
def property_2():
    return


@bad_decorator_2
@property
def property_3():
    return


@good_decorator
@property
def property_4():
    return


@property
@bad_decorator_1
def property_5():
    return


@property
@bad_decorator_2
def property_6():
    return


@property
@good_decorator
def property_7():
    return


class Class_1(object):
    
    def __init__(self):
        return
    
    def method(self):
        return
    
    @classmethod
    def class_method(cls):
        return
    
    @staticmethod
    def static_method():
        return
    
    @property
    def property(self):
        return


class Class_2(object):
    
    @bad_decorator_1
    def __init__(self):
        return
    
    @bad_decorator_1
    def method(self):
        return
    
    @bad_decorator_1
    @classmethod
    def class_method(cls):
        return
    
    @bad_decorator_1
    @staticmethod
    def static_method():
        return
    
    @bad_decorator_1
    @property
    def property(self):
        return


class Class_3(object):
    
    @bad_decorator_2
    def __init__(self):
        return
    
    @bad_decorator_2
    def method(self):
        return
    
    @bad_decorator_2
    @classmethod
    def class_method(cls):
        return
    
    @bad_decorator_2
    @staticmethod
    def static_method():
        return
    
    @bad_decorator_2
    @property
    def property(self):
        return


class Class_4(object):
    
    @good_decorator
    def __init__(self):
        return
    
    @good_decorator
    def method(self):
        return
    
    @good_decorator
    @classmethod
    def class_method(cls):
        return
    
    @good_decorator
    @staticmethod
    def static_method():
        return
    
    @good_decorator
    @property
    def property(self):
        return


@classmethod
class EmptyClass_1(object):
    pass


@staticmethod
class EmptyClass_2(object):
    pass


@property
class EmptyClass_3(object):
    pass


@bad_decorator_1
class EmptyClass_4(object):
    pass


@bad_decorator_2
class EmptyClass_5(object):
    pass


@good_decorator
class EmptyClass_6(object):
    pass
