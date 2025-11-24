# The Grid — Frontend Style Guide V2

**Comprehensive Visual Design System**

This V2 style guide consolidates all UI rules, design patterns, and implementation standards for The Grid platform. It merges the original style guide with all design decisions made during development, reflecting the actual implemented system.

Inspired by Lambda.ai's Superintelligence Cloud platform and subtle Tron grid aesthetics: clean, minimal, dark, futuristic, and professional.

---

## 1. Core Aesthetic & Design Principles

### Visual Philosophy
- **Modern Minimal Tech Design**: High-end, data-focused interface with clean geometry
- **Dark Foundation**: Near-black backgrounds (#0b0b0b, #050506) for deep contrast and visual hierarchy
- **Professional & Calm**: Avoid garish neon; maintain sophisticated, subtle aesthetic
- **Sharp Rectangular Geometry**: NO rounded corners (border-radius: 0) except where explicitly defined for specific elements
- **Glassmorphism**: Subtle transparency and layering (used sparingly, not everywhere)
- **Tron-Inspired Grid**: Faint geometric background patterns with chromatic hover effects

### Design Fundamentals
- White/light text for maximum readability on dark backgrounds
- Vibrant accent colors (purple, cyan, pink) used sparingly for emphasis
- Flat surfaces with sharp edges (Lambda.ai style) rather than heavy glassmorphism
- Smooth, subtle interactions (150-250ms transitions)
- Data-first layout: generous whitespace, clear visual hierarchy

---

## 2. Color System

### CSS Variables

```css
:root {
  /* Background colors - SOLID DARK */
  --color-bg: #0b0b0b;              /* Primary background */
  --color-bg-alt: #0b0b0b;          /* Alternative background */

  /* Text colors */
  --color-text: #FFFFFF;
  --color-text-muted: rgba(255, 255, 255, 0.65);
  --color-text-dark: #111216;       /* For text on light backgrounds */

  /* Accent colors - Purple primary, Cyan minimal */
  --color-accent-primary: #6434f8;  /* Primary purple for CTAs/highlights */
  --color-accent-secondary: #00f0ff; /* Cyan - subtle accents only */
  --color-accent-blue: #407BFF;     /* Blue accent */
  --color-spectrum-pink: #ff3b81;   /* Pink for spectrum/chroma effects */

  /* UI element backgrounds - SOLID */
  --color-panel-bg: #0b0b0b;
  --color-input-bg: rgba(255, 255, 255, 0.06);

  /* Borders */
  --color-border: rgba(255, 255, 255, 0.10);
  --color-border-subtle: rgba(255, 255, 255, 0.05);
  --color-border-hover: #6434f8;

  /* Spacing scale */
  --spacing-sm: 0.5rem;
  --spacing-base: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;

  /* Border radius - SHARP rectangular geometry */
  --radius-none: 0px;
  --radius-minimal: 2px;            /* Only for specific UI elements */
}
```

### Color Usage Guidelines

#### Backgrounds
- Primary background: `#0b0b0b` (near-black)
- Hero sections: `#000000` (pure black)
- Body background: `#050506` with subtle grid pattern
- Panel backgrounds: `var(--color-panel-bg)` (#0b0b0b solid, no gradients)

#### Text Colors
- Primary headings/text: `#FFFFFF` (pure white)
- Body/description text: `#e2e2f0` or `#b3b3c2` (off-white, slightly warm)
- Muted text: `rgba(255, 255, 255, 0.65)`

#### Accent Colors (Use Sparingly)
- **Purple (#6434f8)**: Primary CTAs, hover states, primary highlights
  - Lighter hover: `#7648fa`
- **Cyan (#00f0ff)**: Secondary accents, chroma effects (left side in spectrum)
- **Pink (#ff3b81)**: Spectrum effects (right side), chromostereopsis effects
- **White (#ffffff)**: Secondary CTAs, clean button backgrounds

#### Border Colors
- Standard borders: `rgba(255, 255, 255, 0.10)`
- Subtle borders (empty cells): `rgba(255, 255, 255, 0.05)`
- Hover borders: `#6434f8` (purple, 2px width)
- Section dividers: `rgba(255, 255, 255, 0.12)` (1px solid white)

---

## 3. Typography

### Font Families

```css
/* Primary UI font - Sans-serif for headings and UI elements */
font-family: "Suisse Intl", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

/* Monospace font - For descriptions, code, button labels */
font-family: "Suisse Intl Mono", "Roboto Mono", ui-monospace, "SF Mono", "Courier New", monospace;

/* Pixel font - For special glitch effects only */
font-family: "Press Start 2P", monospace;
```

### Font Weights
- **Headings**: 600-700
- **Subheadings**: 600
- **Body text**: 400-500
- **Button labels**: 500
- **Mono elements**: 400-500

### Size Hierarchy

| Element | Size | Usage |
|---------|------|-------|
| Hero title | `clamp(40px, 8vw, 115px)` | Main hero headline |
| Section title (h2) | `3.5rem` (56px) | Section headings like "Programs in the Grid" |
| Subsection title (h3) | `1.5rem` (24px) | Card titles |
| Hero description | `24px` | Subtitle text in hero |
| Body description | `1rem` (16px) | Standard app descriptions |
| Button text | `0.95rem` (15.2px) | CTA and navigation text |
| Caption/muted | `0.85rem` (13.6px) | Small labels, footer text |

### Typography Rules

#### Usage by Element Type
- **Headings (h1, h2, h3)**: Use sans-serif font, weight 600
- **Descriptions/body**: Use monospace font for technical/data aesthetic
- **Button labels**: Use monospace font, uppercase, letter-spacing: 0.05em
- **Navigation items**: Use monospace font, uppercase

#### Formatting
- **Line height**:
  - Body text: 1.4-1.6
  - Headings: 1.05-1.2
- **Letter spacing**:
  - Headings: -0.01em to -0.02em (tighter)
  - Buttons/nav: 0.05em (wider, uppercase)
- **Text transform**:
  - Buttons: `uppercase`
  - Navigation: `uppercase`
  - Labels: `uppercase`

---

## 4. Hero Section Rules

### Full-Height Hero Design

```css
.hero.hero-full {
  height: calc(100vh - 7rem);     /* Full viewport minus header */
  background-color: #000000;       /* Pure black, no canvas */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}
```

### Hero Content Structure
1. **Description first** (top): Mono font, 24px, color `#e2e2f0`
2. **Title** (center): Large sans-serif, 40-115px responsive
3. **Buttons** (bottom): Two-button layout with spectrum effects

### Hero Typography
- **Description**:
  - Font: Mono
  - Size: `24px`
  - Color: `#e2e2f0`
  - Margin: `0 0 1.5rem`

- **Title**:
  - Font: Sans-serif
  - Size: `clamp(40px, 8vw, 115px)`
  - Weight: 700
  - Line-height: 1.05
  - Letter-spacing: -0.02em
  - Margin: `0 0 2rem`

### "Digitally" Glitch Effect
- The word "Digitally" in hero title uses glitch animation (if implemented)
- Pixel font applied to glitched text
- Subtle chromatic aberration effect

### Hero Background
- **Pure black** (`#000000`)
- **NO canvas background** in hero area
- Interactive grid canvas starts BELOW hero section
- Sharp transition at section divider

### Hero Buttons
See Button System section below for detailed button styles.

---

## 5. Navigation System

### Header Specifications

```css
.grid-header {
  height: 7rem;                    /* Fixed header height */
  background: transparent;
  border-bottom: none;
  position: sticky;
  top: 0;
  z-index: 1000;
}
```

### Header Layout Structure
The header uses a three-section layout:

1. **Logo area** (left): 200px width, transparent background
2. **Navigation panel** (center): Black background with borders, flex: 1
3. **Auth section** (right): 200px width, transparent background

### Logo Rules
```css
.grid-logo {
  width: 200px;
  height: 100%;               /* Full 7rem height */
  margin-right: 1.5rem;
}

.grid-logo-img {
  height: 100%;
  width: auto;
}
```

- Logo uses full header height (7rem)
- Transparent background around logo
- Hover: opacity 0.8

### Navigation Panel (Center Section)

```css
.grid-nav-wrapper {
  flex: 1;
  background: rgba(0, 0, 0, 0.85);
  align-self: stretch;
  border-left: 1px solid var(--color-border);
  border-right: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}
```

- **Black centerpiece** with 85% opacity
- Bordered on left, right, and bottom
- Contains centered navigation items
- Full height (stretches to 7rem)

### Navigation Items

```css
.grid-nav-item {
  color: var(--color-text-muted);
  font-family: "Suisse Intl Mono", monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 2px;
}

.grid-nav-item:hover {
  color: #000000;               /* Black text */
  background: #ffffff;          /* White background */
}
```

- Mono font, uppercase, muted color by default
- Gap between items: 2.5rem
- Hover: **white background, black text**

### Dropdown Menus

```css
.dropbtn {
  /* Same styling as .grid-nav-item */
}

.dropbtn:hover {
  color: #000000;
  background: #ffffff;
}

.dropdown-content {
  background-color: rgba(0, 0, 0, 0.85);
  min-width: 250px;
  border: 1px solid var(--color-border);
  border-top: none;
  padding-bottom: 12px;
}

.dropdown-content a {
  color: white;
  padding: 12px 16px;
  font-family: 'Suisse Intl Mono', monospace;
  border-left: 5px solid transparent;
}

.dropdown-content a:hover {
  background-color: white;
  color: black;
  border-left: 5px solid black;
}

.dropdown-content a::before {
  content: "▶";
  color: transparent;
  margin-right: 10px;
}

.dropdown-content a:hover::before {
  color: black;              /* Black arrow indicator on hover */
}
```

- Dropdown appears on hover with "invisible bridge" to prevent flickering
- Items show **black arrow (▶)** on left when hovered
- Hover: white background, black text, black left border

### Authentication Section (Right)

```css
.grid-auth-section {
  width: 200px;
  padding-left: 1.5rem;
}
```

- Contains sign-in button or user info
- Aligned left within its 200px container
- See Button System for auth button styles

---

## 6. Button System

All buttons use **rectangular geometry** (border-radius: 0) and monospace font.

### Primary Button (Purple CTA)

```css
.btn-primary-grid {
  background: var(--color-accent-primary);  /* #6434f8 */
  color: #ffffff;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.7rem 1.75rem;
  border-radius: var(--radius-none);        /* Sharp corners */
  border: none;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: "Suisse Intl Mono", monospace;
}

.btn-primary-grid:hover {
  background: #7648fa;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(100, 52, 248, 0.4);
}
```

**Usage**: Main call-to-action only (used sparingly)

### Secondary Button (White Background)

```css
.btn-secondary-grid {
  background: #ffffff;                      /* Solid white */
  color: var(--color-text-dark);           /* Black text */
  border-radius: var(--radius-none);
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0.7rem 1.75rem;
  font-weight: 500;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: "Suisse Intl Mono", monospace;
}

.btn-secondary-grid:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(0, 0, 0, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

**Usage**: Default button style, secondary actions

### Spectrum 3D Effect Button

```css
.btn-spectrum {
  background: #ffffff;
  color: var(--color-text-dark);
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.7rem 1.75rem;
  border-radius: var(--radius-none);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: "Suisse Intl Mono", monospace;
}

/* 3D colored plate behind - shows on LEFT, TOP, RIGHT (not bottom) */
.btn-spectrum::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: 0;                                /* No offset on bottom */
  background: linear-gradient(90deg,
    var(--color-spectrum-pink) 0%,          /* Pink left */
    var(--color-accent-primary) 33%,        /* Purple top */
    var(--color-accent-primary) 66%,        /* Purple middle */
    var(--color-accent-secondary) 100%      /* Cyan right */
  );
  z-index: -1;
}

.btn-spectrum:hover::before {
  top: -4px;
  left: -4px;
  right: -4px;
}
```

**Usage**: Hero section buttons, special CTAs with chromatic edge effect

### Hero Buttons (Specific Implementation)

```css
.btn-white {
  background: #ffffff;
  color: #111216;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow:
    -2px 0 0 0 #ff3b81,      /* Pink left edge */
    0 -2px 0 0 #6434f8,      /* Purple top edge */
    2px 0 0 0 #00f0ff;       /* Cyan right edge */
}

.btn-purple {
  background: #6434f8;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.12);
}
```

### Authentication Button

```css
.btn-sign-in {
  background: #ffffff;
  color: #111216;
  font-size: 0.85rem;
  font-weight: 500;
  font-family: "Suisse Intl Mono", monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: var(--radius-minimal);     /* 2px radius for auth only */
  padding: 0.6rem 1.2rem;
}

.btn-sign-in:hover {
  border-color: var(--color-accent-primary);
  box-shadow: 0 2px 8px rgba(100, 52, 248, 0.2);
}
```

### Button Row Container

```css
.button-row {
  display: inline-flex;
  gap: 0;                   /* Buttons touch edges, no gap */
}
```

---

## 7. Grid Background System (Interactive Canvas)

### Two-Layer Background Strategy

1. **Static body background** (everywhere):
   ```css
   body {
     background: #050506;
     background-image:
       linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px),
       linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px);
     background-size: 60px 60px;
   }
   ```

2. **Interactive canvas background** (apps section only):
   ```html
   <div class="apps-grid-background">
     <canvas class="apps-grid-canvas"></canvas>
   </div>
   ```

### 3D Horizon Grid (Body Background)

```css
body::before {
  position: fixed;
  background-color: #0b0b0b;
  background-image:
    /* Horizontal lines - denser toward bottom for perspective */
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 39px,
      rgba(100, 52, 248, 0.08) 39px,      /* Purple grid lines */
      rgba(100, 52, 248, 0.08) 40px
    ),
    /* Vertical lines - standard spacing */
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 59px,
      rgba(100, 52, 248, 0.06) 59px,
      rgba(100, 52, 248, 0.06) 60px
    ),
    /* Gradient fade to create horizon effect */
    linear-gradient(
      180deg,
      rgba(11, 11, 11, 1) 0%,
      rgba(11, 11, 11, 0.7) 40%,
      rgba(11, 11, 11, 0.85) 70%,
      rgba(11, 11, 11, 0.95) 100%
    );
  transform-origin: center bottom;
  transform: perspective(800px) rotateX(2deg) scale(1.1);
  opacity: 0.6;
}
```

### Interactive Mouse Hover Canvas

**Placement**:
- Entire page EXCEPT hero section
- Fixed position, z-index: 0
- Canvas responds to mousemove events

**Grid Specifications**:
- Cell size: `60px` (horizontal and vertical)
- Base line alpha: `0.015` (extremely subtle)
- Line color: White `rgba(255,255,255,alpha)`

**Mouse Interaction Behavior**:

1. **Vertical Lines**:
   - Radial falloff: 6 cells (360px)
   - Base alpha increase on hover: +0.04
   - Chroma colors:
     - **Left of mouse**: Pink `rgba(255,59,129,alpha)`
     - **Right of mouse**: Cyan `rgba(0,240,255,alpha)`
   - Chroma intensity: 0.20 (multiplied by distance factor)
   - Vertical fade: Radial gradient centered on mouseY, 3-cell radius (240px)

2. **Horizontal Lines**:
   - Radial falloff: 4 cells (320px)
   - Base alpha increase on hover: +0.04
   - Chroma colors:
     - **Above mouse**: Purple `rgba(100,52,248,alpha)`
     - **Below mouse**: White `rgba(255,255,255,alpha)` (50% intensity)
   - Chroma intensity: 0.20 above, 0.10 below
   - Horizontal fade: Radial gradient centered on mouseX, same radius as vertical

**Subtlety Levels**:
```javascript
var baseAlpha = 0.015;              // Base grid visibility
var chromaIntensity = 0.20;         // Chroma effect strength
var segmentRadius = cellSize * 3.0; // Fade distance (240px)
```

**Gradient Math**:
- Multi-stop gradients for smooth falloff
- Peak intensity at mouse position
- Exponential fade using distance factor: `1 - distance / maxDistance`
- Intensified within 0.5 cells of exact mouse position

### Hero Background Exception
- Hero section uses **pure black** (#000000)
- **NO canvas or interactive grid** in hero area
- Sharp visual break at section divider

---

## 8. Section Dividers

### Full-Width Section Divider

```css
.section-divider {
  border-top: 1px solid rgba(255,255,255,0.12);
  margin: 0;
}

.section-divider--full {
  width: 100vw;
  margin: 0 auto 2.5rem auto;
  transform: translateX(calc(50% - 50vw));
}
```

**Usage**:
- Between hero and apps section
- Visual separator for major content areas
- Full viewport width, breaks out of container

**Placement**:
```html
<section class="hero hero-full">...</section>
<div class="section-divider section-divider--full"></div>
<div class="apps-grid-background">...</div>
```

---

## 9. Application Cards

### Card Grid Layout

```css
.apps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;                           /* NO GAPS - borders touch */
  padding: 0;
  margin: 0;
  border: none;                     /* NO outer border */
}
```

**Pattern**: Card / Empty / Card alternating layout
- Row 1: Card, Empty, Card
- Row 2: Empty, Card, Empty
- Row 3: Card, Empty, Card
- Row 4: Empty, Card, Empty

### App Card Component

```css
.app-card {
  background: var(--color-panel-bg);        /* #0b0b0b solid */
  border: 1px solid var(--color-border);
  border-radius: var(--radius-none);        /* Sharp corners */
  padding: 2rem;
  min-height: 280px;
  display: flex;
  flex-direction: column;
}

