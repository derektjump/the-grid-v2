"""
Digital Signage Admin Configuration

This module configures the Django admin interface for the digital signage app,
providing easy management of screen designs, sales data, and KPI metrics.

IMPORTANT: This app is for design and data management only, NOT live playback.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ScreenDesign, Screen, SalesData, KPI, Device, Playlist, PlaylistItem


@admin.register(ScreenDesign)
class ScreenDesignAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScreenDesign model.

    Provides management interface for designing and previewing screen content
    that will be copied into ScreenCloud Playground.
    """

    list_display = [
        'name',
        'slug',
        'is_active_indicator',
        'preview_link',
        'updated_at',
    ]

    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'name',
        'slug',
        'description',
    ]

    # Enable autocomplete for use in Device/PlaylistItem admin
    # This allows searching by name when assigning screens
    def get_search_results(self, request, queryset, search_term):
        """Enable autocomplete search functionality."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

    prepopulated_fields = {
        'slug': ('name',)
    }

    readonly_fields = ['created_at', 'updated_at', 'preview_url_display']

    fieldsets = (
        ('Design Information', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('HTML/CSS/JS Code', {
            'fields': ('html_code', 'css_code', 'js_code'),
            'description': 'Design your screen content here. Use the preview link to see how it looks.'
        }),
        ('Internal Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
            'description': 'Internal documentation about this design.'
        }),
        ('Preview & Timestamps', {
            'fields': ('preview_url_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_indicator(self, obj):
        """
        Display active status with visual indicator.

        Args:
            obj: ScreenDesign instance

        Returns:
            str: HTML formatted status indicator
        """
        if obj.is_active:
            return format_html(
                '<span style="color: #00F0FF; font-weight: bold;">✓ Active</span>'
            )
        else:
            return format_html(
                '<span style="color: #888; font-weight: bold;">✗ Inactive</span>'
            )

    is_active_indicator.short_description = 'Status'

    def preview_link(self, obj):
        """
        Display clickable preview link in list view.

        Args:
            obj: ScreenDesign instance

        Returns:
            str: HTML formatted link
        """
        url = obj.get_preview_url()
        return format_html(
            '<a href="{}" target="_blank" style="color: #9B59FF; font-weight: bold;">👁 Preview</a>',
            url
        )

    preview_link.short_description = 'Preview'

    def preview_url_display(self, obj):
        """
        Display full preview URL in detail view.

        Args:
            obj: ScreenDesign instance

        Returns:
            str: Formatted preview URL
        """
        url = obj.get_preview_url()
        return format_html(
            '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; font-family: monospace;">'
            '<strong>Preview URL:</strong> {}<br>'
            '<br>'
            '<em>Click "Preview" above to see how this design looks on a screen.</em>'
            '</div>',
            url
        )

    preview_url_display.short_description = 'Preview URL'


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    """
    Admin configuration for Screen model.

    Provides management interface for ScreenCloud-compatible screen experiences.
    """

    list_display = [
        'name',
        'slug',
        'layout_type',
        'is_active_indicator',
        'play_url_link',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'layout_type',
        'created_at',
    ]

    search_fields = [
        'name',
        'slug',
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    readonly_fields = ['created_at', 'updated_at', 'play_url_display']

    fieldsets = (
        ('Screen Information', {
            'fields': ('name', 'slug', 'is_active', 'layout_type')
        }),
        ('Custom Overrides (Advanced)', {
            'fields': ('html_override', 'css_override', 'js_override'),
            'classes': ('collapse',),
            'description': 'Use these fields for custom HTML/CSS/JS. Leave blank for standard layouts.'
        }),
        ('URLs & Timestamps', {
            'fields': ('play_url_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_indicator(self, obj):
        """
        Display active status with visual indicator.

        Args:
            obj: Screen instance

        Returns:
            str: HTML formatted status indicator
        """
        if obj.is_active:
            return format_html(
                '<span style="color: #00F0FF; font-weight: bold;">✓ Active</span>'
            )
        else:
            return format_html(
                '<span style="color: #888; font-weight: bold;">✗ Inactive</span>'
            )

    is_active_indicator.short_description = 'Status'

    def play_url_link(self, obj):
        """
        Display clickable play URL in list view.

        Args:
            obj: Screen instance

        Returns:
            str: HTML formatted link
        """
        if obj.is_active:
            url = obj.get_play_url()
            return format_html(
                '<a href="{}" target="_blank" style="color: #6434f8; font-weight: bold;">▶ Play</a>',
                url
            )
        else:
            return format_html('<span style="color: #888;">Inactive</span>')

    play_url_link.short_description = 'Play URL'

    def play_url_display(self, obj):
        """
        Display full play URL in detail view.

        Args:
            obj: Screen instance

        Returns:
            str: Formatted play URL with copy instructions
        """
        url = obj.get_play_url()
        full_url = f"https://yourdomain.com{url}"  # TODO: Update with actual domain
        return format_html(
            '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; font-family: monospace;">'
            '<strong>Relative URL:</strong> {}<br>'
            '<strong>Full URL (example):</strong> {}<br>'
            '<br>'
            '<em>Use this URL in ScreenCloud as a "Web Page" source.</em>'
            '</div>',
            url,
            full_url
        )

    play_url_display.short_description = 'ScreenCloud Play URL'


@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    """
    Admin configuration for SalesData model.

    Provides list display, filtering, search, and bulk actions
    for managing sales data records.
    """

    list_display = [
        'store',
        'employee',
        'total_sales_formatted',
        'date',
        'created_at',
    ]

    list_filter = [
        'store',
        'date',
        'created_at',
    ]

    search_fields = [
        'store',
        'employee',
    ]

    date_hierarchy = 'date'

    ordering = ['-date', 'store', 'employee']

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Sales Information', {
            'fields': ('store', 'employee', 'total_sales', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def total_sales_formatted(self, obj):
        """
        Format total sales with currency symbol for display.

        Args:
            obj: SalesData instance

        Returns:
            str: Formatted sales amount
        """
        return format_html(
            '<strong style="color: #00F0FF;">${:,.2f}</strong>',
            obj.total_sales
        )

    total_sales_formatted.short_description = 'Total Sales'
    total_sales_formatted.admin_order_field = 'total_sales'


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    """
    Admin configuration for KPI model.

    Provides list display, filtering, search, and performance indicators
    for managing KPI records.
    """

    list_display = [
        'store',
        'employee',
        'sales_target_formatted',
        'actual_sales_formatted',
        'performance_indicator',
        'date',
        'created_at',
    ]

    list_filter = [
        'store',
        'date',
        'created_at',
    ]

    search_fields = [
        'store',
        'employee',
    ]

    date_hierarchy = 'date'

    ordering = ['-date', 'store', 'employee']

    readonly_fields = ['created_at', 'updated_at', 'performance_percentage_display']

    fieldsets = (
        ('KPI Information', {
            'fields': ('store', 'employee', 'date')
        }),
        ('Targets and Performance', {
            'fields': ('sales_target', 'actual_sales', 'performance_percentage_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def sales_target_formatted(self, obj):
        """
        Format sales target with currency symbol for display.

        Args:
            obj: KPI instance

        Returns:
            str: Formatted target amount
        """
        return format_html(
            '<strong>${:,.2f}</strong>',
            obj.sales_target
        )

    sales_target_formatted.short_description = 'Target'
    sales_target_formatted.admin_order_field = 'sales_target'

    def actual_sales_formatted(self, obj):
        """
        Format actual sales with currency symbol for display.

        Args:
            obj: KPI instance

        Returns:
            str: Formatted actual sales amount
        """
        return format_html(
            '<strong style="color: #00F0FF;">${:,.2f}</strong>',
            obj.actual_sales
        )

    actual_sales_formatted.short_description = 'Actual'
    actual_sales_formatted.admin_order_field = 'actual_sales'

    def performance_indicator(self, obj):
        """
        Display performance indicator with color coding.

        Args:
            obj: KPI instance

        Returns:
            str: HTML formatted performance indicator
        """
        percentage = obj.performance_percentage
        color = '#00F0FF' if obj.is_on_target else '#ff5959'
        icon = '✓' if obj.is_on_target else '✗'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {:.1f}%</span>',
            color,
            icon,
            percentage
        )

    performance_indicator.short_description = 'Performance'

    def performance_percentage_display(self, obj):
        """
        Display detailed performance metrics in readonly field.

        Args:
            obj: KPI instance

        Returns:
            str: Formatted performance metrics
        """
        return format_html(
            '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">'
            '<strong>Performance:</strong> {:.1f}%<br>'
            '<strong>Variance:</strong> ${:,.2f}<br>'
            '<strong>Status:</strong> {}'
            '</div>',
            obj.performance_percentage,
            obj.variance,
            'On Target ✓' if obj.is_on_target else 'Under Target ✗'
        )

    performance_percentage_display.short_description = 'Performance Metrics'

    # Custom actions
    actions = ['mark_on_target']

    def mark_on_target(self, request, queryset):
        """
        Custom admin action to filter for on-target KPIs.

        Args:
            request: HTTP request
            queryset: Selected KPI records
        """
        on_target = [kpi for kpi in queryset if kpi.is_on_target]
        self.message_user(
            request,
            f'{len(on_target)} of {queryset.count()} selected KPIs are on target.'
        )

    mark_on_target.short_description = 'Check which are on target'


# ============================================================================
# DEVICE AND PLAYLIST MANAGEMENT ADMIN
# ============================================================================

class PlaylistItemInline(admin.TabularInline):
    """
    Inline admin for managing playlist items within a playlist.

    Allows editing screen order and duration directly from the playlist admin.
    """
    model = PlaylistItem
    extra = 1
    fields = ['screen', 'order', 'duration_seconds']
    ordering = ['order']
    autocomplete_fields = ['screen']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """
    Admin configuration for Playlist model.

    Allows creating playlists and managing their screen items inline.
    """

    list_display = [
        'name',
        'slug',
        'item_count',
        'is_active_indicator',
        'updated_at',
    ]

    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'name',
        'slug',
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    readonly_fields = ['id', 'created_at', 'updated_at']

    inlines = [PlaylistItemInline]

    fieldsets = (
        ('Playlist Information', {
            'fields': ('name', 'slug', 'is_active')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def item_count(self, obj):
        """
        Display the number of items in this playlist.

        Args:
            obj: Playlist instance

        Returns:
            int: Number of playlist items
        """
        count = obj.items.count()
        return format_html(
            '<span style="color: #9B59FF; font-weight: bold;">{} screen{}</span>',
            count,
            's' if count != 1 else ''
        )

    item_count.short_description = 'Items'

    def is_active_indicator(self, obj):
        """
        Display active status with visual indicator.

        Args:
            obj: Playlist instance

        Returns:
            str: HTML formatted status indicator
        """
        if obj.is_active:
            return format_html(
                '<span style="color: #00F0FF; font-weight: bold;">✓ Active</span>'
            )
        else:
            return format_html(
                '<span style="color: #888; font-weight: bold;">✗ Inactive</span>'
            )

    is_active_indicator.short_description = 'Status'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Device model.

    Provides management of Fire TV devices, registration codes,
    and content assignments.
    """

    list_display = [
        'device_name_display',
        'registration_status',
        'assigned_content',
        'location',
        'last_seen_display',
    ]

    list_filter = [
        'registered',
        'created_at',
        'last_seen',
    ]

    search_fields = [
        'name',
        'id',
        'registration_code',
        'location',
    ]

    readonly_fields = ['id', 'registration_code', 'created_at', 'updated_at', 'last_seen']

    autocomplete_fields = ['assigned_playlist', 'assigned_screen']

    fieldsets = (
        ('Device Information', {
            'fields': ('name', 'location', 'notes')
        }),
        ('Registration', {
            'fields': ('id', 'registration_code', 'registered'),
            'description': 'Registration code is auto-generated. Mark as registered after device setup.'
        }),
        ('Content Assignment', {
            'fields': ('assigned_playlist', 'assigned_screen'),
            'description': 'Assign either a playlist (preferred) or a single screen. Playlist takes precedence.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'last_seen'),
            'classes': ('collapse',)
        }),
    )

    def device_name_display(self, obj):
        """
        Display device name or ID with visual styling.

        Args:
            obj: Device instance

        Returns:
            str: HTML formatted device identifier
        """
        if obj.name:
            return format_html(
                '<strong style="color: #9B59FF;">{}</strong><br>'
                '<span style="color: #888; font-size: 0.9em;">{}</span>',
                obj.name,
                str(obj.id)[:8]
            )
        else:
            return format_html(
                '<span style="color: #888;">Unnamed Device</span><br>'
                '<span style="color: #888; font-size: 0.9em;">{}</span>',
                str(obj.id)[:8]
            )

    device_name_display.short_description = 'Device'

    def registration_status(self, obj):
        """
        Display registration status with code and visual indicator.

        Args:
            obj: Device instance

        Returns:
            str: HTML formatted registration status
        """
        if obj.registered:
            return format_html(
                '<span style="color: #00F0FF; font-weight: bold;">✓ Registered</span>'
            )
        elif obj.registration_code:
            return format_html(
                '<span style="color: #ff9800; font-weight: bold;">⏳ Pending</span><br>'
                '<span style="background: #333; padding: 2px 6px; border-radius: 3px; '
                'font-family: monospace; color: #fff;">{}</span>',
                obj.registration_code
            )
        else:
            return format_html(
                '<span style="color: #888;">No Code</span>'
            )

    registration_status.short_description = 'Registration'

    def assigned_content(self, obj):
        """
        Display assigned playlist or screen.

        Args:
            obj: Device instance

        Returns:
            str: HTML formatted content assignment
        """
        if obj.assigned_playlist:
            return format_html(
                '<span style="color: #9B59FF; font-weight: bold;">📋 Playlist:</span> {}',
                obj.assigned_playlist.name
            )
        elif obj.assigned_screen:
            return format_html(
                '<span style="color: #00F0FF; font-weight: bold;">🖥 Screen:</span> {}',
                obj.assigned_screen.name
            )
        else:
            return format_html(
                '<span style="color: #888;">None Assigned</span>'
            )

    assigned_content.short_description = 'Assigned Content'

    def last_seen_display(self, obj):
        """
        Display last seen timestamp with relative time.

        Args:
            obj: Device instance

        Returns:
            str: HTML formatted last seen time
        """
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        diff = now - obj.last_seen

        if diff < timedelta(minutes=5):
            color = '#00F0FF'
            status = 'Online'
        elif diff < timedelta(hours=1):
            color = '#ff9800'
            status = f'{int(diff.total_seconds() / 60)}m ago'
        else:
            color = '#888'
            status = 'Offline'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )

    last_seen_display.short_description = 'Status'
