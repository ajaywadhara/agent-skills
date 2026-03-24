# figma-to-code

Convert Figma designs into production-ready UI code that integrates with your project's existing codebase — no MCP required.

## What It Does

This skill takes Figma exports (JSON, screenshots, dev-mode snippets, or asset files) and generates UI code that matches your project's existing frontend setup. It detects your framework, design system, component library, and file conventions, then generates code that fits right in.

**If no existing project exists**, it falls back to Next.js + TypeScript + Tailwind CSS + shadcn/ui.

## Supported Inputs

| Input Type | How to Get It | Data Richness |
|------------|--------------|---------------|
| **Figma JSON** | REST API or "Figma to JSON" plugin | Best — full layout, tokens, components |
| **Screenshots** | Export frames as PNG (2x) | Good — visual analysis by Claude |
| **Dev-mode snippets** | Copy CSS from Figma Dev Mode | Supplementary — exact values |
| **SVG/asset exports** | Export icons/images from Figma | Assets only — placed in project |

See `references/figma-export-guide.md` for detailed export instructions.

## How It Works

1. **Collect** — Gather Figma exports (JSON, images, assets) into a `figma/` directory
2. **Detect** — Run `detect_project.js` to scan your project's framework, styling, components, and tokens
3. **Parse** — Run `parse_figma_json.js` (if JSON available) to extract design tokens, component tree, and layout structure
4. **Map** — Match Figma components to existing project components; identify gaps
5. **Generate** — Create UI code following your project's patterns and conventions
6. **Validate** — Run build/lint, fix errors, present summary for review

## Scripts

### `scripts/detect_project.js`

Scans a project directory and outputs a JSON report of the frontend setup.

```bash
node scripts/detect_project.js /path/to/project
```

**Detects:** framework (Next.js, React, Vue, Svelte, Angular), language (TS/JS), styling (Tailwind, CSS Modules, styled-components, Sass), component libraries (shadcn/ui, MUI, Chakra, Radix, Mantine), file naming conventions, design token files, and state management.

### `scripts/parse_figma_json.js`

Parses a Figma JSON export and extracts structured design data.

```bash
# Output to stdout
node scripts/parse_figma_json.js figma/export.json

# Output to directory (creates design-tokens.json, components.json, layout-tree.json)
node scripts/parse_figma_json.js figma/export.json --output-dir figma/parsed
```

**Extracts:** color palette (sorted by frequency), typography scale, spacing values, component tree with auto-layout info, and page layout structure.

## Project Detection Examples

**Existing Next.js + Tailwind + shadcn project:**
- Reuses existing `Button`, `Card`, `Input` components
- Maps Figma colors to Tailwind config / CSS variables
- Generates `.tsx` files in the project's component directory
- Follows PascalCase naming if that's what the project uses

**No project found:**
- Asks for preferred stack (defaults to Next.js + TS + Tailwind + shadcn/ui)
- Scaffolds with `create-next-app` + shadcn init
- Creates a minimal token system in `tailwind.config.ts`

## Usage

Invoke the skill by running `/figma-to-code` in Claude Code, or by asking Claude to "build UI from Figma", "implement this design", or mentioning a "figma pack".

## Requirements

- **Node.js** (v18+) — scripts use only Node stdlib, no npm install needed
- **Claude Code** — the skill runs within Claude Code's agent environment

## File Structure

```
figma-to-code/
├── SKILL.md                          ← Skill entry point (<200 lines)
├── README.md                         ← This file
├── scripts/
│   ├── detect_project.js             ← Project setup detection
│   └── parse_figma_json.js           ← Figma JSON parser
└── references/
    ├── figma-export-guide.md         ← How to export from Figma
    ├── project-detection.md          ← Detection details and output format
    ├── code-generation-workflow.md   ← Component mapping and generation rules
    └── framework-mappings.md         ← Framework-specific code patterns
```
