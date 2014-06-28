"""
    gorilla.settings
    ~~~~~~~~~~~~~~~~
    
    Default settings.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""


class Settings(object):
    
    """Default settings defining the extensions behavior."""
    
    _attributes = ('allow_overwriting', 'update_class')
    
    #: If False, do not allow to overwrite an existing attribute by
    #: raising an Exception. Otherwise the original attribute is to be
    #: saved under another name and becomes callable from within the
    #: extension's code.
    allow_overwriting = True
    
    #: If True and that a class extension is about to overwrite an
    #: existing class, then the process is done by updating the content
    #: of the original class with the class extension. Otherwise, the
    #: original class is entirely overwritten.
    update_class = True
    
    @classmethod
    def as_dict(cls):
        """Convert those settings into a dictionary.
        
        Returns
        -------
        dict
            The dictionary of those settings.
        """
        settings = {}
        for attribute in cls._attributes:
            settings[attribute] = getattr(cls, attribute)
        
        return settings
