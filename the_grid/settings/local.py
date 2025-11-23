"""
Django settings for the_grid project - Local Development

These settings are used for local development.
Inherits from base.py and overrides with development-specific settings.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Database
# Using SQLite for local development

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Email backend for local development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Disable HTTPS redirects in local development
SECURE_SSL_REDIRECT = False


# Django Debug Toolbar (optional - uncomment if installed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1']