.app-card:hover {
  border-color: var(--color-border-hover);  /* Purple */
  border-width: 2px;                        /* Thicker border */
  background: var(--color-panel-bg);
  box-shadow: 0 2px 8px rgba(100, 52, 248, 0.15);
  z-index: 10;
  margin: -1px;                             /* Compensate for thicker border */
  transform: none !important;               /* NO SCALING */
}
```

**Hover Behavior**:
- Border changes to purple, increases to 2px
- Subtle purple shadow appears
- **NO transform/scale effects** (explicitly disabled)
- Margin adjustment prevents layout shift

### Empty Cell Styling

```css
.app-cell-empty {
  background: transparent;
  border: 1px solid var(--color-border-subtle);
  min-height: 280px;
}

/* Remove outer borders from empty cells to prevent frame effect */
.apps-grid > .app-cell-empty:nth-child(3n+1) {
  border-left: none;        /* Left column */
}

.apps-grid > .app-cell-empty:nth-child(3n) {
  border-right: none;       /* Right column */
}

.apps-grid > .app-cell-empty:nth-child(-n+3) {
  border-top: none;         /* Top row */
}

.apps-grid > .app-cell-empty:nth-child(n+10) {
  border-bottom: none;      /* Bottom row (items 10-12) */
}
```

**Purpose**: Creates checkerboard pattern without visible outer grid frame

### Card Content Structure

```html
<article class="card-glass app-card">
  <div class="app-card-icon">
    <svg class="app-icon">...</svg>
  </div>
  <h3 class="app-card-title">Card Title</h3>
  <p>Description text in mono font...</p>
  <a href="#" class="app-card-link">Open</a>
