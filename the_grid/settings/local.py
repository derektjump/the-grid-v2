"""
Django settings for the_grid project - Local Development

These settings are used for local development.
Inherits from base.py and overrides with development-specific settings.
"""

import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CSRF trusted origins for local development
# Required for OIDC callback to work properly
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


# Database
# Use PostgreSQL for local development if environment variables are set,
# otherwise fall back to SQLite

if os.getenv('DB_HOST'):
    db_host_val = os.getenv('DB_HOST')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'the-grid-v2'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': db_host_val,
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {},  # No SSL required for local development
        }
    }

    # Data Connect database for sales data (read-only)
    # Contains sales_board_summary table refreshed every 15 minutes
    if os.getenv('DATA_CONNECT_DB_NAME'):
        DATABASES['data_connect'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATA_CONNECT_DB_NAME', 'data_connect'),
            'USER': os.getenv('DATA_CONNECT_DB_USER', os.getenv('DB_USER')),
            'PASSWORD': os.getenv('DATA_CONNECT_DB_PASSWORD', os.getenv('DB_PASSWORD')),
            'HOST': os.getenv('DATA_CONNECT_DB_HOST', db_host_val),
            'PORT': os.getenv('DATA_CONNECT_DB_PORT', '5432'),
            'OPTIONS': {},
        }
else:
    # Fallback to SQLite if no database environment variables are set
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


# ============================================================================
# AZURE AD / OIDC CONFIGURATION FOR LOCAL DEVELOPMENT
# ============================================================================

# In Azure AD App Registration, configure redirect URI as:
# http://localhost:8000/oidc/callback/
#
# Optionally also add:
# http://127.0.0.1:8000/oidc/callback/
#
# Set these environment variables locally (via .env file or system environment):
# - OIDC_RP_CLIENT_ID: Application (client) ID from Azure AD app registration
# - OIDC_RP_CLIENT_SECRET: Client secret value from Azure AD app registration
# - OIDC_TENANT_ID: Directory (tenant) ID from Azure AD (or use 'common' for multi-tenant)
#
# Example .env file:
# OIDC_RP_CLIENT_ID=12345678-1234-1234-1234-123456789012
# OIDC_RP_CLIENT_SECRET=your-secret-value-here
# OIDC_TENANT_ID=87654321-4321-4321-4321-210987654321


# Django Debug Toolbar (optional - uncomment if installed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1']
