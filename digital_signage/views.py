"""
Digital Signage Views

This module provides views for the digital signage design and data management portal.

IMPORTANT: This app is NOT a signage player or live dashboard.
It is an INTERNAL DESIGN + DATA PORTAL where we:
  - Design screen content (HTML/CSS/JS)
  - Preview what screens will look like
  - Manage signage-related data
  - Copy final designs into ScreenCloud Playground

Views:
    ACTIVE DESIGN MANAGEMENT VIEWS:
    - ScreenDesignListView: List all screen designs
    - ScreenDesignUpdateView: Create/edit screen designs
    - ScreenDesignPreviewView: Preview a screen design

    DEPRECATED DASHBOARD VIEWS (kept for backward compatibility):
    - ScreenPlayView: Legacy full-screen player (DEPRECATED)
    - SalesDataListView: Display sales data (DEPRECATED - no longer primary feature)
    - KPIListView: Display KPI metrics (DEPRECATED - no longer primary feature)
    - DisplayDashboardView: Combined dashboard (DEPRECATED - no longer primary feature)
"""

from django.views.generic import ListView, UpdateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg, Q, F
from django.utils import timezone
from django.urls import reverse_lazy
from django.conf import settings
from datetime import timedelta
from .models import ScreenDesign, Screen, SalesData, KPI


# ============================================================================
# API ENDPOINTS FOR SCREENCLOUD / EXTERNAL INTEGRATIONS
# ============================================================================

@csrf_exempt  # CSRF exemption required for external API calls
@require_http_methods(["GET"])  # Only allow GET requests
def test_profit_data(request):
    """
    API endpoint for ScreenCloud to fetch test profit data by location.

    This endpoint returns static test data to verify ScreenCloud connectivity.
    In the future, this will be replaced with live data from the database.

    Authentication:
        Requires API key via header (X-API-KEY) or query parameter (api_key)

    Returns:
        JSON: {
            "items": [
                {"store": "Store Name", "profit": 123456, "devices": 42},
                ...
            ]
        }

    HTTP Status Codes:
        200: Success - returns test data
        403: Forbidden - invalid or missing API key

    Example Usage:
        fetch("https://app.azurewebsites.net/signage/api/test-profit-by-location/", {
            headers: { "X-API-KEY": "your-api-key-here" }
        })

    CORS Note:
        CORS headers will need to be configured once ScreenCloud's exact origin is known.
        For now, this endpoint is accessible but requires API key authentication.
    """
    # Extract API key from header or query parameter
    api_key = request.headers.get('X-API-KEY') or request.GET.get('api_key')

    # Validate API key against environment variable
    expected_key = getattr(settings, 'SIGNAGE_API_KEY', '')

    if not expected_key:
        # API key not configured in environment
        return HttpResponseForbidden("API authentication is not configured on the server.")

    if not api_key or api_key != expected_key:
        # API key missing or incorrect
        return HttpResponseForbidden("Invalid or missing API key.")

    # Static test data for ScreenCloud connectivity testing
    # TODO: Replace with live database queries once connectivity is verified
    test_data = {
        "items": [
            {"store": "Regina Downtown", "profit": 123456, "devices": 42},
            {"store": "Regina East", "profit": 98765, "devices": 35},
            {"store": "Moose Jaw", "profit": 45678, "devices": 18},
        ]
    }

    return JsonResponse(test_data)


# ============================================================================
# ACTIVE DESIGN MANAGEMENT VIEWS
# ============================================================================

