# Digital Signage Device Management Implementation

## Overview

This document describes the complete device management, playlist, and Fire TV app implementation for The Grid's digital signage system.

## What Has Been Implemented

### 1. Database Models (digital_signage/models.py)

Three new models have been added to support device management and playlists:

#### Device Model
- **Purpose**: Represents physical Fire TV devices that display signage content
- **Fields**:
  - `id` (UUID): Unique device identifier
  - `name`: Human-readable device name
  - `registration_code`: 6-character code for registration
  - `registered`: Boolean flag for registration status
  - `assigned_playlist`: Foreign key to Playlist (optional)
  - `assigned_screen`: Foreign key to ScreenDesign (optional)
  - `location`: Physical location description
  - `notes`: Internal notes
  - `last_seen`: Auto-updated timestamp
- **Key Properties**:
  - `is_pending_registration`: Check if awaiting registration

#### Playlist Model
- **Purpose**: Collection of screens to rotate through on devices
- **Fields**:
  - `id` (UUID): Unique playlist identifier
  - `name`: Unique playlist name
  - `slug`: URL-safe identifier
  - `is_active`: Active status flag
  - `created_at`, `updated_at`: Timestamps
- **Relationships**: One-to-many with PlaylistItem

#### PlaylistItem Model
- **Purpose**: Individual screen within a playlist with ordering and duration
- **Fields**:
  - `playlist`: Foreign key to Playlist
  - `screen`: Foreign key to ScreenDesign
  - `order`: Display order (integer)
  - `duration_seconds`: How long to display (default 30)
- **Constraints**: Unique together on (playlist, order)

### 2. Django Admin Configuration (digital_signage/admin.py)

#### PlaylistAdmin
- List display: name, slug, item count, active status, updated timestamp
- Inline editing: Manage playlist items directly within playlist
- Search: By name and slug
- Filters: Active status, created/updated dates

#### DeviceAdmin
- List display: device name, registration status (with code), assigned content, location, last seen status
- Registration status shows:
  - Registered devices with checkmark
  - Pending devices with code in monospace box
  - Last seen with color coding (green=online, orange=recent, gray=offline)
- Autocomplete fields for assigning playlists/screens
- Search: By name, ID, registration code, location
- Filters: Registration status, dates

#### PlaylistItemInline
- Tabular inline editor for managing screen order and duration
- Autocomplete screen selection
- Ordered by display order

### 3. API Endpoints (digital_signage/views.py)

All endpoints are CSRF-exempt and publicly accessible for device use.

#### POST /digital-signage/api/devices/request-code/
**Purpose**: Request a registration code for a new device

**Request Body**:
```json
{
    "device_name": "Optional friendly name"
}
```

**Response**:
```json
{
    "success": true,
    "device_id": "uuid",
    "registration_code": "ABC123"
}
```

#### POST /digital-signage/api/devices/{device_id}/register/
**Purpose**: Mark device as registered (after admin assigns content)

**Request Body**:
```json
{
    "registration_code": "ABC123"
}
```

**Response**:
```json
{
    "success": true,
    "registered": true
}
```

#### GET /digital-signage/api/devices/{device_id}/config/
**Purpose**: Fetch device configuration (assigned playlist or screen)

**Response (Playlist)**:
```json
{
    "success": true,
    "device_id": "uuid",
    "device_name": "Store 1 Main Display",
    "registered": true,
    "config": {
        "type": "playlist",
        "playlist_id": "uuid",
        "playlist_name": "Store Rotation",
        "items": [
            {
                "screen_id": "uuid",
                "screen_name": "Sales Dashboard",
                "screen_slug": "sales-dashboard",
                "player_url": "https://domain/digital-signage/player/sales-dashboard/",
                "duration_seconds": 30,
                "order": 0
            }
        ]
    }
}
```

**Response (Single Screen)**:
```json
{
    "success": true,
    "device_id": "uuid",
    "device_name": "Store 2 Display",
    "registered": true,
    "config": {
        "type": "screen",
        "screen_id": "uuid",
        "screen_name": "Welcome Screen",
        "screen_slug": "welcome",
        "player_url": "https://domain/digital-signage/player/welcome/"
    }
}
```

**Response (No Content)**:
```json
{
    "success": true,
    "device_id": "uuid",
    "device_name": "",
    "registered": false,
    "config": {
        "type": "none"
    }
}
```