</article>
```

**Spacing**:
- Icon wrapper: `margin-bottom: 0.75rem`
- Title: `margin-bottom: 0.75rem`
- Description: `flex: 1` (pushes CTA to bottom)
- CTA link: `margin-top: var(--spacing-md)`

### Card Typography

```css
.app-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  font-family: "Suisse Intl", sans-serif;
}

.app-card p {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
  font-family: "Suisse Intl Mono", monospace;
}
```

### Card CTA Link

```css
.app-card-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #ffffff;
  color: #111216;
  font-size: 0.85rem;
  font-family: "Suisse Intl Mono", monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(0, 0, 0, 0.4);
  border-radius: 0;
  padding: 0.5rem 0.85rem;
  box-shadow:
    -2px 0 0 0 #ff3b81,      /* Pink left edge */
    0 -2px 0 0 #6434f8,      /* Purple top edge */
    2px 0 0 0 #00f0ff;       /* Cyan right edge */
}

/* Black triangle arrow on the LEFT */
.app-card-link::before {
  content: '';
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 4px 0 4px 6px;
  border-color: transparent transparent transparent #111216;
}

.app-card-link:hover {
  border-color: rgba(0, 0, 0, 0.5);
  box-shadow: none;                /* Chroma edges removed on hover */
}
```

---

## 10. Cryptic Icon System (SVG)

### Icon Specifications

**Size**: 60px × 60px
**Viewbox**: `0 0 24 24`
**Placement**: Above card title, left-aligned

### Stroke Classes

```css
/* Base strokes */
.app-icon .stroke-main {
  stroke: #ffffff;
  stroke-width: 0.6;
  fill: none;
}