class ScreenDesignListView(LoginRequiredMixin, ListView):
    """
    List view for all screen designs.

    Displays all screen design templates with their metadata,
    allowing users to browse, edit, and preview designs.

    Access: Staff/authenticated users only
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_list.html'
    context_object_name = 'designs'
    paginate_by = 20

    def get_queryset(self):
        """
        Get queryset with optional filtering.

        Returns:
            QuerySet: Filtered screen designs
        """
        queryset = super().get_queryset()

        # Filter by active status if requested
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        # Search by name or slug
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(slug__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['total_designs'] = ScreenDesign.objects.count()
        context['active_designs'] = ScreenDesign.objects.filter(is_active=True).count()
        return context


class ScreenDesignUpdateView(LoginRequiredMixin, UpdateView):
    """
    Create/Edit view for screen designs.

    Allows users to create new screen designs or edit existing ones.
    Provides large text areas for HTML/CSS/JS code editing.

    Access: Staff/authenticated users only
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_form.html'
    fields = ['name', 'slug', 'description', 'html_code', 'css_code', 'js_code', 'notes', 'is_active']
    success_url = reverse_lazy('digital_signage:screen_design_list')

    def get_object(self, queryset=None):
        """
        Get the object to edit, or None for create mode.

        Returns:
            ScreenDesign or None: The design to edit, or None for new
        """
        slug = self.kwargs.get('slug')
        if slug:
            return get_object_or_404(ScreenDesign, slug=slug)
        return None

    def get_context_data(self, **kwargs):
        """
        Add mode indicator to context.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)
        context['is_create_mode'] = self.object is None
        return context

    def get(self, request, *args, **kwargs):
        """
        Handle GET request for create or edit.

        Returns:
            HttpResponse: Rendered form
        """
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for create or edit.

        Returns:
            HttpResponse: Redirect or form with errors
        """
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ScreenDesignPreviewView(LoginRequiredMixin, DetailView):
    """
    Preview view for screen designs.

    Renders a barebones HTML shell that displays the screen design
    exactly as it would appear on a TV screen. This is for internal
    preview only - the actual playback happens in ScreenCloud.

    The view injects:
    - CSS code into a <style> block
    - HTML code into the body
    - JavaScript code into a <script> block

    Access: Staff/authenticated users only
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_preview.html'
    context_object_name = 'screen_design'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """
        Get queryset (no filtering needed for preview).

        Returns:
            QuerySet: All screen designs
        """
        return ScreenDesign.objects.all()


# ============================================================================
# DEPRECATED VIEWS (kept for backward compatibility)
# ============================================================================
# These views were created when digital_signage was a sales dashboard.
# They are DEPRECATED and should not be used for new features.
# They will be removed or repurposed in a future version.
# ============================================================================

class ScreenPlayView(TemplateView):
    """
    DEPRECATED: Legacy full-screen player view for ScreenCloud integration.

    This view was designed for anonymous playback of screen content.
    It is no longer the primary feature of this app.

    Use ScreenDesign and ScreenDesignPreviewView instead.
    """

    def get_template_names(self):
        """
        Dynamically select template based on screen layout type.

        Returns:
            list: Template names to try
        """
        screen = self.get_screen()
        layout_type = screen.layout_type

        # Map layout types to templates
        template_map = {
            'test': 'digital_signage/screen_test_play.html',
        }

        return [template_map.get(layout_type, 'digital_signage/screen_test_play.html')]

    def get_screen(self):
        """
        Get the Screen object from the URL slug.

        Returns:
            Screen: The screen instance

        Raises:
            Http404: If screen not found or not active
        """
        slug = self.kwargs.get('slug')
        screen = get_object_or_404(Screen, slug=slug, is_active=True)
        return screen

    def get_context_data(self, **kwargs):
        """
        Add screen data and test data to context.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)

        screen = self.get_screen()
        context['screen'] = screen

        # Layout-specific context
        if screen.layout_type == 'test':
            # Provide placeholder test data for the test layout
            context['test_data'] = [
                {
                    'store_name': 'Downtown Store',
                    'profit': 123456.78,
                    'device_sales': 42,
                },
                {
                    'store_name': 'West End Location',
                    'profit': 89012.34,
                    'device_sales': 28,
                },
                {
                    'store_name': 'North Branch',
                    'profit': 156789.01,
                    'device_sales': 55,
                },
            ]

        return context


class SalesDataListView(LoginRequiredMixin, ListView):
    """
    DEPRECATED: List view for displaying sales data.

    This view was created when digital_signage was a sales dashboard.
    It is no longer the primary feature of this app.
    """

    model = SalesData
    template_name = 'digital_signage/sales_data_list.html'
    context_object_name = 'sales_data'
    paginate_by = 50

    def get_queryset(self):
        """
        Filter queryset based on query parameters.

        Returns:
            QuerySet: Filtered sales data
        """
        queryset = super().get_queryset()

        # Filter by store if provided
        store = self.request.GET.get('store')
        if store:
            queryset = queryset.filter(store__icontains=store)

        # Filter by date range (default: last 7 days)
        days = int(self.request.GET.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        queryset = queryset.filter(date__gte=start_date)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)

        # Add filter parameters to context
        context['selected_store'] = self.request.GET.get('store', '')
        context['selected_days'] = int(self.request.GET.get('days', 7))

        # Add summary statistics
        queryset = self.get_queryset()
        context['total_sales'] = queryset.aggregate(Sum('total_sales'))['total_sales__sum'] or 0
        context['average_sales'] = queryset.aggregate(Avg('total_sales'))['total_sales__avg'] or 0

        # Get unique stores for filter dropdown
        context['available_stores'] = SalesData.objects.values_list('store', flat=True).distinct().order_by('store')

        return context


