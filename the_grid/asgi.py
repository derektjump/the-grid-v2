"""
ASGI config for the_grid project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Use production settings by default for ASGI
# Override with DJANGO_SETTINGS_MODULE environment variable if needed
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_grid.settings.production')

application = get_asgi_application()
