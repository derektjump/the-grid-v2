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

# Note: Azure health checks from internal IPs (169.254.0.0/16) are handled by
# HealthCheckMiddleware in core.middleware, which intercepts /robots933456.txt
# requests before they reach ALLOWED_HOSTS validation

# CSRF trusted origins for production
# Required for OIDC callback to work properly with Azure AD
csrf_origins_str = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins_str:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_str.split(',') if origin.strip()]
else:
    # Default to the primary Azure App Service domain
    CSRF_TRUSTED_ORIGINS = ['https://the-grid-v2.azurewebsites.net']

# Trust proxy headers for HTTPS detection
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECRET_KEY should come from environment variable
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)


# Middleware configuration for production
# Insert production-specific middleware at the beginning
MIDDLEWARE = [
    'core.middleware.HealthCheckMiddleware',  # Handle Azure health checks first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving
] + [m for m in MIDDLEWARE if m not in [
    'django.middleware.security.SecurityMiddleware',
]]

# Use WhiteNoise's compressed static file storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


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


# ============================================================================
# AZURE AD / OIDC CONFIGURATION FOR PRODUCTION
# ============================================================================

# In Azure AD App Registration, configure redirect URI as:
# https://the-grid-v2.azurewebsites.net/oidc/callback/
#
# (Replace 'the-grid-v2' with your actual Azure App Service name)
#
# Set these application settings in Azure App Service Configuration:
# - OIDC_RP_CLIENT_ID: Application (client) ID from Azure AD app registration
# - OIDC_RP_CLIENT_SECRET: Client secret value from Azure AD app registration
# - OIDC_TENANT_ID: Directory (tenant) ID from Azure AD (or use 'common' for multi-tenant)
# - CSRF_TRUSTED_ORIGINS: https://the-grid-v2.azurewebsites.net (and any custom domains)
#
# Optional settings:
# - OIDC_RP_SIGN_ALGO: RS256 (default, usually not needed to set)
#
# The OIDC configuration is inherited from base.py and will use these environment variables.