.app-icon .stroke-secondary {
  stroke: #555555;
  stroke-width: 0.3;
  fill: none;
}

/* Chroma overlay (always on, stronger on hover) */
.app-icon .stroke-chroma {
  stroke-width: 0.6;
  fill: none;
  opacity: 0.25;                    /* Subtle at rest */
}

.app-card:hover .app-icon .stroke-chroma {
  opacity: 0.8;                     /* Stronger on hover */
}
```

### Chroma Gradient Definition

```html
<defs>
  <linearGradient id="chroma-[iconname]" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#ff3b81"/>    <!-- Pink left -->
    <stop offset="50%" stop-color="#6434f8"/>   <!-- Purple center -->
    <stop offset="100%" stop-color="#00f0ff"/>  <!-- Cyan right -->
  </linearGradient>
</defs>
```

**Usage**: Apply to `.stroke-chroma` elements:
```html
<polyline class="stroke-chroma" stroke="url(#chroma-[iconname])"/>
```

### Icon Design Principles

1. **Geometric abstraction**: Simple shapes representing app concept
2. **White main lines**: Primary structure in white (#ffffff)
3. **Grey secondary lines**: Supporting detail in grey (#555555)
4. **Chroma highlights**: Spectrum gradient on key elements
5. **Always-on chromostereopsis**: Subtle at rest, intensified on hover
6. **Grid-based composition**: Align to 24×24 grid for consistency

### Example Icon Patterns

**Lifecycle Icon** (circular cycle):
- Four corner squares connected by loop
- Grey dashed connector
- Chroma overlay on connection loop

**Inventory Icon** (stacked boxes):
- Three overlapping rectangles
- Chroma highlight on front box

**Analytics Icon** (dashboard chart):
- Outer frame with sidebar
- Grid lines in chart area
- Polyline chart with chroma overlay
- Chroma offset on outer frame

**Signage Icon** (display screen):
- Outer display frame
- Inner chroma content area

**Agents Icon** (network circuit):
- Central square hub
- Four corner nodes
- Chroma circuit connections (puzzle-piece style)

**Coming Soon Icon** (glitch placeholder):
- Outer faint frame
- Broken inner square (discontinuous lines)
- Small filled node in center
- Chroma frame overlay

---

## 11. Applications Section Layout

### Section Container

```css
.apps-section {
  position: relative;
  margin-bottom: var(--spacing-xl);
  z-index: 1;
  /* Break out of main-container padding to go full-width */
  margin-left: calc(-1 * var(--spacing-base));
  margin-right: calc(-1 * var(--spacing-base));
  padding-left: var(--spacing-base);
  padding-right: var(--spacing-base);
}
```

**Purpose**: Allows apps grid to stretch edge-to-edge while maintaining proper padding

### Section Header

```css
.apps-header {
  margin-bottom: 10rem;             /* Large space before grid */
}

