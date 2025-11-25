# ScreenCloud Integration Guide

## Overview

The `digital_signage` app has been refactored to support **Screen Manager + Player** functionality for ScreenCloud integration. This allows you to create and manage multiple screen experiences that can be displayed on TVs via ScreenCloud's "Web Page" source.

## Architecture

### Phase 1: Test Screen (Current Implementation)

This initial phase implements:
- **Screen Model**: Database model for managing screen configurations
- **Player View**: Unauthenticated view for displaying screens
- **Test Layout**: A simple, styled test page with placeholder data

### Future Phases

Phase 2+ will add:
- Real Data Connect integration (profit by location, device sales, etc.)
- Additional layout types (profit_by_location, device_sales, custom)
- Dynamic data refresh from external APIs

---

## Key Components

### 1. Screen Model (`digital_signage/models.py`)

**Purpose**: Represents a logical screen experience that can be displayed via ScreenCloud.

**Fields**:
- `name`: Descriptive name (e.g., "Store 1 Main Display")
- `slug`: URL-safe identifier (auto-generated from name)
- `is_active`: Boolean flag to enable/disable screens
- `layout_type`: Choice field for layout template (currently only 'test')
- `html_override`, `css_override`, `js_override`: For custom layouts (Phase 2+)
- `created_at`, `updated_at`: Timestamps

**Methods**:
- `get_play_url()`: Returns the player URL for this screen

**Example Usage**:
```python
screen = Screen.objects.create(
    name="Test Screen",
    slug="test",
    layout_type="test",
    is_active=True
)
# Player URL: /signage/play/test/
```

### 2. ScreenPlayView (`digital_signage/views.py`)

**Purpose**: Renders full-screen, TV-optimized content for ScreenCloud.

**Key Features**:
- **NO AUTHENTICATION REQUIRED** - ScreenCloud needs anonymous access
- Dynamic template selection based on `layout_type`
- 404 if screen not found or inactive
- Provides test data for 'test' layout

**URL**: `/signage/play/<slug>/`

**Example**: `/signage/play/test/`

### 3. Full-Screen Player Template (`digital_signage/templates/digital_signage/screen_test_play.html`)

**Purpose**: Full-screen TV display with no navigation or chrome.

