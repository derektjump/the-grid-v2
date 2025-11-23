# The Grid -- Platform Overview

## 1. Purpose & Vision

**The Grid** is a unified internal hub/portal that gives users one place
to access multiple tools and data experiences.

It is:

-   A **landing area** for all internal Django-based applications.
-   A **consistent UX shell** that keeps everything feeling unified.
-   A **foundation** for AI-assisted development and maintenance using
    Claude Code and specialized agents.

Initial applications accessed via The Grid:

-   **Customer Lifecycle Management**
-   **Shopify Inventory Manager**
-   **Company Sales Analytics**
-   **Digital Signage Management**
-   **Agents / Assistant Platform**
-   Future tools as they are built

The Grid should feel like a modern, professional, futuristic AI control
surface with a subtle Tron "grid" influence, not a noisy neon arcade.

------------------------------------------------------------------------

## 2. Guiding Principles

1.  **Single front door**\
    Users should have one URL and one login to reach all tools.

2.  **Modular monolith first**\
    Prefer a single Django project with multiple apps over many
    microservices.

3.  **Azure-native authentication**\
    Authentication is handled by Azure AD (Entra ID).

4.  **Consistent UX & styling**\
    All apps accessed through The Grid should eventually share:

    -   The same look & feel
    -   The same navigation patterns
    -   The same layout

5.  **AI-assisted development**\
    Project structured for easy contribution from Claude Code agents.

6.  **Iterative evolution**\
    Start simple, deploy early, integrate gradually.

------------------------------------------------------------------------

## 3. Users & Use Cases

### User Types

-   Internal staff (sales, ops, marketing, leadership)
-   Technical users (developer, analysts, admins)

### Common Use Cases

-   Quickly jump between lifecycle, analytics, or Shopify tools.
-   Access digital signage manager.
-   Query agent/assistant platform.
-   View cross-app summaries and insights.

------------------------------------------------------------------------

## 4. Architecture Overview

### High-Level Components

-   **The Grid (hub)**
    -   Django-based main project.
    -   Handles login, landing page, shared UI, navigation.
    -   May eventually contain lighter apps.
-   **External Apps**
    -   Lifecycle app
    -   Shopify manager
    -   Agent/assistant platform
    -   Sales analytics
    -   Digital signage

### Modular Monolith Approach

-   One Django project: `the_grid`
-   Multiple Django apps:
    -   `core` -- shared utilities, base templates, CSS, auth
    -   `hub` -- landing page, navigation
    -   Future internalized apps

------------------------------------------------------------------------

## 5. Django Project Layout (Recommended)

    the-grid/
      docs/
        PLATFORM_OVERVIEW.md
        STYLE_GUIDE_FRONTEND.md

      .claude/
        CLAUDE.md
        agents/
          grid-architect.md
          grid-frontend.md

      the_grid/
        settings/
          base.py
          local.py
          production.py
        urls.py
        asgi.py
        wsgi.py

      core/
        templates/core/
        static/core/
          grid.css

      hub/
        templates/hub/
          dashboard.html
        urls.py
        views.py

      manage.py

------------------------------------------------------------------------

## 6. Authentication & Authorization

### Authentication

-   Azure AD / Entra ID via OpenID Connect.
-   No local passwords.
-   Smooth SSO when already signed into Microsoft.

### Authorization

-   Initially simple: all users see the hub.
-   Later:
    -   Per-app permissions
    -   Role/group-based visibility
    -   Azure AD group mappings

------------------------------------------------------------------------

## 7. Frontend & Styling

The Grid's UI matches the **Lambda.ai-inspired, Tron-flavored**
aesthetic:

-   Near-black backgrounds (`#111216`)
-   White foreground text
-   Purple (`#9B59FF`) primary accent
-   Cyan (`#00F0FF`) secondary accent
-   Glassmorphism cards
-   Bootstrap 5 layouts
-   Minimal JavaScript; HTMX when needed

Full rules in:\
**docs/STYLE_GUIDE_FRONTEND.md**

------------------------------------------------------------------------

## 8. Integration With Existing Apps

The hub will display tiles linking to:

-   Lifecycle
-   Shopify Manager
-   Sales Analytics
-   Digital Signage
-   Agent Platform

Integration Types: - External links with SSO - Optional embedding
(iframes, partial integration) - Future API-based cross-app data
surfaces

------------------------------------------------------------------------

## 9. Deployment & Infrastructure

### Hosting

-   Azure App Service for Linux
-   Azure PostgreSQL Flexible Server

### Environments

-   Local
-   QA/Dev
-   Production

### Health & Stability

-   `/health/` endpoint
-   Logging to Azure Monitor or App Insights
-   Automated Postgres backups

------------------------------------------------------------------------

## 10. AI & Development Workflow

### Dev Agents

Examples: - `grid-architect` (backend structure) - `grid-frontend`
(UI/styling)

Agents read: - `PLATFORM_OVERVIEW.md` - `STYLE_GUIDE_FRONTEND.md`

### Coding Conventions

-   Incremental commits
-   Predictable project layout
-   Clear file boundaries
-   Update docs when architecture changes

------------------------------------------------------------------------

## 11. Roadmap

### Phase 1 -- Core Framework

-   Initial Django project
-   `core` & `hub` apps
-   Minimal landing page
-   Healthcheck

### Phase 2 -- Azure AD Integration

-   Implement login & redirect flows
-   User profile display

### Phase 3 -- UI Styling

-   Glass UI
-   Tiles
-   Shared layout

### Phase 4 -- Cross-App Insights

-   Show simple lifecycle / analytics / inventory metrics

### Phase 5 -- Consolidation

-   Move small apps into The Grid
-   Standardize UI across all tools

------------------------------------------------------------------------

*End of overview.*