.apps-title {
  font-size: 3.5rem;
  font-weight: 600;
  margin: 0;
}
```

### Subtitle with Elbow Line

```html
<div class="apps-subtitle">
  <div class="apps-subtitle-line"></div>
  <div>
    <p class="apps-description">Description text...</p>
    <a href="#" class="apps-cta">Explore</a>
  </div>
</div>
```

**Elbow line styling**:
```css
.apps-subtitle-line {
  width: 80px;
  height: 24px;
}

.apps-subtitle-line::before {
  /* Vertical line */
  content: "";
  position: absolute;
  background: #ffffff;
  width: 1px;
  height: 100%;
  left: 0;
  top: 0;
}

.apps-subtitle-line::after {
  /* Horizontal line */
  content: "";
  position: absolute;
  background: #ffffff;
  height: 1px;
  width: 80px;
  left: 0;
  bottom: 0;
}
```

**Description styling**:
```css
.apps-description {
  font-size: 1rem;
  line-height: 1.45;
  padding-top: 0.45rem;             /* Align with elbow line */
  font-family: "Suisse Intl Mono", monospace;
  color: #b3b3c2;
}
```

### Section CTA

```css
.apps-cta {
  display: inline-block;
  margin-top: 1.25rem;
  padding: 0.65rem 2rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #ffffff;
  background: #6434f8;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 0;
}

