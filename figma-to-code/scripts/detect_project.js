#!/usr/bin/env node
/**
 * Detect project frontend setup: framework, styling, component library, patterns.
 * Outputs a JSON report to stdout.
 *
 * Usage: node detect_project.js <project_root>
 */

const fs = require("fs");
const path = require("path");

function detectPackageJson(root) {
  const pkgPath = path.join(root, "package.json");
  if (!fs.existsSync(pkgPath)) return null;
  const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
  const deps = { ...pkg.dependencies, ...pkg.devDependencies };
  return { name: pkg.name || "", deps };
}

function detectFramework(deps) {
  const result = { name: "unknown", version: null, language: "javascript" };
  const map = {
    next: "nextjs",
    react: "react",
    vue: "vue",
    nuxt: "nuxt",
    svelte: "svelte",
    "@sveltejs/kit": "sveltekit",
    "@angular/core": "angular",
    gatsby: "gatsby",
    astro: "astro",
    "solid-js": "solidjs",
    remix: "remix",
    "@remix-run/react": "remix",
  };
  const priority = [
    "next", "nuxt", "@sveltejs/kit", "remix", "@remix-run/react",
    "gatsby", "astro", "vue", "svelte", "solid-js", "@angular/core", "react",
  ];
  for (const pkg of priority) {
    if (deps[pkg]) {
      result.name = map[pkg];
      result.version = deps[pkg];
      break;
    }
  }
  if (deps.typescript || Object.keys(deps).some((k) => k.startsWith("@types/"))) {
    result.language = "typescript";
  }
  return result;
}

function globFiles(dir, pattern) {
  // Simple recursive file finder
  const results = [];
  if (!fs.existsSync(dir)) return results;
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith(".") && entry.name !== "node_modules") {
        results.push(...globFiles(full, pattern));
      } else if (entry.isFile() && pattern.test(entry.name)) {
        results.push(full);
      }
    }
  } catch {}
  return results;
}

function detectStyling(deps, root) {
  const styling = { approach: "css", details: [] };
  const map = {
    tailwindcss: "tailwind",
    "styled-components": "styled-components",
    "@emotion/react": "emotion",
    "@emotion/styled": "emotion",
    sass: "sass/scss",
    less: "less",
    "@vanilla-extract/css": "vanilla-extract",
    "styled-jsx": "styled-jsx",
  };
  for (const [pkg, name] of Object.entries(map)) {
    if (deps[pkg]) {
      styling.approach = name;
      styling.details.push(pkg);
    }
  }

  // Check for CSS modules
  const moduleFiles = globFiles(path.join(root, "src"), /\.module\.(css|scss)$/);
  if (moduleFiles.length > 0) {
    styling.details.push("css-modules");
    if (styling.approach === "css") styling.approach = "css-modules";
  }

  // Tailwind config
  for (const cfg of ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.mjs"]) {
    if (fs.existsSync(path.join(root, cfg))) {
      styling.tailwind_config = path.join(root, cfg);
      break;
    }
  }

  // PostCSS
  if (fs.existsSync(path.join(root, "postcss.config.js")) || fs.existsSync(path.join(root, "postcss.config.mjs"))) {
    styling.details.push("postcss");
  }

  return styling;
}

function detectComponentLibrary(deps) {
  const libraries = [];
  const map = {
    "@mui/material": "material-ui",
    "@chakra-ui/react": "chakra-ui",
    antd: "ant-design",
    "@radix-ui/react-dialog": "radix-ui",
    "@headlessui/react": "headless-ui",
    "@mantine/core": "mantine",
    primereact: "primereact",
    "flowbite-react": "flowbite",
    "@nextui-org/react": "nextui",
  };
  for (const [pkg, name] of Object.entries(map)) {
    if (deps[pkg]) libraries.push({ name, package: pkg, version: deps[pkg] });
  }

  // shadcn/ui detection
  const indicators = [
    !!deps["@radix-ui/react-slot"],
    !!deps["class-variance-authority"],
    !!(deps.clsx || deps["tailwind-merge"]),
  ].filter(Boolean).length;
  if (indicators >= 2) {
    libraries.push({ name: "shadcn-ui", package: "local", version: "n/a" });
  }

  return { libraries };
}

