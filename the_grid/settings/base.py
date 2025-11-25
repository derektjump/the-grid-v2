"""
Django settings for the_grid project - Base Configuration

Settings common to all environments (local, production, etc.)
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# This will be overridden in production.py from environment variables
SECRET_KEY = 'django-insecure-REPLACE-THIS-IN-PRODUCTION'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORS support for external integrations (ScreenCloud, etc.)
    'corsheaders',

    # Azure AD / OpenID Connect authentication
    'mozilla_django_oidc',

    # The Grid apps
    'core.apps.CoreConfig',
    'hub.apps.HubConfig',
    'digital_signage.apps.DigitalSignageConfig',  # Digital signage for sales data and KPI displays
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # CORS middleware - must be before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # OIDC session refresh middleware (optional - keeps tokens fresh)
    'mozilla_django_oidc.middleware.SessionRefresh',
]

ROOT_URLCONF = 'the_grid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core' / 'templates',
            BASE_DIR / 'hub' / 'templates',
            BASE_DIR / 'digital_signage' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'the_grid.wsgi.application'


# Database
# This will be overridden in local.py and production.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validators.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validators.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validators.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validators.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================================
# AZURE AD / ENTRA ID AUTHENTICATION (OpenID Connect)
# ============================================================================

# Authentication backends - OIDC must come BEFORE ModelBackend
# This allows Azure AD authentication to be tried first, with fallback to Django auth
AUTHENTICATION_BACKENDS = [
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Azure AD / Entra ID Configuration
# These values come from environment variables and must be set in:
# - Local: .env file or system environment
# - Azure: App Service Configuration -> Application settings

OIDC_RP_CLIENT_ID = os.environ.get('OIDC_RP_CLIENT_ID', '')
OIDC_RP_CLIENT_SECRET = os.environ.get('OIDC_RP_CLIENT_SECRET', '')
OIDC_TENANT_ID = os.environ.get('OIDC_TENANT_ID', 'common')  # 'common' for multi-tenant, or specific tenant ID

# Azure AD OpenID Connect Endpoints
# Using v2.0 endpoints for modern Azure AD / Microsoft Identity Platform
OIDC_OP_AUTHORIZATION_ENDPOINT = f"https://login.microsoftonline.com/{OIDC_TENANT_ID}/oauth2/v2.0/authorize"
OIDC_OP_TOKEN_ENDPOINT = f"https://login.microsoftonline.com/{OIDC_TENANT_ID}/oauth2/v2.0/token"
OIDC_OP_USER_ENDPOINT = "https://graph.microsoft.com/oidc/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"https://login.microsoftonline.com/{OIDC_TENANT_ID}/discovery/v2.0/keys"

# Signing algorithm used by Azure AD (RS256 is standard for Azure AD)
OIDC_RP_SIGN_ALGO = os.environ.get('OIDC_RP_SIGN_ALGO', 'RS256')

# Scopes to request from Azure AD
# openid: Required for OIDC
# profile: Gets user profile information
# email: Gets user email address
OIDC_RP_SCOPES = "openid profile email"

# Create users in Django database if they don't exist
OIDC_CREATE_USER = True

# Session renewal settings
# Renew ID token every 15 minutes (Azure AD tokens typically last 1 hour)
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 900

# Login/Logout URL Configuration
LOGIN_URL = '/oidc/authenticate/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Allow sessions to persist after logout redirect
# This prevents issues with Azure AD logout flow
OIDC_OP_LOGOUT_URL_METHOD = 'mozilla_django_oidc.views.get_next_url'


# ============================================================================
# CORS CONFIGURATION
# ============================================================================

# CORS (Cross-Origin Resource Sharing) configuration
# Allows ScreenCloud and other external services to fetch data from our API endpoints
#
# SECURITY NOTE:
# - CORS_ALLOW_ALL_ORIGINS = True is convenient for development and allows any domain
# - For production, consider restricting to specific origins for better security:
#
#   CORS_ALLOW_ALL_ORIGINS = False
#   CORS_ALLOWED_ORIGINS = [
#       'https://screencloud.com',
#       'https://*.screencloud.com',
#       'https://app.screencloud.com',
#   ]
#
# - Set CORS_ALLOW_CREDENTIALS = True if you need to send cookies/auth headers cross-origin
# - The custom 'x-api-key' header is included for API key authentication

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (can restrict later to specific domains)
CORS_ALLOW_CREDENTIALS = False  # Don't send cookies cross-origin (API uses key-based auth)

# Allowed headers that can be sent in cross-origin requests
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-api-key',  # Custom header for API authentication
    'x-csrftoken',
    'x-requested-with',
]


# ============================================================================
# DIGITAL SIGNAGE API CONFIGURATION
# ============================================================================

# API key for ScreenCloud and other external integrations to fetch signage data
# This key must be set in environment variables:
# - Local: Add to .env file or system environment
# - Azure: App Service Configuration -> Application settings -> SIGNAGE_API_KEY
SIGNAGE_API_KEY = os.environ.get('SIGNAGE_API_KEY', '')
