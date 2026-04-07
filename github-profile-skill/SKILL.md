---
name: github-profile
description: "Create a standout GitHub profile README from scratch. Pulls real data from GitHub, asks style preferences, generates animated header, tech stack, project showcase, stats, and snake animation. Use when user says 'create github profile', 'improve my github', 'make my github look good', 'github readme', or 'profile readme'."
license: MIT
metadata:
  author: Ajay Wadhara
  version: "1.0"
  category: developer-branding
---

# GitHub Profile README Generator

Generate a visually polished, personalized GitHub profile README with real data, animated elements, and a theme the user picks.

## Prerequisites Check

Before anything, verify the environment:

```bash
gh auth status
```

If not authenticated, tell the user:
> You need the GitHub CLI authenticated. Run `! gh auth login` to connect your account.

**Do NOT proceed until `gh auth status` succeeds.**

## Workflow

```
- [ ] Step 1: Gather GitHub data
- [ ] Step 2: Ask style questions
- [ ] Step 3: Generate profile README
- [ ] Step 4: Create repo + GitHub Actions
- [ ] Step 5: Push and verify
```

### Step 1: Gather GitHub Data

Pull everything about the user from the GitHub API. Run these in parallel:

```bash
# Get username from auth
gh api user --jq '.login'

# Get profile info
gh api user --jq '{name: .name, bio: .bio, company: .company, blog: .blog, location: .location, public_repos: .public_repos, followers: .followers, following: .following, created_at: .created_at}'

# Get repos sorted by stars (top 20)
gh repo list USERNAME --limit 20 --json name,description,primaryLanguage,stargazerCount,forkCount,isPrivate,url --jq 'sort_by(-.stargazerCount)'

# Get contribution count
gh api graphql -f query='query { user(login: "USERNAME") { contributionsCollection { contributionCalendar { totalContributions } } } }' --jq '.data.user.contributionsCollection.contributionCalendar.totalContributions'
```

From this data, extract:
- **Username** (exact casing)
- **Display name** (or fall back to username)
- **Bio / tagline**
- **Location**
- **Top languages** (aggregate from repos)
- **Top repos** (by stars, excluding forks where isPrivate=false)
- **Total contributions** this year
- **Account age** (years since created_at)
- **Blog / website URL** (if present)
- **Company** (if present)

### Step 2: Ask Style Questions

Present a short interactive menu. Ask ONE message with ALL questions:

---

**I've pulled your GitHub data. Let me personalize your profile:**

1. **How would you describe yourself?** (e.g., "Software Engineer", "Full-Stack Developer", "ML Researcher", or a custom tagline)

2. **Pick a theme** (see [references/themes.md](references/themes.md) for full catalog):
   - `github-dark` — GitHub's native dark palette, green accents (clean, default)
   - `midnight` — Deep navy + electric blue glow (modern, sleek)
   - `aurora` — Dark base + shifting green/purple aurora (atmospheric)
   - `cyberpunk` — Black + neon pink/cyan (bold, edgy)
   - `minimal-light` — White + black type + single accent color (clean, Apple-like)
   - `sunset` — Warm dark + orange/amber gradients (inviting, warm)
   - `ocean` — Deep blue + teal accents (calm, professional)
   - `monochrome` — Pure black/white/gray, no color (stark, editorial)

3. **What do you want highlighted?** Pick up to 3:
   - Open-source projects
   - Tech stack / skills
   - Current work / focus areas
   - Stats & contribution streaks
   - Blog / writing
   - Social links