function detectFilePatterns(root) {
  const patterns = { component_dirs: [], naming_convention: "unknown", file_extensions: new Set() };
  const searchDirs = [
    "src/components", "components", "app/components", "src/ui", "ui",
    "src/app", "app", "pages", "src/pages", "src/views", "views",
  ];

  for (const d of searchDirs) {
    if (fs.existsSync(path.join(root, d)) && fs.statSync(path.join(root, d)).isDirectory()) {
      patterns.component_dirs.push(d);
    }
  }

  for (const compDir of patterns.component_dirs) {
    const full = path.join(root, compDir);
    try {
      const entries = fs.readdirSync(full, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isFile()) continue;
        const ext = path.extname(entry.name);
        if ([".tsx", ".jsx", ".vue", ".svelte"].includes(ext)) {
          patterns.file_extensions.add(ext);
          const name = path.basename(entry.name, ext);
          if (name.includes("-")) patterns.naming_convention = "kebab-case";
          else if (name[0] === name[0].toUpperCase()) patterns.naming_convention = "PascalCase";
          else if (name.includes("_")) patterns.naming_convention = "snake_case";
          else patterns.naming_convention = "camelCase";
          break;
        }
      }
    } catch {}
    if (patterns.naming_convention !== "unknown") break;
  }

  patterns.file_extensions = [...patterns.file_extensions].sort();
  return patterns;
}

function detectDesignTokens(root) {
  const tokens = { files: [], css_vars: false, theme_file: null };
  const tokenPatterns = [
    "src/styles/tokens", "src/theme", "src/styles/theme",
    "styles/tokens", "theme", "src/design-tokens",
    "tokens", "src/styles/variables", "styles/variables",
  ];

  for (const pattern of tokenPatterns) {
    for (const ext of [".js", ".ts", ".json", ".css", ".scss"]) {
      const filePath = path.join(root, pattern + ext);
      if (fs.existsSync(filePath)) {
        tokens.files.push(path.relative(root, filePath));
        if (path.basename(filePath).toLowerCase().includes("theme")) {
          tokens.theme_file = path.relative(root, filePath);
        }
      }
    }
  }

  // Check for CSS custom properties
  const globalCssPatterns = [
    "src/styles/globals.css", "src/app/globals.css",
    "styles/globals.css", "app/globals.css", "src/index.css", "src/global.css",
  ];
  for (const p of globalCssPatterns) {
    const filePath = path.join(root, p);
    if (fs.existsSync(filePath)) {
      try {
        const content = fs.readFileSync(filePath, "utf8");
        if (content.includes("--") && content.includes(":")) {
          tokens.css_vars = true;
          tokens.files.push(p);
        }
      } catch {}
    }
  }

  // Tailwind custom theme
  for (const cfg of ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.mjs"]) {
    const cfgPath = path.join(root, cfg);
    if (fs.existsSync(cfgPath)) {
      try {
        const content = fs.readFileSync(cfgPath, "utf8");
        if (content.includes("extend") || content.includes("theme")) {
          tokens.files.push(cfg);
          tokens.has_custom_tailwind_theme = true;
        }
      } catch {}
    }
  }

  return tokens;
}

function detectStateManagement(deps) {
  const map = {
    zustand: "zustand",
    "@reduxjs/toolkit": "redux-toolkit",
    redux: "redux",
    recoil: "recoil",
    jotai: "jotai",
    valtio: "valtio",
    mobx: "mobx",
    pinia: "pinia",
    vuex: "vuex",
  };
  return Object.entries(map).filter(([pkg]) => deps[pkg]).map(([, name]) => name);
}

function main() {
  const root = path.resolve(process.argv[2] || ".");
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    console.log(JSON.stringify({ error: `Not a directory: ${root}` }));
    process.exit(1);
  }

  const pkgInfo = detectPackageJson(root);
  if (!pkgInfo) {
    console.log(JSON.stringify({
      detected: false,
      message: "No package.json found. This may not be a JS/TS frontend project.",
      recommendation: "Ask user for preferred stack. Default: Next.js + TypeScript + Tailwind CSS.",
    }, null, 2));
    process.exit(0);
  }

  const { deps } = pkgInfo;
  const report = {
    detected: true,
    project_name: pkgInfo.name,
    framework: detectFramework(deps),
    styling: detectStyling(deps, root),
    component_library: detectComponentLibrary(deps),
    file_patterns: detectFilePatterns(root),
    design_tokens: detectDesignTokens(root),
    state_management: detectStateManagement(deps),
  };

  console.log(JSON.stringify(report, null, 2));
}

main();
