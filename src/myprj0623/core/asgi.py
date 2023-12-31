"""
ASGI config for myprj0623 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Modified base directory (created settings directory from settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')

application = get_asgi_application()
