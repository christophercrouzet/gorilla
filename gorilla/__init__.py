#                     __ __ __       
#   .-----.-----.----|__|  |  .---.-.
#   |  _  |  _  |   _|  |  |  |  _  |
#   |___  |_____|__| |__|__|__|___._|
#   |_____|                          
#                                    

"""
    gorilla
    ~~~~~~~
    
    Convenient approach to monkey patching.
    
    :copyright: Copyright 2014 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

from gorilla.decorators import apply, name, patch
from gorilla.utils import get_original_attribute


__version__ = '0.1.0'

__all__ = [
    'decorators',
    'extension',
    'extensionset',
    'extensionsregistrar',
    'settings',
    'utils'
]
