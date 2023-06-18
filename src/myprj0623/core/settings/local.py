"""
Django local environment settings for myprj0623 project.

Protected info should be written in ".env" file. For more information, go to the comment in base.py > "SECRET_KEY."
"""
from .base import *

DEBUG = True

INSTALLED_APPS += [
    # DjangoDebugToolbar
    'debug_toolbar',
]

# ----- Used by DjangoDebugToolbar -----
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1']
# ----------
