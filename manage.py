#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


def main():
    """Run administrative tasks."""
    # Default to local settings for development
    # Override with DJANGO_SETTINGS_MODULE environment variable if needed
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_grid.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
