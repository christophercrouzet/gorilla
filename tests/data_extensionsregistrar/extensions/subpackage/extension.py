import gorilla.decorators

from ... import guineapig


class Class(object):
    
    @gorilla.decorators.patch(guineapig.GuineaPig, name="needle_method")
    def method(self):
        return "Everything is %s! This %s too." % (self._value, self.THIS)
