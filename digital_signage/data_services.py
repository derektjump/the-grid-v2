"""
Data Services for Digital Signage

Provides functions to fetch and cache data from external sources
for use in dynamic screen content.
"""

import logging
from decimal import Decimal
from django.core.cache import cache
from django.db import connections
from django.db.models import Sum, F, Window
from django.db.models.functions import Rank
from django.conf import settings

logger = logging.getLogger(__name__)

# Cache key prefix for sales data
CACHE_PREFIX = 'signage_data'
DEFAULT_CACHE_TIMEOUT = 300  # 5 minutes


def get_sales_data():
    """
    Fetch all sales data from the sales_board_summary table.
    Returns a comprehensive data structure for use in templates.

    Data is cached for 5 minutes (configurable).

    Returns:
        dict: Structured sales data with totals, rankings, and top performers
    """
    cache_key = f'{CACHE_PREFIX}:sales_all'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        logger.debug("Returning cached sales data")
        return cached_data

    try:
        data = _fetch_sales_data_from_db()
        cache.set(cache_key, data, DEFAULT_CACHE_TIMEOUT)
        logger.info("Sales data fetched and cached")
        return data
    except Exception as e:
        logger.error(f"Error fetching sales data: {e}")
        return _get_empty_sales_data()


def _fetch_sales_data_from_db():
    """
    Fetch sales data directly from the database.
    This is the internal implementation that queries the data_connect database.
    """
    # Check if data_connect database is configured
    if 'data_connect' not in settings.DATABASES:
        logger.warning("data_connect database not configured, returning empty data")
        return _get_empty_sales_data()

    try:
        from .models import SalesBoardSummary

        # Get all store data
        stores = list(SalesBoardSummary.objects.using('data_connect').all())

        if not stores:
            logger.warning("No sales data found in database")
            return _get_empty_sales_data()

        # Get the current_day_date from any record (should be same for all)
        current_day_date = stores[0].current_day_date if stores else None

        # Build the data structure
        data = {
            'meta': {
                'current_day_date': str(current_day_date) if current_day_date else None,
                'store_count': len(stores),
                'last_updated': str(stores[0].last_updated) if stores and stores[0].last_updated else None,
            },
            'today': _build_period_data(stores, 'today'),
            'wtd': _build_period_data(stores, 'wtd'),
            'mtd': _build_period_data(stores, 'mtd'),
        }

        return data

    except Exception as e:
        logger.error(f"Database error fetching sales data: {e}")
        return _get_empty_sales_data()


def _build_period_data(stores, period):
    """
    Build data structure for a specific time period (today, wtd, mtd).

    Args:
        stores: List of SalesBoardSummary objects
        period: 'today', 'wtd', or 'mtd'

    Returns:
        dict: Period-specific data with totals, rankings, and top performers
    """
    profit_field = f'{period}_profit'
    devices_field = f'{period}_devices_sold'
    invoiced_field = f'{period}_invoiced'
    invoice_count_field = f'{period}_invoice_count'
    device_profit_field = f'{period}_device_profit'

    # Calculate totals
    total_profit = sum((getattr(s, profit_field) or 0) for s in stores)
    total_devices = sum((getattr(s, devices_field) or 0) for s in stores)
    total_invoiced = sum((getattr(s, invoiced_field) or 0) for s in stores)
    total_invoices = sum((getattr(s, invoice_count_field) or 0) for s in stores)
    total_device_profit = sum((getattr(s, device_profit_field) or 0) for s in stores)

    # Sort by profit for rankings
    by_profit = sorted(
        stores,
        key=lambda s: getattr(s, profit_field) or 0,
        reverse=True
    )

    # Sort by devices for rankings
    by_devices = sorted(
        stores,
        key=lambda s: getattr(s, devices_field) or 0,
        reverse=True
    )

    return {
        'totals': {
            'profit': _format_currency(total_profit),
            'profit_raw': float(total_profit),
            'devices': total_devices,
            'invoiced': _format_currency(total_invoiced),
            'invoiced_raw': float(total_invoiced),
            'invoice_count': total_invoices,
            'device_profit': _format_currency(total_device_profit),
            'device_profit_raw': float(total_device_profit),
        },
        'top5_profit': [
            {
                'rank': i + 1,
                'store_name': s.store_name,
                'value': _format_currency(getattr(s, profit_field) or 0),
                'value_raw': float(getattr(s, profit_field) or 0),
            }
            for i, s in enumerate(by_profit[:5])
        ],
        'top5_devices': [
            {
                'rank': i + 1,
                'store_name': s.store_name,
                'value': getattr(s, devices_field) or 0,
            }
            for i, s in enumerate(by_devices[:5])
        ],
        'top20_profit': [
            {
                'rank': i + 1,
                'store_name': s.store_name,
                'value': _format_currency(getattr(s, profit_field) or 0),
                'value_raw': float(getattr(s, profit_field) or 0),
            }
            for i, s in enumerate(by_profit[:20])
        ],
        'top20_devices': [
            {
                'rank': i + 1,
                'store_name': s.store_name,
                'value': getattr(s, devices_field) or 0,
            }
            for i, s in enumerate(by_devices[:20])
        ],
        'all_profit': [
            {
                'rank': i + 1,
                'store_name': s.store_name,
                'value': _format_currency(getattr(s, profit_field) or 0),
                'value_raw': float(getattr(s, profit_field) or 0),
            }
            for i, s in enumerate(by_profit)
        ],
        'all_devices': [
            {
                'rank': i + 1,
                'store_name': s.store_name,
                'value': getattr(s, devices_field) or 0,
            }
            for i, s in enumerate(by_devices)
        ],
    }