class KPIListView(LoginRequiredMixin, ListView):
    """
    DEPRECATED: List view for displaying KPI metrics.

    This view was created when digital_signage was a sales dashboard.
    It is no longer the primary feature of this app.
    """

    model = KPI
    template_name = 'digital_signage/kpi_list.html'
    context_object_name = 'kpi_data'
    paginate_by = 50

    def get_queryset(self):
        """
        Filter queryset based on query parameters.

        Returns:
            QuerySet: Filtered KPI data
        """
        queryset = super().get_queryset()

        # Filter by store if provided
        store = self.request.GET.get('store')
        if store:
            queryset = queryset.filter(store__icontains=store)

        # Filter by date range (default: last 7 days)
        days = int(self.request.GET.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        queryset = queryset.filter(date__gte=start_date)

        # Filter by performance status if provided
        status = self.request.GET.get('status')
        if status == 'on_target':
            queryset = queryset.filter(actual_sales__gte=F('sales_target'))
        elif status == 'under_target':
            queryset = queryset.filter(actual_sales__lt=F('sales_target'))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)

        # Add filter parameters to context
        context['selected_store'] = self.request.GET.get('store', '')
        context['selected_days'] = int(self.request.GET.get('days', 7))
        context['selected_status'] = self.request.GET.get('status', '')

        # Add summary statistics
        queryset = self.get_queryset()
        context['total_target'] = queryset.aggregate(Sum('sales_target'))['sales_target__sum'] or 0
        context['total_actual'] = queryset.aggregate(Sum('actual_sales'))['actual_sales__sum'] or 0

        # Calculate overall performance percentage
        if context['total_target'] > 0:
            context['overall_performance'] = (context['total_actual'] / context['total_target']) * 100
        else:
            context['overall_performance'] = 0

        # Count on-target vs under-target
        context['on_target_count'] = queryset.filter(actual_sales__gte=F('sales_target')).count()
        context['under_target_count'] = queryset.filter(actual_sales__lt=F('sales_target')).count()

        # Get unique stores for filter dropdown
        context['available_stores'] = KPI.objects.values_list('store', flat=True).distinct().order_by('store')

        return context


class DisplayDashboardView(LoginRequiredMixin, TemplateView):
    """
    DEPRECATED: Combined dashboard view for digital signage displays.

    This view was created when digital_signage was a sales dashboard.
    It is no longer the primary feature of this app.
    """

    template_name = 'digital_signage/display_dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Gather all necessary data for the dashboard display.

        Returns:
            dict: Complete dashboard context
        """
        context = super().get_context_data(**kwargs)

        # Get today's date
        today = timezone.now().date()

        # Filter by store if provided in URL
        store_filter = self.request.GET.get('store')

        # Get today's sales data
        sales_queryset = SalesData.objects.filter(date=today)
        if store_filter:
            sales_queryset = sales_queryset.filter(store=store_filter)

        # Get today's KPI data
        kpi_queryset = KPI.objects.filter(date=today)
        if store_filter:
            kpi_queryset = kpi_queryset.filter(store=store_filter)

        # Add to context
        context['todays_sales'] = sales_queryset
        context['todays_kpis'] = kpi_queryset
        context['selected_store'] = store_filter

        # Calculate daily totals
        context['daily_sales_total'] = sales_queryset.aggregate(Sum('total_sales'))['total_sales__sum'] or 0
        context['daily_target_total'] = kpi_queryset.aggregate(Sum('sales_target'))['sales_target__sum'] or 0
        context['daily_actual_total'] = kpi_queryset.aggregate(Sum('actual_sales'))['actual_sales__sum'] or 0

        # Calculate daily performance
        if context['daily_target_total'] > 0:
            context['daily_performance'] = (context['daily_actual_total'] / context['daily_target_total']) * 100
        else:
            context['daily_performance'] = 0

        # Get top performers (top 5 by sales for today)
        context['top_performers'] = sales_queryset.order_by('-total_sales')[:5]

        # Auto-refresh interval (in seconds) for digital signage
        context['refresh_interval'] = 60  # Refresh every 60 seconds

        return context
