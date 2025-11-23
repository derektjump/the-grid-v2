# The Grid -- Frontend Style Guide

A unified visual system for all UI in **The Grid**.\
Inspired by Lambda.ai's Superintelligence Cloud and subtle Tron grid
aesthetics:\
clean, minimal, dark, futuristic, professional.

------------------------------------------------------------------------

## 1. Core Aesthetic

-   Modern, minimal, high-end tech design.
-   Near-black backgrounds for deep contrast.
-   White/light text for maximum readability.
-   Vibrant accent colors used sparingly for emphasis.
-   Subtle Tron-grid influence:
    -   Thin low-opacity geometric lines or grid patterns.
    -   Cyan/blue highlights where appropriate.
-   Glassmorphism surfaces floating over dark backgrounds.
-   Calm, smooth interactions (no heavy neon or jittery animations).

------------------------------------------------------------------------

## 2. Color System

### CSS Variables

``` css
:root {
  --color-bg: #111216;
  --color-bg-alt: #131313;
  --color-text: #FFFFFF;
  --color-text-muted: rgba(255,255,255,0.65);

  --color-accent-primary: #9B59FF;      
  --color-accent-secondary: #00F0FF;    
  --color-accent-blue: #407BFF;         

  --color-panel-bg: rgba(255,255,255,0.08);
  --color-input-bg: rgba(255,255,255,0.10);

  --color-border: rgba(255,255,255,0.12);
}
```

### Usage Rules

-   Backgrounds → `--color-bg`, `--color-bg-alt`
-   Primary text → `--color-text`
-   Muted text → `--color-text-muted`
-   Panels/cards use:
    -   `--color-panel-bg`
    -   gradients
    -   backdrop blur
-   Accents:
    -   **Purple** for primary CTAs & highlights
    -   **Cyan** for focus states & subtle grid effects

------------------------------------------------------------------------

## 3. Typography

### Font Families

-   Primary: `"Inter", "Sora", "SF Pro Display", sans-serif`
-   Mono: `"Roboto Mono", "SF Mono", monospace`

### Weights

-   Headings: **700--800**
-   Subheadings: **500--600**
-   Body text: **400--500**
-   Code elements: **mono regular**

### Sizing

-   Hero headline: **3rem--4rem**
-   Subheadline: **1.5rem--2rem**
-   Section titles: **1.75rem--2.25rem**
-   Body: **1rem--1.125rem**
-   Caption: **0.85rem--0.95rem**
-   CTA buttons: **1rem--1.25rem**

### Line Height

-   Body text: `1.4–1.5`
-   Headings: `1.1–1.2`

### Rules

-   Large text left-aligned unless it's a hero section.
-   Avoid stacking more than two font sizes in a single UI section.
-   Maintain generous spacing around all headings.

------------------------------------------------------------------------

## 4. Layout & Spacing

### Spacing Scale

-   Small: 0.5rem\
-   Base: 1rem\
-   Medium: 1.5rem\
-   Large: 2--3rem\
-   Section padding: 3--5rem

### Container Width

-   Max-width: **1100--1200px**

### Subtle Grid Background

Optional faint grid pattern: - Lines: `rgba(255,255,255,0.02–0.04)` -
Spacing: **40--80px** - Should remain unobtrusive.

------------------------------------------------------------------------

## 5. Cards & Panels (Glassmorphism)

### Base Card Style

``` css
.card-glass {
  background: linear-gradient(
    120deg,
    rgba(255,255,255,0.08) 0%,
    rgba(255,255,255,0.02) 100%
  );
  border-radius: 22px;
  border: 1.5px solid rgba(255,255,255,0.12);

  backdrop-filter: blur(18px) saturate(1.35);
  -webkit-backdrop-filter: blur(18px) saturate(1.35);

  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  padding: 1.5rem;
}
```

### Hover State

``` css
.card-glass:hover {
  transform: translateY(-2px);
  border-color: rgba(155,89,255,0.45);
  box-shadow: 0 12px 42px rgba(0,0,0,0.35);
  transition: 0.18s ease-out;
}
```

