"""
URL configuration for the_grid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from core.views import health_check

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Health check endpoint
    path('health/', health_check, name='health_check'),

    # Hub routes (landing page at root)
    path('', include('hub.urls')),

    # TODO: Add additional app URLs as they are developed
    # path('lifecycle/', include('lifecycle.urls')),
    # path('shopify/', include('shopify.urls')),
    # path('analytics/', include('analytics.urls')),
    # path('signage/', include('signage.urls')),
    # path('agents/', include('agents.urls')),
]
