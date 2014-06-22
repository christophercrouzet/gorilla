"""
    gorilla._constants
    ~~~~~~~~~~~~~~~~~~~
    
    Constants for internal use.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

# Naming pattern to use for each constant name.
PATTERN = '_gorilla_%s'

# Naming pattern to use when backuping the attributes to be overriden
# during the patching process.
ORIGINAL = PATTERN % 'original_%s'

# Data stored by the decorators.
DECORATOR_DATA = PATTERN % 'decorator_data'
