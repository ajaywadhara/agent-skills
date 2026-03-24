# Project Detection

The `detect_project.py` script analyzes the current project to determine how to generate code that fits.

## What It Detects

| Category | How | Examples |
|----------|-----|---------|
| Framework | `package.json` dependencies | Next.js, React, Vue, Svelte, Angular |
| Language | TypeScript presence | `.ts`/`.tsx` files, `typescript` dep |
| Styling | Dependencies + config files | Tailwind, CSS Modules, styled-components, Sass |
| Component library | Dependencies + patterns | shadcn/ui, MUI, Chakra, Radix, Mantine |
| File patterns | Directory scan | Component dirs, naming convention (PascalCase, kebab-case) |
| Design tokens | Token/theme files | CSS variables, Tailwind theme, theme files |
| State management | Dependencies | Zustand, Redux Toolkit, Jotai |

## Output Format

```json
{
  "detected": true,
  "project_name": "my-app",
  "framework": {
    "name": "nextjs",
    "version": "^14.0.0",
    "language": "typescript"
  },
  "styling": {
    "approach": "tailwind",
    "details": ["tailwindcss", "postcss"],
    "tailwind_config": "/path/to/tailwind.config.ts"
  },
  "component_library": {
    "libraries": [
      {"name": "shadcn-ui", "package": "local", "version": "n/a"}
    ]
  },
  "file_patterns": {
    "component_dirs": ["src/components", "app"],
    "naming_convention": "PascalCase",
    "file_extensions": [".tsx"]
  },
  "design_tokens": {
    "files": ["src/styles/globals.css", "tailwind.config.ts"],
    "css_vars": true,
    "has_custom_tailwind_theme": true
  },
  "state_management": ["zustand"]
}
```

## Using the Report

### Existing Project

Use the report to:
1. **Framework** → determines JSX vs templates, routing approach, file conventions
2. **Styling** → determines class names (Tailwind) vs CSS-in-JS vs module imports
3. **Component library** → reuse existing components; only create what's missing
4. **File patterns** → match naming and directory structure
5. **Design tokens** → map Figma colors/fonts to existing token system

### No Project Found

When `detected: false`:
1. Ask user for preferred stack
2. Default fallback: **Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui**
3. Scaffold with: `npx create-next-app@latest` then add shadcn/ui
4. Create a minimal token system in `tailwind.config.ts`

## Manual Override

If detection misses something, the user can provide:
- "We use shadcn/ui" → treat as shadcn project
- "Our components are in `lib/ui/`" → use that directory
- "We use CSS modules, not Tailwind" → generate `.module.css` files
