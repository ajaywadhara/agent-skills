#!/usr/bin/env node
/**
 * Parse Figma JSON export and extract design structure, tokens, and component tree.
 * Works with exports from Figma REST API or JSON export plugins.
 *
 * Usage: node parse_figma_json.js <figma_json_file> [--output-dir <dir>]
 */

const fs = require("fs");
const path = require("path");

function extractColors(node, colors) {
  const fills = node.fills || [];
  for (const fill of fills) {
    if (fill.type === "SOLID" && fill.visible !== false) {
      const c = fill.color || {};
      const r = Math.round((c.r || 0) * 255);
      const g = Math.round((c.g || 0) * 255);
      const b = Math.round((c.b || 0) * 255);
      const a = Math.round((c.a ?? 1) * 100) / 100;
      const hex = `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
      const key = a === 1 ? hex : `rgba(${r}, ${g}, ${b}, ${a})`;
      colors[key] = (colors[key] || 0) + 1;
    }
  }
  for (const child of node.children || []) extractColors(child, colors);
}

function extractTypography(node, typography) {
  if (node.type === "TEXT") {
    const style = node.style || {};
    typography.push({
      fontFamily: style.fontFamily || "",
      fontSize: style.fontSize || 0,
      fontWeight: style.fontWeight || 400,
      lineHeight: style.lineHeightPx || 0,
      letterSpacing: style.letterSpacing || 0,
      textContent: (node.characters || "").slice(0, 50),
    });
  }
  for (const child of node.children || []) extractTypography(child, typography);
}

function extractComponents(node, components) {
  const type = node.type || "";
  if (["COMPONENT", "COMPONENT_SET", "INSTANCE"].includes(type)) {
    const comp = {
      name: node.name || "",
      type,
      id: node.id || "",
      size: {
        width: node.absoluteBoundingBox?.width || 0,
        height: node.absoluteBoundingBox?.height || 0,
      },
    };
    if (node.layoutMode) {
      comp.layout = {
        mode: node.layoutMode,
        gap: node.itemSpacing || 0,
        padding: {
          top: node.paddingTop || 0,
          right: node.paddingRight || 0,
          bottom: node.paddingBottom || 0,
          left: node.paddingLeft || 0,
        },
        align: node.primaryAxisAlignItems || "",
        crossAlign: node.counterAxisAlignItems || "",
      };
    }
    if (node.children?.length) {
      comp.children = node.children.map((c) => ({ name: c.name || "", type: c.type || "" }));
    }
    components.push(comp);
  }
  for (const child of node.children || []) extractComponents(child, components);
}

function extractLayoutTree(node, depth = 0, maxDepth = 4) {
  if (depth > maxDepth) return { name: node.name || "", type: node.type || "", truncated: true };

  const tree = { name: node.name || "", type: node.type || "" };
  const bbox = node.absoluteBoundingBox;
  if (bbox) tree.size = { w: Math.round(bbox.width || 0), h: Math.round(bbox.height || 0) };
  if (node.layoutMode) {
    tree.layout = node.layoutMode.toLowerCase();
    tree.gap = node.itemSpacing || 0;
  }
  if (node.cornerRadius) tree.borderRadius = node.cornerRadius;
  if (node.opacity != null && node.opacity !== 1) tree.opacity = Math.round(node.opacity * 100) / 100;

  if (node.children?.length) {
    tree.children = node.children.map((c) => extractLayoutTree(c, depth + 1, maxDepth));
  }
  return tree;
}

function extractSpacing(node, spacings) {
  for (const key of ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "itemSpacing"]) {
    if (node[key] > 0) spacings.add(Math.round(node[key]));
  }
  for (const child of node.children || []) extractSpacing(child, spacings);
}

function dedupeTypography(typography) {
  const seen = new Set();
  const unique = [];
  for (const t of typography) {
    const key = `${t.fontFamily}-${t.fontSize}-${t.fontWeight}`;
    if (!seen.has(key)) {
      seen.add(key);
      unique.push(t);
    }
  }
  return unique.sort((a, b) => b.fontSize - a.fontSize);
}

function parseFigmaFile(data) {
  const result = { pages: [], colors: {}, typography: [], components: [], spacing_scale: [] };
  const document = data.document || data;
  let pages = document.children || [];

  if (!pages.length && data.nodes) {
    pages = Object.values(data.nodes).map((n) => n.document).filter(Boolean);
  }

  const allTypography = [];
  const allSpacings = new Set();

  for (const page of pages) {
    result.pages.push({ name: page.name || "Untitled", layout_tree: extractLayoutTree(page) });
    extractColors(page, result.colors);
    extractTypography(page, allTypography);
    extractComponents(page, result.components);
    extractSpacing(page, allSpacings);
  }

  result.typography = dedupeTypography(allTypography);
  result.spacing_scale = [...allSpacings].sort((a, b) => a - b);

  // Sort colors by frequency
  result.colors = Object.fromEntries(
    Object.entries(result.colors).sort(([, a], [, b]) => b - a)
  );

  return result;
}

function main() {
  const args = process.argv.slice(2);
  if (!args.length) {
    console.error("Usage: node parse_figma_json.js <figma_json_file> [--output-dir <dir>]");
    process.exit(1);
  }

  const filePath = args[0];
  const outputDirIdx = args.indexOf("--output-dir");
  const outputDir = outputDirIdx >= 0 ? args[outputDirIdx + 1] : null;

  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found: ${filePath}`);
    process.exit(1);
  }

  const data = JSON.parse(fs.readFileSync(filePath, "utf8"));
  const result = parseFigmaFile(data);

  if (outputDir) {
    fs.mkdirSync(outputDir, { recursive: true });

    fs.writeFileSync(
      path.join(outputDir, "design-tokens.json"),
      JSON.stringify({ colors: result.colors, typography: result.typography, spacing: result.spacing_scale }, null, 2)
    );
    fs.writeFileSync(path.join(outputDir, "components.json"), JSON.stringify(result.components, null, 2));
    fs.writeFileSync(path.join(outputDir, "layout-tree.json"), JSON.stringify(result.pages, null, 2));

    console.log(`Output written to ${outputDir}/`);
    console.log(`  - design-tokens.json (${Object.keys(result.colors).length} colors, ${result.typography.length} type styles)`);
    console.log(`  - components.json (${result.components.length} components)`);
    console.log(`  - layout-tree.json (${result.pages.length} pages)`);
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
}

main();
