# Code Generation Workflow

Detailed patterns for mapping Figma designs to project code.

## Component Mapping Strategy

### 1. Inventory Existing Components

Before generating anything, scan the project's component directories:
```
Glob: src/components/**/*.{tsx,jsx,vue,svelte}
```

Build a mental map: what exists, what props they take, how they're styled.

### 2. Map Figma → Project Components

| Figma Layer Name | Likely Project Component | Action |
|-----------------|------------------------|--------|
| Button, CTA | `Button` | Reuse with variant prop |
| Input, TextField | `Input`, `TextField` | Reuse existing |
| Card, Panel | `Card` | Reuse or extend |
| Nav, Header | `Navbar`, `Header` | Reuse layout component |
| Modal, Dialog | `Dialog`, `Modal` | Reuse existing |
| Icon/* | Icon library | Use existing icon set |
| Custom/unique | — | Create new component |

### 3. Handle Missing Components

When a Figma component has no project equivalent:
1. Create it in the project's component directory
2. Follow the project's component pattern (props interface, styling approach)
3. Make it reusable — extract props for variants if the design shows multiple states

## Design Token Mapping

### Colors

```
Figma color → Check project tokens → Map or extend

Example (Tailwind):
  Figma #3B82F6 → Already exists as `blue-500` → Use `text-blue-500`
  Figma #1A1A2E → Not in config → Add to tailwind.config as `primary`

Example (CSS vars):
  Figma #3B82F6 → Exists as `--color-primary` → Use `var(--color-primary)`
  Figma #1A1A2E → Not defined → Add `--color-surface: #1A1A2E` to globals
```

### Typography

```
Figma style → Map to project type scale

Example (Tailwind):
  32px/700 → `text-3xl font-bold`
  16px/400 → `text-base font-normal`
  14px/500 → `text-sm font-medium`

Example (CSS vars / custom):
  32px/700 → `var(--font-heading-lg)` or `.heading-lg`
```

### Spacing

```
Figma spacing → Map to project spacing scale

Example (Tailwind):
  8px → `p-2` or `gap-2`
  16px → `p-4` or `gap-4`
  24px → `p-6` or `gap-6`

Example (custom):
  8px → `var(--space-2)` or `spacing.sm`
```

## Layout Translation

### Figma Auto-Layout → CSS

| Figma Property | CSS Equivalent | Tailwind |
|---------------|---------------|----------|
| Horizontal | `flex-direction: row` | `flex flex-row` |
| Vertical | `flex-direction: column` | `flex flex-col` |
| Gap: 16 | `gap: 16px` | `gap-4` |
| Padding: 24 | `padding: 24px` | `p-6` |
| Space between | `justify-content: space-between` | `justify-between` |
| Align center | `align-items: center` | `items-center` |
| Fill container | `flex: 1` | `flex-1` |
| Hug contents | `width: fit-content` | `w-fit` |

### Figma Constraints → Responsive

| Figma Constraint | Responsive Approach |
|-----------------|-------------------|
| Fixed width | `w-[320px]` or `max-w-sm` |
| Fill container | `w-full` |
| Left & Right (stretch) | `w-full` with padding |
| Center | `mx-auto` |

## Code Generation Rules

1. **One component per file** — match project convention
2. **Props interface first** — define the component's API before implementation
3. **Semantic HTML** — use `<nav>`, `<main>`, `<section>`, `<article>`, `<button>`, not just `<div>`
4. **Accessibility** — add `aria-label`, `role`, `alt` text from Figma layer names
5. **Responsive** — if Figma shows mobile + desktop frames, implement both with breakpoints
6. **No hardcoded text** — use the actual text from Figma designs, but structure for i18n readiness
7. **Images** — use `next/image` (Next.js), `<img>` with loading="lazy" (others), reference asset paths

## File Organization

Generate files matching the project's structure:

```
# If project uses flat structure:
src/components/HeroSection.tsx
src/components/FeatureCard.tsx

# If project uses grouped structure:
src/components/hero/HeroSection.tsx
src/components/hero/HeroSection.module.css
src/components/features/FeatureCard.tsx

# If project uses barrel exports:
src/components/hero/index.ts  ← re-export
```

## Post-Generation Checklist

```
- [ ] All imports resolve (no missing dependencies)
- [ ] Types are correct (no `any` in TypeScript)
- [ ] Styling matches project approach (no mixing Tailwind + CSS modules)
- [ ] Existing components reused where possible
- [ ] New components follow project naming convention
- [ ] Responsive breakpoints match project's breakpoint system
- [ ] Images/assets referenced correctly
- [ ] Build passes: npm run build
```