4. **Any specific technologies you want featured?** (I'll auto-detect from your repos, but you can override)

5. **Animated snake eating your contribution graph?** (yes/no — requires GitHub Action, runs daily)

---

Wait for user answers before proceeding.

### Step 3: Generate Profile README

Build the README using the selected theme and data. See [references/components.md](references/components.md) for all available components and [references/hero-templates.md](references/hero-templates.md) for hero section options.

**Structure (top to bottom):**

1. **Hero section** — Custom animated SVG header with name + role. The SVG must be committed to the repo as `header.svg`. Use the theme's color palette. Include: subtle grid pattern overlay, floating animated particles (using SMIL `<animate>`), clean sans-serif name, monospace role subtitle, thematic glow orbs, corner bracket accents.
   - **IMPORTANT**: GitHub sanitizes SVG animations from repo files. The SVG will render as a static image. This is fine — design it so it looks great static. The typing-svg below provides the motion.

2. **Typing animation** — Use `readme-typing-svg.demolab.com`. Cycle 2-3 short phrases that capture the user's focus areas. Style as terminal commands (`$ building distributed systems →`).

3. **Social badges** — `flat-square` style from shields.io. Only include links the user actually has (GitHub followers, LinkedIn, blog, Twitter/X, location).

4. **About Me** — 2-4 bullet points. Write these with personality — not a resume, not a bio. Make them memorable. Use **bold** for key phrases. Reference what the user actually builds based on their repos, not generic platitudes.

5. **Tech Stack** — Use `skillicons.dev` icon rows (max 3 rows of 6). Auto-detect from repo languages, let user override. Group by: Languages & Frameworks → Cloud & Infrastructure → Tools.

6. **Project Showcase** — Markdown table (2 columns, up to 3 rows = 6 projects max). Each cell: linked project name with shields.io star/fork badges + 1-line description. Pick the user's most starred/forked public repos. If descriptions are missing, write concise ones from the repo content.

7. **GitHub Stats** — Streak stats from `github-readme-streak-stats.herokuapp.com` using the theme's palette.

8. **Contribution Graph** — Activity graph from `github-readme-activity-graph.vercel.app`. Use `<picture>` tag with dark/light source variants.

9. **Snake Animation** (if opted in) — Reference the SVG from the `output` branch. Set up GitHub Action in Step 4.

10. **Footer** — Profile view counter from `komarev.com/ghpvc`. Optionally a quote in a code block (make it relevant to the user's domain, not generic inspiration).

**Component rules:**
- Every external image service must use the theme's color values for consistency
- Use `<div align="center">` for centered sections
- Use `<br/>` for spacing, not empty lines (more reliable on GitHub)
- Use `<picture>` with `prefers-color-scheme` sources where supported
- All shields.io badges: `style=flat-square`, `labelColor` = theme background, `color` = theme accent
- Do NOT use `github-readme-stats.vercel.app/api/pin` — rate-limited, images break constantly
- Do NOT use `github-profile-trophy.vercel.app` — same rate-limit problem
- Profile README should be under 300 lines

### Step 4: Create Repo + GitHub Actions

**Create the profile repo:**

```bash
# Check if repo exists
gh repo view USERNAME/USERNAME 2>&1

# If not found, create it
gh repo create USERNAME --public --description "GitHub profile README"
```

**Clone, write files, set up actions:**

```bash
# Clone to /tmp
cd /tmp && git clone https://github.com/USERNAME/USERNAME.git

# Write README.md and header.svg
# (use Write tool)

# If snake animation opted in, create the workflow:
mkdir -p /tmp/USERNAME/.github/workflows
```

**Snake workflow** (`.github/workflows/snake.yml`):

```yaml
name: Generate Snake Animation
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
jobs:
  generate:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Generate snake game from contribution graph
        uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark
      - name: Push to output branch
        uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Step 5: Push and Verify

**IMPORTANT**: Before pushing, ask the user for confirmation:

> Ready to push your new profile to GitHub. Want me to go ahead?

Only push after explicit "yes."

```bash
cd /tmp/USERNAME
git add -A
git commit -m "Add profile README"
git branch -M main
git push -u origin main
```

If snake animation is enabled, trigger the workflow:

```bash
gh workflow run snake.yml --repo USERNAME/USERNAME
```

After push, tell the user:
1. Visit `github.com/USERNAME` to see the profile
2. If they see the "Share to Profile" banner on the repo page, click it
3. Snake animation takes ~2 minutes to generate on first run
4. The snake workflow runs daily at midnight UTC to stay current

## Theme Application

When applying a theme, use the color values from [references/themes.md](references/themes.md) consistently across ALL components:
- Header SVG background, text, accents
- Typing SVG `color` parameter
- All shields.io `labelColor` and `color` parameters
- Streak stats `background`, `border`, `ring`, `fire`, label colors
- Activity graph `bg_color`, `color`, `line`, `point`, `area_color`
- Snake animation variant (dark/light)
- Komarev counter colors

## References

- [Theme catalog](references/themes.md) — 8 themes with full hex values
- [Component guide](references/components.md) — All available widgets with integration URLs
- [Hero templates](references/hero-templates.md) — SVG header templates for each theme
