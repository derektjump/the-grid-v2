"""
Django settings for the_grid project - Production

These settings are used for production deployment on Azure App Service.
Inherits from base.py and overrides with production-specific settings.
"""

import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS - Azure App Service configuration
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]

# If no ALLOWED_HOSTS set, default to Azure wildcard
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*.azurewebsites.net']

# Azure App Service uses a reverse proxy that forwards requests
# Trust the X-Forwarded-Host header from Azure's load balancer
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECRET_KEY should come from environment variable
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)


# Database - Azure PostgreSQL configuration
# Fallback to SQLite if DB_HOST is not set (for initial deployment troubleshooting)
if os.getenv('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'the-grid-v2'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                # Use 'prefer' instead of 'require' to allow non-SSL connections for testing
                # Change back to 'require' once VNet integration is working
                'sslmode': os.getenv('DB_SSLMODE', 'prefer'),
            },
        }
    }
else:
    # Temporary fallback to SQLite for initial deployment
    # Remove this once database connectivity is confirmed
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',  # Azure temp storage
        }
    }


# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Static files configuration for Azure
# TODO: Configure Azure Blob Storage for static files if needed
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# AZURE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
# AZURE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
# AZURE_CONTAINER = 'static'


# Logging configuration
# TODO: Configure Azure Application Insights or Azure Monitor
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}


# Email configuration for production
# TODO: Configure email backend (Azure Communication Services or similar)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
