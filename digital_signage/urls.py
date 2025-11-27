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
    MAIN TABBED OVERVIEW (PRIMARY ENTRY POINT):
    - / - Main dashboard with Overview/Designs/Playlists/Devices tabs

    DEVICE MANAGEMENT:
    - /devices/<uuid>/ - Individual device detail/edit page
    - /devices/<uuid>/delete/ - Delete device confirmation

    PLAYLIST MANAGEMENT:
    - /playlists/create/ - Create new playlist
    - /playlists/<uuid>/edit/ - Edit existing playlist

    DESIGN MANAGEMENT:
    - /designs/ - List all screen designs
    - /designs/new/ - Create a new screen design
    - /designs/<slug>/edit/ - Edit an existing screen design
    - /designs/<slug>/preview/ - Preview a screen design

    AJAX ENDPOINTS (UI INTERACTIONS):
    - /ajax/devices/register-with-code/ - Register device with code
    - /ajax/devices/<uuid>/assign-content/ - Assign content to device

    API ENDPOINTS (FIRE TV DEVICES):
    - /api/devices/request-code/ - Request registration code
    - /api/devices/<uuid>/register/ - Mark device as registered
    - /api/devices/<uuid>/config/ - Get device configuration
    - /api/devices/by-code/<code>/config/ - Get config by code

    PUBLIC PLAYER:
    - /player/<slug>/ - Public full-screen player for devices

    DEPRECATED DASHBOARD URLS (kept for backward compatibility):
    - /play/<slug>/ - Legacy ScreenCloud player (DEPRECATED)
    - /dashboard/ - Legacy dashboard (DEPRECATED)
    - /sales/ - Legacy sales data list (DEPRECATED)
    - /kpi/ - Legacy KPI list (DEPRECATED)
"""

from django.urls import path
from .views import (
    # Main tabbed overview interface
    OverviewView,
    DeviceDetailView,
    DeviceDeleteView,
    # AJAX endpoints
    register_device_with_code,
    assign_device_content,
    upload_media,
    create_folder,
    # Playlist management
    PlaylistCreateView,
    PlaylistUpdateView,
    # API endpoints
    test_profit_data,
    device_request_code,
    device_register,
    device_config,
    device_config_by_code,
    # Active design management views
    ScreenDesignListView,
    ScreenDesignUpdateView,
    ScreenDesignPreviewView,
    screen_player,
    media_player,
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
    # DEVICE MANAGEMENT API ENDPOINTS
    # ========================================================================
    # These endpoints are for Fire TV device registration and configuration.
    # No authentication required - devices use UUID and registration codes.

    # Request a registration code for a new device
    path('api/devices/request-code/', device_request_code, name='device_request_code'),

    # Mark device as registered (after admin assigns content)
    path('api/devices/<uuid:device_id>/register/', device_register, name='device_register'),

    # Get device configuration (assigned playlist or screen)
    path('api/devices/<uuid:device_id>/config/', device_config, name='device_config'),

    # Get device configuration by registration code (alternative lookup)
    path('api/devices/by-code/<str:code>/config/', device_config_by_code, name='device_config_by_code'),

    # ========================================================================
    # PUBLIC PLAYER ENDPOINT
    # ========================================================================
    # Full-screen player for Fire TV devices (no authentication required)

    # Public player endpoint for displaying screens on devices
    path('player/<slug:slug>/', screen_player, name='screen_player'),

    # Public player endpoint for displaying media assets on devices
    path('media/<slug:slug>/', media_player, name='media_player'),

    # ========================================================================
    # MAIN TABBED OVERVIEW INTERFACE (PRIMARY ENTRY POINT)
    # ========================================================================
    # This is the new default landing page for Digital Signage

    # Main overview dashboard with tabs for Overview/Designs/Playlists/Devices
    path('', OverviewView.as_view(), name='overview'),

    # ========================================================================
    # DEVICE MANAGEMENT URLS
    # ========================================================================
    # Individual device detail and management pages

    # Device detail/edit page
    path('devices/<uuid:pk>/', DeviceDetailView.as_view(), name='device_detail'),

    # Delete device with confirmation
    path('devices/<uuid:pk>/delete/', DeviceDeleteView.as_view(), name='device_delete'),

    # ========================================================================
    # AJAX ENDPOINTS FOR UI INTERACTIONS
    # ========================================================================
    # These endpoints are called via JavaScript from the frontend

    # Register a device using its registration code (from Add Device modal)
    path('ajax/devices/register-with-code/', register_device_with_code, name='register_device'),

    # Assign playlist or screen to a device (from device cards)
    path('ajax/devices/<uuid:pk>/assign-content/', assign_device_content, name='assign_content'),

    # ========================================================================
    # MEDIA LIBRARY AJAX ENDPOINTS
    # ========================================================================
    # These endpoints handle media asset upload and folder management

    # Upload media files (images/videos)
    path('ajax/media/upload/', upload_media, name='upload_media'),

    # Create a new media folder
    path('ajax/folders/create/', create_folder, name='create_folder'),

    # ========================================================================
    # PLAYLIST MANAGEMENT URLS
    # ========================================================================
    # Create and edit playlists

    # Create new playlist
    path('playlists/create/', PlaylistCreateView.as_view(), name='playlist_create'),

    # Edit existing playlist
    path('playlists/<uuid:pk>/edit/', PlaylistUpdateView.as_view(), name='playlist_edit'),

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
    path('dashboard/', DisplayDashboardView.as_view(), name='display_dashboard'),

    # Legacy sales data views (DEPRECATED)
    # DEPRECATED: Sales data management is not the primary feature
    path('sales/', SalesDataListView.as_view(), name='sales_data_list'),

    # Legacy KPI views (DEPRECATED)
    # DEPRECATED: KPI management is not the primary feature
    path('kpi/', KPIListView.as_view(), name='kpi_list'),
]

# MIGRATION NOTE:
# The primary entry point for this app is now:
#   /digital-signage/ (which shows the new tabbed overview)
#
# The old entry point was:
#   /digital-signage/ (which showed the deprecated dashboard)
#
# All navigation links, hub tiles, and bookmarks should now point to:
#   {% url 'digital_signage:overview' %}
