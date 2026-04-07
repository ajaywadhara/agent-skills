# Hero Section Templates

SVG header templates for each theme. Each template is a complete `header.svg` file that gets committed to the profile repo.

All templates share a common structure but vary in visual treatment based on the theme.

---

## Common SVG Structure

```xml
<svg width="1200" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {GRADIENTS}
    {PATTERNS}
    {FILTERS}
  </defs>

  {BACKGROUND}
  {DECORATIVE_ELEMENTS}
  {TEXT}
  {ACCENT_LINES}
  {CORNER_ACCENTS}
</svg>
```

**All templates use these text positions:**
- Name: `x="600" y="120"`, `font-size="52"`, `font-weight="700"`, `text-anchor="middle"`
- Role: `x="600" y="160"`, `font-size="18"`, `font-weight="400"`, `text-anchor="middle"`, `letter-spacing="4"`
- Tagline: `x="600" y="215"`, `font-size="15"`, `text-anchor="middle"`, `letter-spacing="1"`

**Font stacks:**
- Name: `'Segoe UI', 'Helvetica Neue', Arial, sans-serif`
- Role: `'JetBrains Mono', 'SF Mono', 'Fira Code', monospace`
- Tagline: `'Segoe UI', 'Helvetica Neue', Arial, sans-serif`

---

## Template: `github-dark`

**Feel:** Clean, professional, the GitHub native look.

- Background: linear gradient `bg → bg-secondary → bg`
- Grid: 40px squares, `border` color at opacity 0.4
- Glow: single green radial at 75% x, 40% y, radius 35%, accent at opacity 0.15
- Secondary glow: blue radial at 25% x, 60% y, radius 30%, accent-blue at opacity 0.08
- Particles: 8 circles, accent color, radius 0.8-1.5, opacity 0.3-0.6
- Accent line: horizontal at y=175, x=350→850, accent at opacity 0.4
- Bottom border: gradient line at y=270, x=200→1000, accent fading to transparent
- Corner accents: 4 L-shaped brackets, accent at opacity 0.3

---

## Template: `midnight`

**Feel:** Deep space, electric blue energy.

- Background: linear gradient `#0a0e1a → #111633 → #0a0e1a`
- Grid: 50px squares, `#1e2544` at opacity 0.3 (wider, more spacious)
- Glow: large blue radial at center, `#4f8ff7` at opacity 0.12
- Secondary glow: purple radial offset right, `#a78bfa` at opacity 0.06
- Particles: 10 circles, mix of blue `#4f8ff7` and purple `#a78bfa`, radius 1-2
- No accent line — use a subtle horizontal gradient bar instead (2px height, blue→purple→blue)
- Corner accents: dots instead of brackets (small circles at corners)

---

## Template: `aurora`

**Feel:** Northern lights, nature meets tech.

- Background: linear gradient `#0b0f19 → #111827 → #0b0f19`
- Grid: none (clean, natural feel)
- Glow: green radial at 30% x, `#22c55e` at opacity 0.15
- Secondary glow: purple radial at 70% x, `#a855f7` at opacity 0.10
- Tertiary glow: cyan accent at top center, `#38bdf8` at opacity 0.05
- Particles: 6 circles, alternating green and purple
- Aurora band: a subtle curved path with green→purple gradient at opacity 0.08, sweeping across upper third
- Bottom border: gradient line, green→purple

---

## Template: `cyberpunk`

**Feel:** Neon city, high contrast, Blade Runner vibes.

- Background: solid `#0a0a0a` (no gradient — stark)
- Grid: 30px squares, `#2d2d44` at opacity 0.5 (denser grid, more digital)
- Glow: neon pink radial at center, `#ff2d75` at opacity 0.10
- Secondary glow: cyan radial offset, `#00f5ff` at opacity 0.08
- Text glow filter: stronger `feGaussianBlur` (stdDeviation 3), pink flood
- Particles: 12 circles (more particles = more digital), pink and cyan mix
- Horizontal scan lines: thin horizontal lines every 4px at opacity 0.03 (CRT effect)
- Accent line: double lines (pink and cyan, 1px apart) at y=175
- Corner accents: sharper, 2px stroke, pink color

---

## Template: `minimal-light`

**Feel:** Apple.com restraint. White space is the design.

- Background: solid `#ffffff`
- Grid: none
- Glow: none
- Particles: none
- No filters
- Name: `#1f2328`, sans-serif (not monospace for role either — use sans-serif throughout)
- Role: `#0969da` accent color, normal weight (not bold), regular case (not UPPERCASE)
- Tagline: `#656d76`
- Single thin line at y=260, x=300→900, `#d0d7de`
- No corner accents

---

## Template: `sunset`

**Feel:** Golden hour, warm and inviting.

- Background: radial gradient from center `#2d1b18 → #1a1110`
- Grid: none (organic, not technical)
- Glow: warm amber radial at center, `#f59e0b` at opacity 0.12
- Secondary glow: red radial at bottom-right, `#ef4444` at opacity 0.06
- Particles: 6 circles, amber color, larger radius (1.5-2.5), lower opacity (0.2-0.4) — feels like embers
- Role text color: `#f59e0b` amber
- Bottom border: amber→red→amber gradient

---

## Template: `ocean`

**Feel:** Deep water, bioluminescent calm.

- Background: linear gradient `#0c1222 → #132040 → #0c1222`
- Grid: 45px squares, `#1e3a5f` at opacity 0.25 (subtle)
- Glow: teal radial at center-bottom, `#06b6d4` at opacity 0.10
- Secondary glow: blue radial at top-left, `#3b82f6` at opacity 0.06
- Particles: 8 circles, teal `#06b6d4`, varying sizes — like bioluminescent plankton
- Wave-like decorative path at bottom (subtle sine wave, teal at opacity 0.1)
- Bottom border: teal gradient line

---

## Template: `monochrome`

**Feel:** Architectural drawing, Swiss design.

- Background: solid `#000000`
- Grid: 40px squares, `#333333` at opacity 0.6 (prominent grid is the design)
- Glow: none
- Particles: none
- Name: `#ffffff`, slightly larger (`font-size="58"`)
- Role: `#888888` (not white — gray for hierarchy)
- Tagline: `#666666`
- No accent lines
- Corner accents: white, opacity 0.5 (more visible against black)

---

## Writing the About Me Section

The About Me bullets are the most human part of the profile. They should NOT read like a resume or LinkedIn summary.

**Rules:**
1. Lead with what the person *builds*, not what they *are*
2. Use specific, concrete language — "I build real-time payment systems" not "I'm passionate about fintech"
3. Include a "currently" or "obsessed with" line that shows momentum
4. Reference actual repos or technologies detected, not generic skills
5. Max 4 bullets, min 2
6. Use `**bold**` for 1-2 key phrases per bullet

**Good examples:**
- "I build **distributed systems** that process millions of events/sec — and the **AI agents** that help ship them faster."
- "Currently deep in **agentic software development** — where AI doesn't just suggest code, it drives the entire SDLC."
- "Open-sourcing the **developer tools** I wish existed when I started."
- "By day: **cloud architecture** at scale. By night: making AI agents that can do my day job."

**Bad examples (avoid):**
- "Passionate about coding and technology" (generic)
- "15 years of experience in Java" (resume line)
- "Senior Software Engineer at Company X" (LinkedIn)
- "I love learning new things" (everyone says this)
- "Full-stack developer who enjoys solving problems" (meaningless)