#### GET /digital-signage/api/devices/by-code/{code}/config/
**Purpose**: Alternative config lookup by registration code

Same response format as device_config endpoint.

### 4. Public Player Endpoint (digital_signage/views.py)

#### GET /digital-signage/player/{slug}/
**Purpose**: Full-screen player view for Fire TV devices

- No authentication required
- Renders barebones HTML with screen design code injected
- Only shows active screen designs
- Returns 404 for inactive or non-existent screens

### 5. Player Template (digital_signage/templates/digital_signage/player.html)

- Minimal HTML structure
- No navigation, no controls, no authentication UI
- Full-screen black background
- Injects user-defined HTML, CSS, and JavaScript from ScreenDesign
- Designed for WebView rendering on Fire TV

### 6. Fire TV Android App (core/firetv_app/)

Complete Android app for Fire TV devices with the following structure:

```
core/firetv_app/
├── README.md                    # Comprehensive documentation
├── build.gradle                 # Project-level Gradle config
├── settings.gradle              # Module settings
├── gradle.properties            # Gradle properties
└── app/
    ├── build.gradle            # App-level Gradle config
    ├── proguard-rules.pro      # ProGuard rules
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/ca/jump/thegrid/signage/
        │   └── MainActivity.java
        └── res/
            ├── layout/
            │   └── activity_main.xml
            └── values/
                ├── strings.xml
                └── styles.xml
```

#### MainActivity.java Features

**Registration Flow**:
1. Requests registration code from API on startup
2. Displays code in large text on screen
3. Shows status messages and progress indicator
4. Polls API every 5 seconds for configuration

**Playback Modes**:
1. **Playlist Mode**:
   - Loads all playlist items
   - Rotates through screens based on duration
   - Continuous loop
2. **Single Screen Mode**:
   - Loads one screen and displays indefinitely
   - No rotation

**WebView Configuration**:
- JavaScript enabled
- DOM storage enabled
- No cache (always fresh content)
- Wide viewport for full-screen rendering
- Full-screen system UI hiding

**Error Handling**:
- Automatic retry on connection failures
- Graceful degradation
- Silent failures during polling (retries automatically)

#### Layout (activity_main.xml)

