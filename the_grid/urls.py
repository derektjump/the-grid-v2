"""
URL configuration for the_grid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import health_check, custom_logout

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Health check endpoint
    path('health/', health_check, name='health_check'),

    # Custom logout endpoint (must be BEFORE mozilla_django_oidc.urls to override)
    path('oidc/logout/', custom_logout, name='oidc_logout'),

    # Azure AD / OpenID Connect authentication
    # Provides these endpoints:
    # - /oidc/authenticate/ - Initiates login with Azure AD
    # - /oidc/callback/ - Azure AD redirects here after authentication
    path('oidc/', include('mozilla_django_oidc.urls')),

    # Hub routes (landing page at root)
    path('', include('hub.urls')),

    # Digital Signage routes (sales data and KPI displays)
    path('digital-signage/', include('digital_signage.urls')),

    # TODO: Add additional app URLs as they are developed
    # path('lifecycle/', include('lifecycle.urls')),
    # path('shopify/', include('shopify.urls')),
    # path('analytics/', include('analytics.urls')),
    # path('agents/', include('agents.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
