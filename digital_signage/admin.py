"""
Digital Signage Admin Configuration

This module configures the Django admin interface for the digital signage app,
providing easy management of screen designs, sales data, and KPI metrics.

IMPORTANT: This app is for design and data management only, NOT live playback.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ScreenDesign, Screen, SalesData, KPI


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
