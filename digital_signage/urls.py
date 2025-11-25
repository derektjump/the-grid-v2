"""
Digital Signage URL Configuration

This module defines URL patterns for the digital signage design and data management portal.

IMPORTANT: This app is NOT a signage player or live dashboard.
It is an INTERNAL DESIGN + DATA PORTAL where we:
  - Design screen content (HTML/CSS/JS)
  - Preview what screens will look like
  - Manage signage-related data
  - Copy final designs into ScreenCloud Playground

URL Patterns:
    PRIMARY DESIGN MANAGEMENT URLS (ACTIVE):
    - /designs/ - List all screen designs
    - /designs/new/ - Create a new screen design
    - /designs/<slug>/edit/ - Edit an existing screen design
    - /designs/<slug>/preview/ - Preview a screen design

    DEPRECATED DASHBOARD URLS (kept for backward compatibility):
    - /play/<slug>/ - Legacy ScreenCloud player (DEPRECATED)
    - /dashboard/ - Legacy dashboard (DEPRECATED)
    - /sales/ - Legacy sales data list (DEPRECATED)
    - /kpi/ - Legacy KPI list (DEPRECATED)
"""

from django.urls import path
from .views import (
    # API endpoints
    test_profit_data,
    # Active design management views
    ScreenDesignListView,
    ScreenDesignUpdateView,
    ScreenDesignPreviewView,
    # Deprecated legacy views
    ScreenPlayView,
    SalesDataListView,
    KPIListView,
    DisplayDashboardView,
)

# App namespace for URL reversing
app_name = 'digital_signage'

urlpatterns = [
    # ========================================================================
    # API ENDPOINTS FOR SCREENCLOUD / EXTERNAL INTEGRATIONS
    # ========================================================================
    # These endpoints are for external systems (ScreenCloud) to fetch live data.
    # Authentication: API key via X-API-KEY header or api_key query parameter

    # Test endpoint with static data for ScreenCloud connectivity verification
    path('api/test-profit-by-location/', test_profit_data, name='test_profit_data'),

    # ========================================================================
    # PRIMARY DESIGN MANAGEMENT URLS (ACTIVE)
    # ========================================================================
    # These are the main features of this app going forward.

    # List all screen designs
    path('designs/', ScreenDesignListView.as_view(), name='screen_design_list'),

    # Create a new screen design (no slug parameter)
    path('designs/new/', ScreenDesignUpdateView.as_view(), name='screen_design_create'),

    # Edit an existing screen design
    path('designs/<slug:slug>/edit/', ScreenDesignUpdateView.as_view(), name='screen_design_edit'),

    # Preview a screen design (internal use only, requires login)
    path('designs/<slug:slug>/preview/', ScreenDesignPreviewView.as_view(), name='screen_design_preview'),

    # ========================================================================
    # DEPRECATED DASHBOARD URLS (kept for backward compatibility)
    # ========================================================================
    # These URLs are DEPRECATED and should not be used for new features.
    # They were created when digital_signage was a sales dashboard.
    # They are commented out but can be re-enabled if needed for legacy data.
    #
    # To remove completely:
    # 1. Ensure no external systems are using these URLs
    # 2. Remove the URL patterns below
    # 3. Remove the deprecated views from views.py
    # 4. Remove the deprecated templates
    # ========================================================================

    # Legacy ScreenCloud player endpoint (NO AUTHENTICATION)
    # DEPRECATED: Use ScreenDesign + ScreenDesignPreviewView instead
    path('play/<slug:slug>/', ScreenPlayView.as_view(), name='screen_play'),

    # Legacy dashboard views (DEPRECATED)
    # DEPRECATED: This app is no longer a sales dashboard
    path('', DisplayDashboardView.as_view(), name='dashboard'),
    path('dashboard/', DisplayDashboardView.as_view(), name='display_dashboard'),

    # Legacy sales data views (DEPRECATED)
    # DEPRECATED: Sales data management is not the primary feature
    path('sales/', SalesDataListView.as_view(), name='sales_data_list'),

    # Legacy KPI views (DEPRECATED)
    # DEPRECATED: KPI management is not the primary feature
    path('kpi/', KPIListView.as_view(), name='kpi_list'),
]

# MIGRATION NOTE:
# The primary entry point for this app should now be:
#   /digital-signage/designs/
#
# The old entry point was:
#   /digital-signage/ (which showed the dashboard)
#
# Consider updating any navigation links, hub tiles, or bookmarks
# to point to the new designs list URL.