**Design**:
- Dark background (#050506, #000000)
- Grid-style layout with 3 columns
- Purple (#6434f8), cyan (#00f0ff), pink (#ff3b81) accents
- Sharp rectangular cards matching The Grid aesthetic
- Responsive design for different screen sizes
- Auto-refresh every 60 seconds

**Test Data Display**:
- Store name
- Profit (cyan accent)
- Device sales (pink accent)

### 4. Admin Interface (`digital_signage/admin.py`)

**Purpose**: Easy management of Screen instances.

**Features**:
- List view with name, slug, layout type, active status
- Clickable "Play" links to preview screens
- Auto-slug generation from name
- Copy-friendly play URLs
- Collapsible sections for advanced options

**Workflow**:
1. Go to Django admin → Digital Signage → Screens
2. Click "Add Screen"
3. Enter name (e.g., "Test Screen")
4. Slug auto-generates (or customize)
5. Select layout type: "Test Layout"
6. Save
7. Copy play URL from admin
8. Use URL in ScreenCloud

---

## Usage: ScreenCloud Integration

### Step 1: Create a Screen in Django Admin

1. Navigate to: `https://yourdomain.com/admin/digital_signage/screen/`
2. Click "Add Screen"
3. Fill in:
   - **Name**: `Test Screen`
   - **Slug**: `test` (auto-generated)
   - **Layout Type**: `Test Layout`
   - **Is Active**: ✓ (checked)
4. Save

### Step 2: Get the Play URL

After saving, the admin will display the play URL:
```
Relative URL: /signage/play/test/
Full URL: https://yourdomain.com/signage/play/test/
```

### Step 3: Configure ScreenCloud

1. Log into ScreenCloud
2. Add a new "Web Page" source
3. Enter the full play URL: `https://yourdomain.com/signage/play/test/`
4. Set refresh interval (optional - page auto-refreshes every 60 seconds)
5. Assign to your screen(s)

### Step 4: Verify Display

The screen should now display:
- Title: "Test Screen – The Grid"
- Three data cards showing:
  - Downtown Store (Profit: $123,456.78, Device Sales: 42)
  - West End Location (Profit: $89,012.34, Device Sales: 28)
  - North Branch (Profit: $156,789.01, Device Sales: 55)

---

## URL Structure

### Player URLs (NO AUTH)
```
/signage/play/<slug>/
```

Examples:
- `/signage/play/test/` - Test screen
- `/signage/play/store-1/` - Future: Store 1 screen
- `/signage/play/hq-dashboard/` - Future: HQ dashboard

### Dashboard URLs (AUTH REQUIRED)
```
/signage/                   - Old dashboard (kept for compatibility)
/signage/dashboard/         - Old dashboard
/signage/sales/             - Sales data list
/signage/kpi/               - KPI metrics list
```

---

## Security Considerations

### Why No Authentication on Player View?

ScreenCloud needs to access the player URLs directly as a "Web Page" source. If authentication were required:
- ScreenCloud would hit the login page instead of the content
- OAuth flows wouldn't work in an iframe/web page context
- Screens would fail to load

### Mitigations:

1. **Slug-based URLs**: Screens are not easily discoverable without knowing the slug
2. **is_active Flag**: Inactive screens return 404
3. **No Sensitive Data (Phase 1)**: Test layout shows placeholder data only
4. **Future**: Phase 2+ will implement:
   - Token-based authentication in URL parameters (optional)
   - IP whitelisting for ScreenCloud servers
   - Data sanitization for public display

---

## Old Dashboard Code

The existing `DisplayDashboardView`, `SalesDataListView`, and `KPIListView` have been **kept intact** and remain accessible at:
- `/signage/` or `/signage/dashboard/`
- `/signage/sales/`
- `/signage/kpi/`

These views still require authentication and serve their original purpose.

---

## Database Migrations

A new migration has been created:
```
digital_signage/migrations/0002_screen.py
```

To apply:
```bash
python manage.py migrate digital_signage
```

---

## Future Development Roadmap

### Phase 2: Real Data Layouts
- Add `profit_by_location` layout
- Connect to Data Connect API for live profit data
- Add `device_sales` layout for real-time device sales metrics

### Phase 3: Custom Layouts
- Enable `html_override`, `css_override`, `js_override` fields
- Allow fully custom screen experiences
- Add template editor in admin (optional)

### Phase 4: Advanced Features
- Screen scheduling (show different content at different times)
- Multi-zone layouts (split screen into regions)
- Webhook support for external triggers
- Analytics/view tracking

---

## Troubleshooting

### Screen Returns 404
- Check that `is_active = True` in admin
- Verify the slug matches the URL
- Ensure migrations have been applied

### Screen Shows Login Page
- The player URL should NOT require authentication
- Check that you're using `/signage/play/<slug>/` (not `/signage/dashboard/`)
- Verify middleware isn't forcing authentication globally

### Placeholder Data Not Showing
- Check that `layout_type = 'test'` in the Screen model
- Verify the template path is correct
- Inspect browser console for errors

### ScreenCloud Can't Load the Page
- Check that the URL is publicly accessible (not localhost)
- Verify SSL certificate is valid (ScreenCloud requires HTTPS)
- Check firewall/security group settings

---

## Contact / Support

For issues or questions about ScreenCloud integration, consult:
- Django admin: `/admin/digital_signage/screen/`
- This documentation: `digital_signage/SCREENCLOUD_INTEGRATION.md`
- Platform overview: `docs/PLATFORM_OVERVIEW.md`
