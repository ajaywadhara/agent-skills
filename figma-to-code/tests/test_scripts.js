#!/usr/bin/env node
/**
 * Unit tests for figma-to-code scripts.
 * Run: node tests/test_scripts.js
 *
 * Tests both detect_project.js and parse_figma_json.js against fixtures.
 * Zero dependencies — uses Node assert module.
 */

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");
const assert = require("assert");

const SCRIPTS_DIR = path.join(__dirname, "..", "scripts");
const FIXTURES_DIR = path.join(__dirname, "fixtures");

let passed = 0;
let failed = 0;
const failures = [];

function test(name, fn) {
  try {
    fn();
    passed++;
    console.log(`  PASS  ${name}`);
  } catch (err) {
    failed++;
    failures.push({ name, error: err.message });
    console.log(`  FAIL  ${name}`);
    console.log(`        ${err.message}`);
  }
}

function runScript(script, args = "") {
  return execSync(`node "${path.join(SCRIPTS_DIR, script)}" ${args}`, {
    encoding: "utf8",
    timeout: 10000,
  });
}

function runScriptWithFixtureProject(script, fixturePkg) {
  // Create a temp dir with the fixture package.json
  const tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "ftc-test-"));
  fs.copyFileSync(path.join(FIXTURES_DIR, fixturePkg), path.join(tmp, "package.json"));
  try {
    return runScript(script, `"${tmp}"`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// ─── detect_project.js tests ────────────────────────────────────────

console.log("\n--- detect_project.js ---\n");

test("detects no package.json gracefully", () => {
  const tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "ftc-empty-"));
  try {
    const output = JSON.parse(runScript("detect_project.js", `"${tmp}"`));
    assert.strictEqual(output.detected, false);
    assert.ok(output.message.includes("No package.json"));
    assert.ok(output.recommendation.includes("Next.js"));
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test("detects Next.js + TypeScript + Tailwind + shadcn", () => {
  const output = JSON.parse(runScriptWithFixtureProject("detect_project.js", "nextjs-package.json"));
  assert.strictEqual(output.detected, true);
  assert.strictEqual(output.framework.name, "nextjs");
  assert.strictEqual(output.framework.language, "typescript");
  assert.strictEqual(output.styling.approach, "tailwind");
  const libNames = output.component_library.libraries.map((l) => l.name);
  assert.ok(libNames.includes("shadcn-ui"), `Expected shadcn-ui, got: ${libNames}`);
});

test("detects Vue + Sass + Mantine + Pinia", () => {
  const output = JSON.parse(runScriptWithFixtureProject("detect_project.js", "vue-package.json"));
  assert.strictEqual(output.detected, true);
  assert.strictEqual(output.framework.name, "vue");
  assert.strictEqual(output.framework.language, "typescript");
  assert.strictEqual(output.styling.approach, "sass/scss");
  const libNames = output.component_library.libraries.map((l) => l.name);
  assert.ok(libNames.includes("mantine"), `Expected mantine, got: ${libNames}`);
  assert.ok(output.state_management.includes("pinia"));
});

test("handles bare project with no framework deps", () => {
  const output = JSON.parse(runScriptWithFixtureProject("detect_project.js", "empty-package.json"));
  assert.strictEqual(output.detected, true);
  assert.strictEqual(output.framework.name, "unknown");
  assert.strictEqual(output.component_library.libraries.length, 0);
  assert.strictEqual(output.state_management.length, 0);
});

test("returns valid JSON structure with all expected keys", () => {
  const output = JSON.parse(runScriptWithFixtureProject("detect_project.js", "nextjs-package.json"));
  const requiredKeys = ["detected", "project_name", "framework", "styling", "component_library", "file_patterns", "design_tokens", "state_management"];
  for (const key of requiredKeys) {
    assert.ok(key in output, `Missing key: ${key}`);
  }
});

// ─── parse_figma_json.js tests ──────────────────────────────────────

console.log("\n--- parse_figma_json.js ---\n");

test("shows usage when no args provided", () => {
  try {
    runScript("parse_figma_json.js");
    assert.fail("Should have exited with error");
  } catch (err) {
    assert.ok(err.stderr.includes("Usage:") || err.message.includes("Usage"));
  }
});

test("errors on missing file", () => {
  try {
    runScript("parse_figma_json.js", "/nonexistent/file.json");
    assert.fail("Should have exited with error");
  } catch (err) {
    assert.ok(err.stderr.includes("not found") || err.message.includes("not found"));
  }
});

test("parses sample Figma export correctly", () => {
  const fixture = path.join(FIXTURES_DIR, "sample-figma-export.json");
  const output = JSON.parse(runScript("parse_figma_json.js", `"${fixture}"`));

  // Should have 1 page
  assert.strictEqual(output.pages.length, 1);
  assert.strictEqual(output.pages[0].name, "Landing Page");

  // Should extract colors
  assert.ok(Object.keys(output.colors).length > 0, "Should extract colors");

  // Should extract typography
  assert.ok(output.typography.length > 0, "Should extract typography");
  // Sorted by font size descending
  for (let i = 1; i < output.typography.length; i++) {
    assert.ok(output.typography[i - 1].fontSize >= output.typography[i].fontSize, "Typography should be sorted by size desc");
  }

  // Should extract components
  assert.ok(output.components.length > 0, "Should extract components");
  const compNames = output.components.map((c) => c.name);
  assert.ok(compNames.includes("CTA Button"), `Expected CTA Button, got: ${compNames}`);
  assert.ok(compNames.includes("Feature Card"), `Expected Feature Card, got: ${compNames}`);

  // Should extract spacing
  assert.ok(output.spacing_scale.length > 0, "Should extract spacing");
  // Sorted ascending
  for (let i = 1; i < output.spacing_scale.length; i++) {
    assert.ok(output.spacing_scale[i - 1] <= output.spacing_scale[i], "Spacing should be sorted ascending");
  }
});

test("extracts layout tree with correct structure", () => {
  const fixture = path.join(FIXTURES_DIR, "sample-figma-export.json");
  const output = JSON.parse(runScript("parse_figma_json.js", `"${fixture}"`));

  const page = output.pages[0];
  assert.ok(page.layout_tree, "Should have layout_tree");
  assert.ok(page.layout_tree.children, "Layout tree should have children");
  assert.ok(page.layout_tree.children.length >= 2, "Should have Hero + Features sections");
});

test("outputs to directory with --output-dir", () => {
  const fixture = path.join(FIXTURES_DIR, "sample-figma-export.json");
  const tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "ftc-out-"));
  const outDir = path.join(tmp, "parsed");

  try {
    runScript("parse_figma_json.js", `"${fixture}" --output-dir "${outDir}"`);

    assert.ok(fs.existsSync(path.join(outDir, "design-tokens.json")), "Should create design-tokens.json");
    assert.ok(fs.existsSync(path.join(outDir, "components.json")), "Should create components.json");
    assert.ok(fs.existsSync(path.join(outDir, "layout-tree.json")), "Should create layout-tree.json");

    // Validate JSON is parseable
    const tokens = JSON.parse(fs.readFileSync(path.join(outDir, "design-tokens.json"), "utf8"));
    assert.ok(tokens.colors, "design-tokens should have colors");
    assert.ok(tokens.typography, "design-tokens should have typography");
    assert.ok(tokens.spacing, "design-tokens should have spacing");
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test("deduplicates typography entries", () => {
  const fixture = path.join(FIXTURES_DIR, "sample-figma-export.json");
  const output = JSON.parse(runScript("parse_figma_json.js", `"${fixture}"`));

  // Check no duplicate font family + size + weight combos
  const seen = new Set();
  for (const t of output.typography) {
    const key = `${t.fontFamily}-${t.fontSize}-${t.fontWeight}`;
    assert.ok(!seen.has(key), `Duplicate typography entry: ${key}`);
    seen.add(key);
  }
});

test("handles component with auto-layout info", () => {
  const fixture = path.join(FIXTURES_DIR, "sample-figma-export.json");
  const output = JSON.parse(runScript("parse_figma_json.js", `"${fixture}"`));

  const ctaButton = output.components.find((c) => c.name === "CTA Button");
  assert.ok(ctaButton, "Should find CTA Button component");
  assert.ok(ctaButton.layout, "CTA Button should have layout info");
  assert.strictEqual(ctaButton.layout.mode, "HORIZONTAL");
  assert.strictEqual(ctaButton.layout.gap, 8);
  assert.ok(ctaButton.children, "CTA Button should have children");
});

// ─── Summary ────────────────────────────────────────────────────────

console.log("\n" + "=".repeat(50));
console.log(`Results: ${passed} passed, ${failed} failed, ${passed + failed} total`);

if (failures.length > 0) {
  console.log("\nFailures:");
  for (const f of failures) {
    console.log(`  - ${f.name}: ${f.error}`);
  }
  process.exit(1);
} else {
  console.log("\nAll tests passed!");
  process.exit(0);
}
