# Claude Project Instructions for The Grid

This repository contains **The Grid**, a Django-based internal hub/portal that connects multiple internal tools (lifecycle management, Shopify manager, sales analytics, digital signage, agent platform). Claude Code and its subagents will assist with building and maintaining this project.

---

## 1. Project Intent

The Grid should be:

- A modular, maintainable Django project  
- Using Azure AD (Entra ID) authentication  
- Using a consistent, futuristic UI inspired by Lambda.ai + subtle Tron aesthetics  
- Easy for a single developer to maintain with AI assistance  
- Scalable to integrate multiple internal tools  

All development must respect:

- `docs/PLATFORM_OVERVIEW.md`
- `docs/STYLE_GUIDE_FRONTEND_V2.md` (primary style guide - consolidated V2)
- `docs/STYLE_GUIDE_FRONTEND.md` (original - kept for reference)

---

## 2. Subagent Routing Rules

**Use these subagents when appropriate:**

### `grid-architect`
Use for:
- Django project scaffolding
- App structure (`core`, `hub`, etc.)
- URLs and routing
- Backend logic, utilities
- Azure AD / authentication setup
- Settings design (`base.py`, `local.py`, `production.py`)
- Postgres integration
- Deployment-friendly patterns

### `grid-frontend`
Use for:
- Django templates (HTML)
- Frontend layout and component structure
- CSS, Bootstrap 5 integration
- Applying the Lambda.ai / Tron-inspired design
- Creating app tiles, landing pages, navbars
- Responsive and accessible UI

---

## 3. Development Rules

- Prefer incremental, isolated changes.
- Always show full file contents when creating new files.
- Never hardcode secrets.
- Maintain clarity, simplicity, and consistency across all apps.
- Keep frontend appearance aligned with `STYLE_GUIDE_FRONTEND_V2.md`.
- Keep backend aligned with Django best practices and `PLATFORM_OVERVIEW.md`.
- If a task involves both backend and frontend, delegate in parts to the correct agents.
- When creating new frontend components, consult `STYLE_GUIDE_FRONTEND_V2.md` for design tokens, patterns, and examples.

---

## 4. File Placement Conventions

- Global CSS → `core/static/core/grid.css`
- Global templates → `core/templates/core/base.html`
- Hub landing page → `hub/templates/hub/dashboard.html`
- Settings split across `the_grid/settings/`

---

## 5. Goal for Claude

Claude’s goal is to function as:

- **Architect** (when using subagents)
- **Code writer**
- **Safety rail for structure**
- **Consistency enforcer**
- **Documentation-aware assistant**

Claude should always consult the docs before architectural or UX-level decisions.

---

End of CLAUDE.md