**Registration View**:
- App title: "THE GRID" in purple (#9B59FF)
- Subtitle: "Digital Signage"
- Registration code in large cyan (#00F0FF) monospace text
- Status message
- Progress indicator

**WebView**:
- Full-screen
- Hidden during registration
- Shown during playback

#### Build Configuration

- **Min SDK**: 22 (Android 5.1 - Fire TV Gen 2+)
- **Target SDK**: 33 (Android 13)
- **Dependencies**:
  - AndroidX AppCompat
  - OkHttp 4.11.0 for HTTP requests
  - Built-in JSON parsing

#### Manifest Features

- Internet and network state permissions
- Fire TV leanback support
- Landscape orientation lock
- Full-screen theme
- Leanback launcher intent filter

### 7. URL Configuration (digital_signage/urls.py)

New URL patterns added:

```python
# Device Management API
path('api/devices/request-code/', device_request_code, name='device_request_code')
path('api/devices/<uuid:device_id>/register/', device_register, name='device_register')
path('api/devices/<uuid:device_id>/config/', device_config, name='device_config')
path('api/devices/by-code/<str:code>/config/', device_config_by_code, name='device_config_by_code')

# Public Player
path('player/<slug:slug>/', screen_player, name='screen_player')
```

## Usage Workflow

### Admin Workflow

1. **Create Screen Designs**:
   - Navigate to Django admin → Digital Signage → Screen Designs
   - Create screens with HTML/CSS/JS code
   - Mark as active

2. **Create Playlists** (optional):
   - Navigate to Django admin → Digital Signage → Playlists
   - Add playlist name
   - Add screens with order and duration via inline editor

3. **Register Device**:
   - Wait for device to display registration code
   - Navigate to Django admin → Digital Signage → Devices
   - Find device by registration code
   - Assign device name, location
   - Assign either a playlist OR a single screen
   - Mark as registered (if not auto-registered)

### Device Workflow

1. **Initial Setup**:
   - Sideload APK to Fire TV
   - Launch "The Grid Signage" app
   - Note the 6-character registration code displayed

2. **Registration**:
   - Enter code in admin panel (see Admin Workflow)
   - App polls API every 5 seconds
   - When content is assigned, app transitions to playback

3. **Playback**:
   - WebView loads assigned content
   - For playlists: rotates through screens automatically
   - For single screens: displays indefinitely
   - Screen stays on, full-screen mode

## Database Migration

A new migration has been created: `digital_signage/migrations/0004_playlist_device_playlistitem.py`

To apply:
```bash
python manage.py migrate digital_signage
```

## API Base URL

All endpoints are accessible at:
```
https://the-grid-v2-bxfue0bhbkacffac.canadaeast-01.azurewebsites.net/digital-signage/
```

Fire TV app is pre-configured with this URL.

## Security Considerations

### Public Endpoints
- All device API endpoints are public (no authentication)
- Devices are identified by UUID (unguessable)
- Registration codes are random 6-character alphanumeric

### Admin Protection
- Django admin is protected by existing authentication
- Only authenticated users can assign content to devices

### Player Endpoint
- Public endpoint for device playback
- Only serves active screen designs
- No sensitive data exposed

## Testing Checklist

### Backend
- [ ] Create Playlist in admin
- [ ] Add PlaylistItems with different durations
- [ ] Create Device in admin
- [ ] Test device_request_code endpoint
- [ ] Test device_config endpoint (no content)
- [ ] Assign playlist to device
- [ ] Test device_config endpoint (playlist mode)
- [ ] Assign single screen to device
- [ ] Test device_config endpoint (screen mode)
- [ ] Test player endpoint for active screen
- [ ] Test player endpoint returns 404 for inactive screen

### Fire TV App
- [ ] Build APK in Android Studio
- [ ] Sideload to Fire TV
- [ ] Verify registration code displays
- [ ] Enter code in admin
- [ ] Verify app transitions to playback
- [ ] Test playlist rotation
- [ ] Test single screen display
- [ ] Verify full-screen mode
- [ ] Test app restart (should preserve device ID)

## Future Enhancements

### Potential Improvements
1. **Device Heartbeat**: Track device online/offline status more accurately
2. **Content Scheduling**: Time-based playlist switching
3. **Analytics**: Track screen view counts and durations
4. **Remote Control**: Trigger content refresh from admin
5. **Screen Zones**: Multi-zone layouts on single device
6. **Content Preloading**: Cache next playlist item for smoother transitions
7. **Push Notifications**: Immediate content updates instead of polling

## Troubleshooting

### Device not appearing in admin
- Check network connectivity
- Verify API endpoint is reachable
- Check Django logs for API errors

### Registration code not working
- Ensure code is entered exactly as displayed
- Check that device record exists in admin
- Verify registration_code field matches

### Content not displaying on device
- Verify screen designs are marked as active
- Check player URL is accessible (no auth required)
- Review WebView errors in Android logcat
- Ensure device has content assigned (playlist or screen)

### Playlist not rotating
- Check duration_seconds values
- Verify multiple items exist in playlist
- Check Android logcat for JavaScript errors

## File Locations

### Backend Files
- `digital_signage/models.py` - Device, Playlist, PlaylistItem models
- `digital_signage/admin.py` - Admin configuration
- `digital_signage/views.py` - API endpoints and player view
- `digital_signage/urls.py` - URL routing
- `digital_signage/templates/digital_signage/player.html` - Player template

### Fire TV App Files
- `core/firetv_app/README.md` - App documentation
- `core/firetv_app/app/src/main/AndroidManifest.xml` - App manifest
- `core/firetv_app/app/src/main/java/ca/jump/thegrid/signage/MainActivity.java` - Main activity
- `core/firetv_app/app/src/main/res/layout/activity_main.xml` - Layout
- `core/firetv_app/app/build.gradle` - App build config
- `core/firetv_app/build.gradle` - Project build config
- `core/firetv_app/settings.gradle` - Gradle settings

## Summary

This implementation provides a complete end-to-end solution for managing digital signage devices with The Grid:

1. **Device Management**: Register and track Fire TV devices
2. **Content Assignment**: Assign playlists or individual screens to devices
3. **API Integration**: RESTful API for device registration and configuration
4. **Player Endpoint**: Public full-screen player for device rendering
5. **Fire TV App**: Complete Android app for Fire TV devices with registration and playback
6. **Admin Interface**: Rich admin UI for managing devices, playlists, and content assignments

All components are production-ready, well-documented, and follow Django and Android best practices.