### Guidelines

-   Cards should float visually, not feel flat.
-   Use soft shadows, not sharp edges.
-   Maintain spacing; avoid dense card content.

------------------------------------------------------------------------

## 6. Buttons & CTAs

### Primary Button (Purple CTA)

``` css
.btn-primary-grid {
  background: var(--color-accent-primary);
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  padding: 0.75em 2em;
  border-radius: 2rem;
  border: 1px solid rgba(255,255,255,0.16);
  box-shadow: 0 8px 24px rgba(155,89,255,0.35);
  transition: all 0.15s ease-out;
}

.btn-primary-grid:hover {
  background: #a56aff;
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(155,89,255,0.45);
}
```

### Secondary Button (Cyan Outline)

``` css
.btn-secondary-grid {
  background: transparent;
  color: var(--color-text);
  border-radius: 2rem;
  border: 1px solid var(--color-accent-secondary);
  padding: 0.65em 1.75em;
  transition: all 0.15s ease-out;
}

.btn-secondary-grid:hover {
  box-shadow: 0 0 16px rgba(0,240,255,0.45);
  border-color: rgba(0,240,255,0.6);
}
```

------------------------------------------------------------------------

## 7. Inputs & Forms

### Base Input Style

``` css
.form-control-grid {
  background: var(--color-input-bg);
  color: var(--color-text);
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.14);
  padding: 0.7rem 1rem;
}

.form-control-grid::placeholder {
  color: rgba(255,255,255,0.45);
}

.form-control-grid:focus {
  border-color: var(--color-accent-secondary);
  box-shadow: 0 0 0 2px rgba(0,240,255,0.5);
  outline: none;
}
```

### Labels

-   Uppercase or subtle small caps.
-   Color: `--color-text-muted`.

------------------------------------------------------------------------

## 8. Icons, Dividers, and Micro-Elements

### Icons

-   Thin-line icons.
-   White or accent colored.
-   Subtle outer glow for readability.

### Dividers

``` css
border-top: 1px solid rgba(255,255,255,0.12);
```

### Badges / Pills

-   Semi-transparent accent backgrounds:
    -   `rgba(155,89,255,0.16)` or
    -   `rgba(0,240,255,0.16)`
-   Rounded-full shapes.

------------------------------------------------------------------------

## 9. Motion & Interaction

### Guidelines

-   Animation duration: **150--250ms**
-   Easing: **ease-out**
-   Smooth, subtle transitions.

### Recommended Animations

-   Card elevation on hover
-   Button glow on hover
-   Section fade/slide-in

### Avoid

-   Bright neon flickers
-   Repetitive pulses
-   Distracting or fast animations

------------------------------------------------------------------------

## 10. Bootstrap & Layout

### Use Bootstrap 5 for:

-   Grid layout
-   Spacing utilities
-   Flexbox alignment
-   Responsive structure

### Avoid:

-   Default Bootstrap button colors
-   Bootstrap default card backgrounds
-   Overuse of utility classes over semantic HTML

### Template Structure

-   `core/templates/core/base.html`:
    -   `<header>` (minimal nav)
    -   `<main>` container
    -   `<footer>` subtle/dark
    -   Optional wrapper for background grid pattern

------------------------------------------------------------------------

## 11. File Placement

### Custom CSS

Place global UI styling here:

    core/static/core/grid.css

### Templates

-   Shared layout templates → `core/templates/core/`
-   Hub landing page → `hub/templates/hub/dashboard.html`

------------------------------------------------------------------------

## 12. Summary for AI Subagents

When generating UI for The Grid:

-   Always follow this style guide exactly.
-   Use CSS variables and component classes.
-   Maintain dark, glassmorphic, futuristic aesthetic.
-   Keep Tron influences subtle.
-   Layout must be clean, minimal, and data-focused.
-   Prefer Bootstrap grids + semantic HTML.
-   Minimize JS; use HTMX or Bootstrap where needed.

------------------------------------------------------------------------

*End of style guide.*