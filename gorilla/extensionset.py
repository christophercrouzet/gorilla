"""
    gorilla.extensionset
    ~~~~~~~~~~~~~~~~~~~~
    
    Container for extensions.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import gorilla.utils


class ExtensionSet(object):
    
    """Extension container.
    
    Placeholder for possible future features implementations.
    """
    
    def __init__(self):
        """Constructor."""
        self._extensions = []
    
    @property
    def extensions(self):
        """Extensions contained within this set."""
        return list(self._extensions)
    
    def add(self, extensions):
        """Add extension(s) into this set.
        
        Parameters
        ----------
        extensions : [list of] gorilla.extension.Extension
            Extension(s) to add into this set.
        """
        self._extensions.extend(gorilla.utils.listify(extensions))
    
    def patch(self):
        """Apply the patches.
        
        Raises
        ------
        TypeError
            The object and/or target types are not suitable for patching.
        """
        for extension in self._extensions:
            extension.patch()
