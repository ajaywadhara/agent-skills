# Evaluation Scenarios

Three eval scenarios to validate the skill works end-to-end.

## Eval 1: Existing Next.js + shadcn Project

**Setup:** A Next.js 15 project with TypeScript, Tailwind, shadcn/ui, and existing `Button`, `Card` components.

**Input:** Figma JSON export of a landing page with hero section, feature cards, and CTA buttons.

**Expected behavior:**
- [ ] `detect_project.js` identifies Next.js + TypeScript + Tailwind + shadcn-ui
- [ ] `parse_figma_json.js` extracts colors, typography, components, layout tree
- [ ] Agent reuses existing `Button` and `Card` components (imports from `@/components/ui/`)
- [ ] New components use `.tsx` files with PascalCase naming
- [ ] Styling uses Tailwind classes, not inline styles or CSS modules
- [ ] Colors map to existing CSS variables or Tailwind config
- [ ] Generated page uses `next/image` for images
- [ ] Build passes: `npm run build`

**Failure indicators:**
- Creates new Button/Card instead of reusing existing ones
- Uses CSS modules or styled-components in a Tailwind project
- Generates `.jsx` files in a TypeScript project
- Hardcodes colors instead of using design tokens

## Eval 2: Vue + Sass Project (Different Stack)

**Setup:** A Vue 3 project with TypeScript, Sass/SCSS, Mantine UI, and Pinia state management.

**Input:** Same Figma JSON export.

**Expected behavior:**
- [ ] `detect_project.js` identifies Vue + TypeScript + Sass + Mantine + Pinia
- [ ] Agent generates `.vue` SFC files (not `.tsx`)
- [ ] Uses `<script setup lang="ts">` pattern
- [ ] Styling uses `<style scoped>` with SCSS
- [ ] Imports Mantine components where applicable
- [ ] File structure matches Vue conventions (`src/components/`, `src/views/`)

**Failure indicators:**
- Generates React JSX in a Vue project
- Uses Tailwind classes in a Sass project
- Ignores Mantine and creates custom components from scratch

## Eval 3: Empty Directory (No Project)

**Setup:** Empty directory with no `package.json`.

**Input:** Figma screenshots (PNG images) of a dashboard with sidebar, header, data table, and charts.

**Expected behavior:**
- [ ] `detect_project.js` returns `detected: false` with fallback recommendation
- [ ] Agent asks user for preferred stack OR defaults to Next.js + TS + Tailwind
- [ ] Suggests scaffolding: `npx create-next-app@latest`
- [ ] Generates complete component set from visual analysis of screenshots
- [ ] Creates a reasonable file structure from scratch
- [ ] Extracts colors, spacing, typography from visual inspection

**Failure indicators:**
- Crashes on missing `package.json`
- Generates code without asking about framework preference
- Creates an incoherent mix of frameworks

## Running Evals

### Automated (scripts only)
```bash
node tests/test_scripts.js
```

### Manual (full skill workflow)
1. Set up each scenario's project directory
2. Run `/figma-to-code` in Claude Code
3. Check against the expected behavior checklist above
4. Record pass/fail per checkbox

### Regression
After any changes to the skill, re-run `node tests/test_scripts.js` to catch regressions.
