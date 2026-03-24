# Framework-Specific Code Patterns

Patterns for generating code in each supported framework.

## Next.js (App Router)

```
app/
├── page.tsx              ← home page
├── layout.tsx            ← root layout
├── (marketing)/
│   └── page.tsx          ← marketing pages
└── components/           ← shared components (or src/components/)
```

**Component template:**
```tsx
interface HeroSectionProps {
  title: string;
  subtitle: string;
}

export function HeroSection({ title, subtitle }: HeroSectionProps) {
  return (
    <section className="flex flex-col items-center gap-6 px-4 py-16">
      <h1 className="text-4xl font-bold">{title}</h1>
      <p className="text-lg text-muted-foreground">{subtitle}</p>
    </section>
  );
}
```

**Images:** Use `next/image` with width/height from Figma.
**Fonts:** Use `next/font` — map Figma font family to Google Fonts or local font.
**Metadata:** Generate `metadata` export from page title in Figma.

## React (Vite / CRA)

```
src/
├── App.tsx
├── components/
├── pages/ or views/
└── styles/
```

**Router:** React Router — create route entries in `App.tsx`.
**Images:** Standard `<img>` with lazy loading.

## Vue 3

```
src/
├── App.vue
├── components/
├── views/
└── assets/
```

**Component template:**
```vue
<script setup lang="ts">
interface Props {
  title: string;
  subtitle: string;
}
defineProps<Props>();
</script>

<template>
  <section class="hero">
    <h1>{{ title }}</h1>
    <p>{{ subtitle }}</p>
  </section>
</template>

<style scoped>
.hero { /* styles */ }
</style>
```

## Svelte / SvelteKit

```
src/
├── routes/
│   ├── +page.svelte
│   └── +layout.svelte
└── lib/
    └── components/
```

**Component template:**
```svelte
<script lang="ts">
  export let title: string;
  export let subtitle: string;
</script>

<section class="flex flex-col items-center gap-6 px-4 py-16">
  <h1 class="text-4xl font-bold">{title}</h1>
  <p class="text-lg text-muted-foreground">{subtitle}</p>
</section>
```

## Component Library Patterns

### shadcn/ui
- Import from `@/components/ui/button` (local, not npm)
- Use `cn()` utility for class merging
- Extend with variants using `cva()`
- Check existing components: `ls src/components/ui/`

### Material UI (MUI)
- Import from `@mui/material`
- Use `sx` prop for one-off styles, `styled()` for reusable
- Use MUI's theme tokens: `theme.palette.primary.main`

### Chakra UI
- Import from `@chakra-ui/react`
- Use style props: `<Box p={4} bg="gray.100">`
- Extend theme for custom tokens

### Radix UI (headless)
- Import primitives: `@radix-ui/react-dialog`
- Style with project's CSS approach
- Compose with project's design tokens

## Responsive Patterns

When Figma shows multiple viewport frames:

```tsx
{/* Mobile-first with Tailwind breakpoints */}
<div className="flex flex-col md:flex-row gap-4 md:gap-8">
  <div className="w-full md:w-1/2">
    {/* Content */}
  </div>
</div>
```

Map Figma frame widths to breakpoints:
- 375px frame → mobile (default)
- 768px frame → `md:` breakpoint
- 1024px frame → `lg:` breakpoint
- 1440px frame → `xl:` breakpoint

## Fallback Stack (No Existing Project)

When no project exists, scaffold with:

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app
npx shadcn@latest init
```

Then generate components into this structure.
