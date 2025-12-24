"""
Settings package for environment-based configuration.
"""
from .base import *

# Import local settings for development
try:
    from .local import *
except ImportError:
    pass





