# github-profile

Create a standout GitHub profile README in minutes. Pulls real data from your GitHub account, lets you pick a visual theme, and generates everything — animated header, tech stack icons, project showcase, contribution stats, and snake animation.

## What It Does

1. **Connects to your GitHub** via the `gh` CLI — pulls your repos, languages, stars, bio, and contribution data
2. **Asks your preferences** — role title, visual theme (8 options), what to highlight
3. **Generates a complete profile** — custom SVG header, skill icons, project table, streak stats, activity graph, and optional snake animation
4. **Creates the repo and pushes** — sets up the special `username/username` repo, GitHub Actions, and deploys

## Install

```bash
npx @anthropic-ai/agent-skills add ajaywadhara/agent-skills/github-profile-skill
```

Or manually copy the `github-profile-skill/` directory into your `.claude/skills/` folder.

## Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated (`gh auth login`)
- Git configured with push access to your GitHub account

## Usage

```
/github-profile
```

Or just say:
- "Create a GitHub profile for me"
- "Make my GitHub look good"
- "Improve my GitHub profile"

## Themes

| Theme | Vibe |
|-------|------|
| `github-dark` | GitHub's native dark palette, green accents — clean default |
| `midnight` | Deep navy + electric blue — modern, premium |
| `aurora` | Dark + green/purple northern lights — atmospheric |
| `cyberpunk` | Black + neon pink/cyan — bold, futuristic |
| `minimal-light` | White + black + single accent — Apple-like restraint |
| `sunset` | Warm dark + orange/amber — inviting, approachable |
| `ocean` | Deep blue + teal — calm, professional |
| `monochrome` | Pure black/white/gray — stark, editorial |

## What Gets Generated

```
username/
├── README.md              # The profile README
├── header.svg             # Custom animated SVG header
└── .github/
    └── workflows/
        └── snake.yml      # Daily snake animation (optional)
```

## Components Used

| Component | Source | Reliability |
|-----------|--------|-------------|
| Header | Custom SVG (self-hosted) | Self-hosted |
| Typing animation | readme-typing-svg.demolab.com | Good |
| Tech stack icons | skillicons.dev | Excellent |
| Badges | shields.io | Excellent |
| Streak stats | github-readme-streak-stats.herokuapp.com | Good |
| Activity graph | github-readme-activity-graph.vercel.app | Good |
| Snake animation | Platane/snk via GitHub Action | Self-hosted |
| View counter | komarev.com | Excellent |

Services known to be unreliable (github-readme-stats pin cards, github-profile-trophy) are intentionally excluded.

## License

MIT
