# The Grid

A unified internal hub/portal for accessing multiple internal tools and applications.

## Overview

The Grid is a Django-based platform that provides:
- Single sign-on via Azure AD (Entra ID)
- Unified navigation and UX across multiple tools
- Modular architecture for easy extension
- Lambda.ai-inspired, Tron-aesthetic design

## Project Structure

```
the-grid/
├── the_grid/              # Main Django project
│   ├── settings/          # Modular settings (base, local, production)
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── core/                  # Shared utilities, base templates, CSS
├── hub/                   # Landing page and navigation
├── docs/                  # Documentation
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip and virtualenv

### Local Development Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Hub: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Health: http://localhost:8000/health/

## Settings

The project uses modular settings:

- `the_grid/settings/base.py` - Common settings
- `the_grid/settings/local.py` - Local development (default)
- `the_grid/settings/production.py` - Production deployment

To use production settings:
```bash
export DJANGO_SETTINGS_MODULE=the_grid.settings.production
```

## Deployment

### Azure App Service

The Grid is designed to deploy to Azure App Service with:
- PostgreSQL Flexible Server for the database
- Azure AD (Entra ID) for authentication
- Azure Blob Storage for static files (optional)
- Application Insights for monitoring (optional)

See production settings for configuration details.

## Apps

### Core
Shared utilities, base templates, global CSS, and common functionality.

### Hub
Landing page and main navigation for The Grid.

### Future Apps
- Customer Lifecycle Management
- Shopify Inventory Manager
- Company Sales Analytics
- Digital Signage Management
- Agents / Assistant Platform

## Documentation

- [Platform Overview](PLATFORM_OVERVIEW.md)
- [Frontend Style Guide](STYLE_GUIDE_FRONTEND.md)
- [Claude Instructions](CLAUDE.md)

## Development Workflow

The Grid is designed for AI-assisted development using Claude Code with specialized agents:
- `grid-architect` - Backend structure and Django architecture
- `grid-frontend` - UI/UX and template development

## License

Internal use only.