.apps-cta:hover {
  background: #5a2ee0;
  box-shadow: none;
  transform: none;
}
```

---

## 12. Layout System

### Container Widths

```css
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-base);
}
```

### Alignment Rules
- Main content: Centered, max-width 1200px
- Full-width elements: Use negative margins to break out
- Hero content: Centered within viewport
- Apps grid: Full-width within main container

### Negative Margin Breakouts

For elements that need to ignore container padding:
```css
margin-left: calc(-1 * var(--spacing-base));
margin-right: calc(-1 * var(--spacing-base));
```

### Spacing Scale
- **Small**: 0.5rem (8px)
- **Base**: 1rem (16px)
- **Medium**: 1.5rem (24px)
- **Large**: 2rem (32px)
- **Extra Large**: 3rem (48px)

---

## 13. Forms & Inputs

### Input Field Styling

```css
.form-control-grid {
  background: var(--color-input-bg);        /* rgba(255,255,255,0.06) */
  color: var(--color-text);
  border-radius: var(--radius-none);        /* Sharp corners */
  border: 1px solid var(--color-border);
  padding: 0.7rem 1rem;
  font-size: 1rem;
  width: 100%;
}

.form-control-grid::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-control-grid:focus {
  outline: none;
  border-color: var(--color-accent-secondary);     /* Cyan focus */
  box-shadow: 0 0 0 1px var(--color-accent-secondary);
}
```

### Label Styling

```css
label {
  display: block;
  color: var(--color-text-muted);
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--spacing-sm);
}
```

---

## 14. Footer

```css
.grid-footer {
  border-top: 1px solid var(--color-border);
  padding: var(--spacing-lg) 0;
  margin-top: calc(var(--spacing-xl) * 2);
  text-align: center;
}

