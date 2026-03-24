---
name: figma-to-code
description: Convert Figma designs into production UI code. Accepts Figma JSON exports, screenshots, or dev-mode snippets. Detects the project's existing frontend framework, design system, and component patterns — generates code that matches. Use when the user wants to build UI from Figma, convert Figma to code, implement a Figma design, or mentions "figma pack".
---

# Figma to Code

Convert Figma design files into production-ready UI code that integrates with the project's existing codebase.

## When to Use

- User provides Figma exports (JSON, images, screenshots, or dev-mode code)
- User asks to "build UI from Figma", "implement this design", or "convert Figma to code"
- User mentions a "figma pack" or design handoff

## Supported Input Formats

1. **Figma JSON export** — richest data (via Figma REST API or export plugin). Run `parse_figma_json.js` to extract structure.
2. **Screenshots/images** — read visually with the Read tool. Extract layout, colors, typography, spacing.
3. **Dev-mode snippets** — CSS/code copied from Figma dev mode. Use directly as reference.
4. **SVG/asset exports** — icons and illustrations. Place in project assets directory.

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Collect Figma inputs (JSON, images, assets)
- [ ] Step 2: Detect project setup (framework, design system, patterns)
- [ ] Step 3: Parse Figma data and extract design tokens
- [ ] Step 4: Map Figma components to project components
- [ ] Step 5: Generate UI code (pages, components, styles)
- [ ] Step 6: Validate output (build check, visual review)
```

### Step 1: Collect Figma Inputs

Ask the user for their Figma exports. See [references/figma-export-guide.md](references/figma-export-guide.md) for export instructions to share with the user.

Locate all provided files:
- JSON files → parse with `scripts/parse_figma_json.js`
- Images → read visually to extract design intent
- SVGs/assets → catalog for later placement

### Step 2: Detect Project Setup

Run the detection script from the project root:

```bash
node SKILL_DIR/scripts/detect_project.js .
```

This outputs a JSON report: framework, styling approach, component library, file structure patterns, and existing design tokens. See [references/project-detection.md](references/project-detection.md) for details.

**If no existing project**: ask user for preferred stack. Default to Next.js + TypeScript + Tailwind CSS.

### Step 3: Parse Figma Data

For JSON exports:
```bash
node SKILL_DIR/scripts/parse_figma_json.js path/to/figma-export.json
```

Extracts: component tree, color palette, typography scale, spacing values, layout structure.

For images: read each image with the Read tool. Note: layout grid, component boundaries, text content, color usage, spacing rhythm, typography hierarchy.

### Step 4: Map Components

Using the detection report + Figma data:

1. **Match existing components** — if the project has a `Button`, `Card`, `Input`, etc., reuse them
2. **Identify gaps** — components in the design not yet in the project
3. **Map design tokens** — Figma colors/fonts → project's token system (CSS vars, Tailwind config, theme file)
4. **Decide new components** — create only what's missing, following project conventions

See [references/code-generation-workflow.md](references/code-generation-workflow.md) for mapping patterns.

### Step 5: Generate Code

Generate code matching the project's patterns. See [references/framework-mappings.md](references/framework-mappings.md) for framework-specific guidance.

**Rules:**
- Use the project's existing file naming convention and directory structure
- Import from the project's component library, not third-party, when components exist
- Follow the project's styling approach (Tailwind classes, CSS modules, styled-components, etc.)
- Use the project's design tokens (colors, spacing, typography) — extend only if the design introduces new ones
- Generate responsive layouts matching the design's breakpoints
- Extract repeated patterns into reusable components

### Step 6: Validate

1. Run the project's build/lint: `npm run build` or equivalent
2. Fix any type errors or lint issues
3. Present a summary of generated files for visual review

## References

- [Figma export guide](references/figma-export-guide.md) — how to export from Figma
- [Project detection](references/project-detection.md) — how detection works
- [Code generation workflow](references/code-generation-workflow.md) — detailed generation patterns
- [Framework mappings](references/framework-mappings.md) — framework-specific code patterns
