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
    
    def __init__(self, extensions=None):
        """Constructor.
        
        Parameters
        ----------
        extensions : list of gorilla.extension.Extension, optional
            Extensions to add into the set.
        """
        self._extensions = gorilla.utils.listify(extensions)
    
    @property
    def extensions(self):
        """Extensions contained within the set."""
        return self._extensions
    
    def patch(self):
        """Apply the patches.
        
        Raises
        ------
        TypeError
            The object and/or target types are not suitable for patching.
        """
        for extension in self._extensions:
            extension.patch()