.grid-footer p {
  color: var(--color-text-muted);
  font-size: 0.85rem;
  margin: 0;
}

/* System Health indicator uses purple text */
.grid-footer .text-muted {
  color: var(--color-accent-primary);
}
```

---

## 15. Responsive Design

### Breakpoints

- **Desktop**: 992px and above (3-column grid)
- **Tablet**: 768px - 991px (2-column grid)
- **Mobile**: Below 768px (1-column grid with gaps)

### Apps Grid Responsive Behavior

```css
@media (max-width: 992px) {
  .apps-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .apps-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-base);       /* Add gaps on mobile */
  }
}
```

### Typography Adjustments

```css
@media (max-width: 768px) {
  .apps-title {
    font-size: 1.75rem;
  }

  h1 {
    font-size: 2.5rem;
  }

  h2 {
    font-size: 1.75rem;
  }
}

@media (max-width: 480px) {
  .apps-title {
    font-size: 1.5rem;
  }
}
```

### Background Grid Mobile Adjustments

```css
@media (max-width: 768px) {
  body::before {
    transform: perspective(600px) rotateX(1deg) scale(1.05);
  }
}
```

---

## 16. Motion & Interaction

### Animation Timing
- **Duration**: 150-250ms
- **Easing**: `ease-out`
- **NO transforms on app cards** (explicitly disabled)

### Hover States
- Border color changes
- Subtle shadows
- Minimal Y-axis translation (1-2px for buttons only)
- Icon chroma intensification

### Disabled Effects
```css
.app-card:hover,
.card-glass:hover {
  transform: none !important;       /* NO scaling/rotating */
}

.app-card,
.card-glass {
  transition: border-color 0.15s ease-out, background 0.15s ease-out !important;
}
```

---

## 17. Components Library

### Cards
- **App Card**: See section 9
- **Glass Card**: Minimal use, only where glassmorphism is appropriate

### Buttons
- **Primary (Purple)**: Main CTAs
- **Secondary (White)**: Default actions
- **Spectrum**: Hero/special CTAs with chromatic edges
- **Auth**: White with minimal radius

### Icons
- **Cryptic SVG**: 60×60px, geometric, white/grey/chroma
- **Legacy CSS**: Deprecated, replaced by SVG system

### Dropdowns
- Navigation dropdown menus
- Black background, white hover state

### Section Elements
- **Dividers**: 1px white line, full-width
- **Elbow Line**: Subtitle decorator
- **Headers**: Large sans-serif titles

---

## 18. Accessibility Requirements

### Color Contrast
- Maintain WCAG AA standards (4.5:1 minimum for text)
- White on dark backgrounds ensures high contrast
- Purple accent on dark: verified contrast ratio

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Focus states on all buttons, links, inputs
- Dropdown menus accessible via keyboard

### ARIA Labels
```html
<svg aria-hidden="true">...</svg>
<article role="article">...</article>
```

### Semantic HTML
- Use proper heading hierarchy (h1 → h2 → h3)
- `<article>` for app cards
- `<nav>` for navigation
- `<main>` for main content

---

## 19. File Organization

### CSS Location
```
core/static/core/grid.css
```
Single global stylesheet containing all custom styles.

### Template Structure
```
core/templates/core/base.html          # Base layout with header/footer
hub/templates/hub/dashboard.html       # Hub landing page
```

### Static Assets
```
core/static/core/
  ├── grid.css
  └── gridv2logotransparent.png
