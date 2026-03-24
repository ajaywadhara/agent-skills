# Figma Export Guide

Instructions to share with the user for exporting from Figma.

## Option 1: Figma JSON Export (Best)

Richest data — preserves layout, tokens, components, auto-layout.

### Via Plugin
1. Install "Figma to JSON" or "Design Tokens" plugin from Figma Community
2. Select the frames/pages to export
3. Run the plugin → export as `.json`
4. Place the JSON file in the project directory (e.g., `figma/export.json`)

### Via Figma REST API

Requires a Figma personal access token (set as env var `FIGMA_TOKEN`).

```bash
# Get file data
curl -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/<file-key>" \
  -o figma/export.json

# Get specific node
curl -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/<file-key>/nodes?ids=<node-id>" \
  -o figma/export.json
```

To get `<file-key>`: open the Figma file and copy from the URL (`figma.com/design/<file-key>/...`).

## Option 2: Screenshots/Images (Good)

Works when JSON export isn't available. Agent reads images visually.

1. In Figma, select the frame or page
2. Right-click → "Copy as PNG" or File → Export
3. Export at 2x resolution for clarity
4. Save to `figma/` directory with descriptive names:
   - `figma/homepage-desktop.png`
   - `figma/homepage-mobile.png`
   - `figma/component-buttons.png`

**Tip**: Export individual component frames separately for better recognition.

## Option 3: Dev Mode Snippets (Supplementary)

Useful as supplementary data alongside images.

1. Open Figma Dev Mode (toggle in top toolbar)
2. Click on any element
3. Copy the CSS/code from the right panel
4. Paste into a file: `figma/dev-mode-notes.md`

## Option 4: Asset Export (Icons, Images)

1. Select icons/images in Figma
2. Right-click → Export → choose SVG for icons, PNG/WebP for images
3. Save to `figma/assets/` directory
4. Agent will place them in the project's asset directory

## Recommended Export Bundle ("Figma Pack")

For best results, provide:
```
figma/
├── export.json           ← JSON export (if available)
├── homepage-desktop.png  ← Full page screenshots
├── homepage-mobile.png
├── components.png        ← Component library screenshot
├── dev-mode-notes.md     ← Any dev mode CSS/code snippets
└── assets/               ← Exported SVGs, images
    ├── logo.svg
    ├── icon-search.svg
    └── hero-image.webp
```