def _format_currency(value):
    """Format a number as currency string."""
    if value is None:
        return "$0"
    if isinstance(value, Decimal):
        value = float(value)
    if value >= 1000:
        return f"${value:,.0f}"
    return f"${value:,.2f}"


def _get_empty_sales_data():
    """Return empty data structure when no data is available."""
    empty_period = {
        'totals': {
            'profit': '$0',
            'profit_raw': 0,
            'devices': 0,
            'invoiced': '$0',
            'invoiced_raw': 0,
            'invoice_count': 0,
            'device_profit': '$0',
            'device_profit_raw': 0,
        },
        'top5_profit': [],
        'top5_devices': [],
        'top20_profit': [],
        'top20_devices': [],
        'all_profit': [],
        'all_devices': [],
    }

    return {
        'meta': {
            'current_day_date': None,
            'store_count': 0,
            'last_updated': None,
        },
        'today': empty_period.copy(),
        'wtd': empty_period.copy(),
        'mtd': empty_period.copy(),
    }


def clear_sales_cache():
    """Clear all cached sales data."""
    cache.delete(f'{CACHE_PREFIX}:sales_all')
    logger.info("Sales data cache cleared")


def get_available_data_variables():
    """
    Get a list of all available data variables for use in screen templates.

    Returns:
        dict: Categorized list of available variables with descriptions
    """
    return {
        'sales': {
            'description': 'Sales data from sales_board_summary (refreshed every 15 minutes)',
            'variables': {
                # Meta
                'sales.meta.current_day_date': 'Date of current day data (may lag by 1 day)',
                'sales.meta.store_count': 'Total number of stores',
                'sales.meta.last_updated': 'When data was last refreshed',

                # Today totals
                'sales.today.totals.profit': 'Today total profit (formatted)',
                'sales.today.totals.devices': 'Today total devices sold',
                'sales.today.totals.invoiced': 'Today total invoiced (formatted)',

                # Today rankings
                'sales.today.top5_profit': 'Top 5 stores by profit today (array)',
                'sales.today.top5_devices': 'Top 5 stores by devices sold today (array)',
                'sales.today.all_profit': 'All stores ranked by profit today (array)',
                'sales.today.all_devices': 'All stores ranked by devices today (array)',

                # WTD totals
                'sales.wtd.totals.profit': 'Week-to-date total profit (formatted)',
                'sales.wtd.totals.devices': 'Week-to-date total devices sold',

                # WTD rankings
                'sales.wtd.top5_profit': 'Top 5 stores by profit WTD (array)',
                'sales.wtd.top5_devices': 'Top 5 stores by devices sold WTD (array)',
                'sales.wtd.all_profit': 'All stores ranked by profit WTD (array)',
                'sales.wtd.all_devices': 'All stores ranked by devices WTD (array)',

                # MTD totals
                'sales.mtd.totals.profit': 'Month-to-date total profit (formatted)',
                'sales.mtd.totals.devices': 'Month-to-date total devices sold',

                # MTD rankings
                'sales.mtd.top5_profit': 'Top 5 stores by profit MTD (array)',
                'sales.mtd.top5_devices': 'Top 5 stores by devices sold MTD (array)',
                'sales.mtd.all_profit': 'All stores ranked by profit MTD (array)',
                'sales.mtd.all_devices': 'All stores ranked by devices MTD (array)',
            }
        }
    }