```

---

## 20. Development Rules & Best Practices

### CSS Architecture
1. **CSS Variables First**: Use root variables for all colors, spacing
2. **Component Classes**: Clear, semantic class names (`.app-card`, `.btn-primary-grid`)
3. **No Deep Nesting**: Keep specificity low
4. **Comments**: Section headers for each major component group
5. **Organization**: Variables → Base → Components → Utilities → Responsive

### Naming Conventions
- **Components**: `.component-name` (kebab-case)
- **Modifiers**: `.component-name--modifier`
- **State classes**: `.is-active`, `.has-error`
- **Grid-specific**: Prefix with `.grid-` for global navigation/layout

### JavaScript Usage
- **Minimize JS**: Prefer CSS-only solutions
- **Vanilla JS**: No jQuery or heavy frameworks
- **Progressive Enhancement**: Core functionality works without JS
- **Canvas**: Only for interactive grid background

### Bootstrap 5 Integration
**Use Bootstrap for**:
- Grid system (`container`, `row`, `col-*`)
- Utility classes (spacing, display, flex)
- Responsive helpers

**Avoid Bootstrap**:
- Default button styles (always override)
- Default card backgrounds (use custom `.card-glass`)
- Color utilities (use custom CSS variables)

---

## 21. Quality Checklist

Before deploying any new UI component:

- [ ] Uses CSS variables for colors
- [ ] Sharp corners (border-radius: 0) except auth button
- [ ] Mono font for descriptions/button labels
- [ ] Sans-serif for headings
- [ ] Purple (#6434f8) for primary accents
- [ ] No transform/scale on app cards
- [ ] Proper color contrast (WCAG AA)
- [ ] Keyboard accessible
- [ ] Responsive at all breakpoints
- [ ] Follows spacing scale
- [ ] Semantic HTML
- [ ] Clear comments in CSS
- [ ] Tested on mobile, tablet, desktop

---

## 22. Common Patterns Reference

### Three-Column Checkerboard Grid
```html
<div class="apps-grid">
  <article class="app-card">...</article>
  <div class="app-cell-empty"></div>
  <article class="app-card">...</article>

  <div class="app-cell-empty"></div>
  <article class="app-card">...</article>
  <div class="app-cell-empty"></div>

  <!-- Repeat pattern -->
</div>
```

### Hero Section Structure
```html
<section class="hero hero-full">
  <div class="hero-overlay">
    <p class="hero-description">Subtitle</p>
    <h1 class="hero-title">Main Title</h1>
    <div class="hero-buttons">
      <a href="#" class="btn-white">Button 1</a>
      <a href="#" class="btn-purple">Button 2</a>
    </div>
  </div>
</section>
```

### Section Header with Elbow
```html
<header class="apps-header">
  <h2 class="apps-title">Section Title</h2>
  <div class="apps-subtitle">
    <div class="apps-subtitle-line"></div>
    <div>
      <p class="apps-description">Description text</p>
      <a href="#" class="apps-cta">CTA</a>
    </div>
  </div>
</header>
```

---

## 23. Design Tokens Summary

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg` | `#0b0b0b` | Primary background |
| `--color-accent-primary` | `#6434f8` | Purple CTAs/highlights |
| `--color-accent-secondary` | `#00f0ff` | Cyan accents |
| `--color-spectrum-pink` | `#ff3b81` | Pink chroma effects |
| `--color-border` | `rgba(255,255,255,0.10)` | Standard borders |

### Spacing
| Token | Value | Usage |
|-------|-------|-------|
| `--spacing-sm` | `0.5rem` | Tight spacing |
| `--spacing-base` | `1rem` | Standard spacing |
| `--spacing-md` | `1.5rem` | Medium spacing |
| `--spacing-lg` | `2rem` | Large spacing |
| `--spacing-xl` | `3rem` | Extra large spacing |

### Typography
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Hero title | Sans-serif | 40-115px | 700 |
| Section title | Sans-serif | 3.5rem | 600 |
| Card title | Sans-serif | 1.25rem | 600 |
| Description | Monospace | 1rem | 400 |
| Button | Monospace | 0.95rem | 500 |

---

## 24. Version History

**V2.0** (Current)
- Consolidated all implemented patterns from codebase
- Sharp rectangular geometry standardized
- Interactive canvas grid system documented
- Cryptic SVG icon system defined
- Navigation hover behavior finalized
- Color system updated with actual values (#6434f8 purple primary)
- Hero section black background rule
- Apps grid checkerboard pattern
- Transform effects disabled on cards
- Chroma spectrum button system

**V1.0**
- Original style guide with Lambda.ai inspiration
- Glassmorphism-heavy approach
- Rounded corners throughout
- Conceptual color system

---

## 25. Future Considerations

### Potential Additions
- Dark mode toggle (if light mode ever needed)
- Additional icon designs for new apps
- Animation library for page transitions
- Loading states for async content
- Error/success message styling
- Modal/dialog system
- Toast notification component

### Maintenance Notes
- Review color contrast if background changes
- Test new components on all breakpoints
- Keep icon library consistent in style
- Update this guide when patterns change

---

**End of Style Guide V2**

*This document is the source of truth for all frontend design decisions in The Grid. All new UI work must reference and adhere to these standards.*
