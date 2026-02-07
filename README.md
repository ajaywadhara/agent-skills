# Agent Skills Collection

[![GitHub Stars](https://img.shields.io/github/stars/ajaywadhara/agent-skills?style=social)](https://github.com/ajaywadhara/agent-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Skills](https://img.shields.io/badge/skills.sh-available-blue)](https://skills.sh)

A curated collection of custom skills that extend AI coding assistants like **Claude Code**, **GitHub Copilot**, **Cursor**, **Cline**, and other AI agents.

> **If you find these skills useful, please consider giving this repo a star!** It helps others discover these tools and motivates continued development.

## Quick Start

Get up and running in 30 seconds:

```bash
# Install with one command
npx skills add ajaywadhara/agent-skills

# Or manually clone
git clone https://github.com/ajaywadhara/agent-skills.git
cp -r agent-skills/*-skill .claude/skills/
```

Then just ask your AI assistant: *"Review my code"*, *"Design a notification service"*, or *"Help me migrate to Spring Boot 4"*

---

## What Are Agent Skills?

Agent Skills are **reusable capabilities** that teach AI assistants how to perform specific tasks. Think of them as instruction manuals that help AI understand specialized workflows, best practices, and domain knowledge.

**Without skills:** AI assistants rely only on their general training.

**With skills:** AI assistants gain expert-level knowledge for specific tasks like code review, API design, or framework migrations.

## Why Use These Skills?

| Benefit | Description |
|---------|-------------|
| **Save Hours** | Skip the research - skills contain battle-tested patterns and checklists |
| **Catch Bugs Early** | Find issues before code review, not during |
| **Best Practices Built-In** | Industry standards baked into every skill |
| **Works Everywhere** | Compatible with Claude Code, Cursor, Cline, and more |
| **Always Up-to-Date** | Community-maintained and regularly updated |
| **Free & Open Source** | MIT licensed - use, modify, and share freely |

---

## Available Skills

| Skill | Description | Use When You Want To... |
|-------|-------------|------------------------|
| **[pr-guardian](pr-guardian-skill/)** | Pre-PR code review and bug detection | Review code before creating a pull request, find bugs, check security |
| **[openapi-architect](openapi-architect-skill/)** | REST API design and OpenAPI specs | Design APIs, create OpenAPI specifications, follow best practices |
| **[spring-boot-4-migration](spring-boot-4-migration-skill/)** | Spring Boot 3.x to 4.x migration | Upgrade Spring Boot, migrate Jackson, update tests |
| **[design-doc](design-doc-skill/)** | Engineering design docs with Mermaid diagrams | Create architecture docs, design systems, document decisions |

---

## I Have a Vague Idea — How Does This Help Me?

You don't need to be an expert. These skills turn **minimal input into expert-level output**. Here's what that looks like in practice:

### Scenario 1: "I need to build a notification service"

That's it. That's all you type. The **design-doc** skill takes that one sentence and produces:

- A complete design document with problem statement, goals, and non-goals
- C4 architecture diagrams showing how the service fits into your ecosystem
- An entity relationship diagram for the data model
- Sequence diagrams for key flows (sending notifications, handling failures)
- A decision log explaining *why* certain choices were made
- Security considerations, risk analysis, and open questions

**You provide:** 1 sentence. **You get:** A 5-10 page engineering design document with 3-5 Mermaid diagrams, ready for team review.

### Scenario 2: "Review my code"

You've written some Java code and want to make sure it's solid before creating a PR. Just say those three words. The **pr-guardian** skill:

- Detects your uncommitted changes or compares your branch
- Scans for 30+ bug patterns (null safety, SQL injection, resource leaks)
- Runs a full OWASP security checklist
- Calculates a risk score (1-10) for your changes
- Generates a detailed report with exact fixes for every issue found
- Offers to **automatically apply the fixes** for you

**You provide:** "Review my code." **You get:** A full code review with actionable fixes, as if a senior engineer spent 30 minutes on your PR.

### Scenario 3: "I need an API for managing users"

That's enough for the **openapi-architect** skill. It produces:

- A complete OpenAPI 3.1 specification with all CRUD endpoints
- Proper error handling following RFC 7807
- Pagination, filtering, and sorting
- Authentication/authorization schemes
- Correct HTTP status codes and headers

**You provide:** A rough idea. **You get:** A production-ready API spec following industry standards.

### Scenario 4: "Migrate to Spring Boot 4"

Your project is on Spring Boot 3.x and you want to upgrade. The **spring-boot-4-migration** skill:

- Walks you through 10 migration phases in order
- Tells you exactly which dependencies, properties, and APIs changed
- Covers Jackson 3, Spring Security 7, Spring Framework 7, and more
- Provides a verification script to validate your migration

**You provide:** "Migrate to Spring Boot 4." **You get:** A step-by-step migration guide tailored to your codebase.

---

> **The pattern is simple:** You bring the *what*, these skills bring the *how*. The less you know about best practices, the more value you get — because every skill encodes expert knowledge that would otherwise take hours to research.

---

## Installation Guide

### Option 1: Using skills.sh (Recommended)

The easiest way to install skills using the [skills.sh](https://skills.sh) CLI:

```bash
# Install skills CLI (if not already installed)
npm install -g skills

# Install all skills from this repository
npx skills add ajaywadhara/agent-skills

# Or install a specific skill
npx skills add ajaywadhara/agent-skills/pr-guardian-skill
npx skills add ajaywadhara/agent-skills/openapi-architect-skill
npx skills add ajaywadhara/agent-skills/spring-boot-4-migration-skill
npx skills add ajaywadhara/agent-skills/design-doc-skill
```

### Option 2: Manual Installation (Claude Code)

For Claude Code users, you can manually add skills to your project:

#### Project-Level Installation (Recommended)

1. Create a `.claude/skills/` directory in your project root:

```bash
mkdir -p .claude/skills
```

2. Clone or copy the skill folder into your project:

```bash
# Clone the entire repository
git clone https://github.com/ajaywadhara/agent-skills.git

# Copy the skill(s) you want
cp -r agent-skills/pr-guardian-skill .claude/skills/
cp -r agent-skills/openapi-architect-skill .claude/skills/
cp -r agent-skills/spring-boot-4-migration-skill .claude/skills/
cp -r agent-skills/design-doc-skill .claude/skills/
```

3. Your project structure should look like:

```
your-project/
├── .claude/
│   └── skills/
│       ├── pr-guardian-skill/
│       │   └── SKILL.md
│       ├── openapi-architect-skill/
│       │   └── SKILL.md
│       ├── spring-boot-4-migration-skill/
│       │   └── SKILL.md
│       └── design-doc-skill/
│           └── SKILL.md
├── src/
└── ...
```

#### User-Level Installation (Available Across All Projects)

Install skills globally so they're available in all your projects:

```bash
# Create user-level skills directory
mkdir -p ~/.claude/skills

# Copy skills
cp -r agent-skills/pr-guardian-skill ~/.claude/skills/
```

### Option 3: Git Submodule

Add this repository as a submodule to keep skills updated:

```bash
# Add as submodule
git submodule add https://github.com/ajaywadhara/agent-skills.git .claude/agent-skills

# Update skills when new versions are released
git submodule update --remote
```

### Option 4: Direct Download

1. Go to the [GitHub releases page](https://github.com/ajaywadhara/agent-skills/releases)
2. Download the ZIP file
3. Extract and copy skill folders to `.claude/skills/` or `~/.claude/skills/`

---

## How to Use Skills

Once installed, skills activate automatically when you use trigger phrases with your AI assistant.

### pr-guardian Examples

```
"Review my code"
"Review my branch against develop"
"Find bugs in UserService.java"
"Check for security issues"
"Is this code ready for PR?"
```

### openapi-architect Examples

```
"Design an API for user management"
"Create an OpenAPI spec for a payment service"
"Review my API design"
"What status code should I use for validation errors?"
```

### design-doc Examples

```
"Design a notification service"
"Create a design doc for user authentication"
"Architect an event-driven order system"
"How should I design a caching layer?"
```

### spring-boot-4-migration Examples

```
"Migrate to Spring Boot 4"
"Help me update Jackson to version 3"
"What changed in Spring Security 7?"
"Update my tests for Spring Boot 4"
```

---

## Publishing Your Skills

Want to share your skills with the community? Here's how:

### 1. List on skills.sh

[skills.sh](https://skills.sh) automatically indexes skills from public GitHub repositories.

**Steps:**

1. Create a public GitHub repository with your skill(s)
2. Ensure each skill has a valid `SKILL.md` file following the [Agent Skills Specification](https://agentskills.io/specification)
3. Your skills will be discoverable via:
   ```bash
   npx skills add your-username/your-repo
   ```

**Validation:** Use the official validator before publishing:

```bash
npx skills-ref validate ./your-skill-directory
```

### 2. Submit to Community Directories

| Platform | How to Submit |
|----------|---------------|
| [skills.sh](https://skills.sh) | Automatic - just have a public GitHub repo |
| [agentskills.io](https://agentskills.io) | Follow the [specification](https://agentskills.io/specification) |
| [Anthropic Community](https://github.com/anthropics/claude-code) | Open an issue or PR with your skill |

### 3. Share on Social Media

Use these hashtags to help others find your skills:

- `#AgentSkills`
- `#ClaudeCode`
- `#AISkills`
- `#CodingAssistant`

---

## Creating Your Own Skills

### Quick Start

1. Create a new directory:

```bash
mkdir my-awesome-skill
cd my-awesome-skill
```

2. Create a `SKILL.md` file:

```markdown
---
name: my-awesome-skill
description: Describe what your skill does and when AI should use it. Include keywords that help trigger the skill.
license: MIT
metadata:
  author: Your Name
  version: "1.0"
---

# My Awesome Skill

Instructions for the AI assistant go here...

## When to Use This Skill

- Trigger phrase 1
- Trigger phrase 2

## Step-by-Step Instructions

1. First, do this...
2. Then, do that...

## Examples

Input: "Example user request"
Output: What the AI should do
```

### Skill Structure

```
my-skill/
├── SKILL.md              # Required - Main instructions
├── references/           # Optional - Detailed documentation
│   ├── patterns.md
│   └── examples.md
├── scripts/              # Optional - Automation scripts
│   └── validate.sh
└── assets/               # Optional - Templates, images, etc.
    └── template.json
```

### Validation Requirements

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Lowercase, hyphens only, 1-64 chars |
| `description` | Yes | 1-1024 chars, explain what & when |
| `license` | No | MIT, Apache-2.0, etc. |
| `metadata` | No | author, version, custom fields |

### Best Practices

1. **Keep SKILL.md under 500 lines** - Move details to `references/`
2. **Use clear trigger phrases** - Help AI know when to activate
3. **Include examples** - Show expected inputs and outputs
4. **Test thoroughly** - Try various prompts with your skill

---

## Frequently Asked Questions

### Do I need to install anything?

For skills.sh: Just `npx skills add` works without global installation.

For manual installation: No additional software needed, just copy files.

### Will skills work with my AI assistant?

Skills work with any AI assistant that supports the Agent Skills format:
- Claude Code
- Cursor
- Cline
- GitHub Copilot (with extensions)
- Other compatible AI coding tools

### How do I update skills?

```bash
# Using skills.sh
npx skills update

# Using git submodule
git submodule update --remote

# Manual: Re-download and replace files
```

### Can I modify skills for my needs?

Yes! Skills are just Markdown files. Feel free to:
- Adjust instructions for your workflow
- Add company-specific guidelines
- Remove sections you don't need
- Combine multiple skills

### How do I report issues or suggest improvements?

Open an issue on our [GitHub repository](https://github.com/ajaywadhara/agent-skills/issues).

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick contribution ideas:**
- Report bugs or issues
- Suggest new skills
- Improve documentation
- Share your custom skills

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

Individual skills may have their own licenses specified in their `SKILL.md` files.

---

## Support This Project

If these skills have helped you, here are some ways to show your support:

### Give a Star

The easiest way to support this project is to **star it on GitHub**. Stars help others discover these skills and show that the community finds them valuable.

[![Star this repo](https://img.shields.io/github/stars/ajaywadhara/agent-skills?style=for-the-badge&logo=github&label=Star%20This%20Repo)](https://github.com/ajaywadhara/agent-skills)

### Spread the Word

Help others discover these skills:

- **Tweet about it:** Share your experience using these skills
- **Write a blog post:** Tutorial on how you use these skills in your workflow
- **Tell your team:** Share with colleagues who might benefit
- **Mention in talks:** Reference in conference talks or meetups

**Sample tweet:**
> Just discovered Agent Skills for @AnthropicAI Claude Code - the pr-guardian skill caught 3 bugs before my code review! Check it out: github.com/ajaywadhara/agent-skills #ClaudeCode #AgentSkills #DeveloperTools

### Share on Social Media

| Platform | Action |
|----------|--------|
| **Twitter/X** | [Tweet about Agent Skills](https://twitter.com/intent/tweet?text=Check%20out%20these%20awesome%20Agent%20Skills%20for%20Claude%20Code%20and%20other%20AI%20assistants!%20%F0%9F%9A%80&url=https://github.com/ajaywadhara/agent-skills&hashtags=ClaudeCode,AgentSkills,AI,DeveloperTools) |
| **LinkedIn** | [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/ajaywadhara/agent-skills) |
| **Reddit** | Share in r/programming, r/ClaudeAI, or r/MachineLearning |
| **Hacker News** | Submit to Show HN |
| **Dev.to** | Write about your experience |

### Contribute

- Report bugs and suggest features
- Submit new skills
- Improve documentation
- Help answer questions in issues

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Stay Updated

Watch this repository to get notified about:
- New skills added
- Major updates to existing skills
- Bug fixes and improvements

[![Watch](https://img.shields.io/github/watchers/ajaywadhara/agent-skills?style=social)](https://github.com/ajaywadhara/agent-skills/subscription)

---

## Star History

If you find this project useful, please star it! Here's how the community has grown:

[![Star History Chart](https://api.star-history.com/svg?repos=ajaywadhara/agent-skills&type=Date)](https://star-history.com/#ajaywadhara/agent-skills&Date)

---

## Author

**Ajay Wadhara**

- GitHub: [@ajaywadhara](https://github.com/ajaywadhara)
- Twitter: [@ajaywadhara](https://twitter.com/ajaywadhara)

Have questions? Feel free to [open an issue](https://github.com/ajaywadhara/agent-skills/issues) or reach out!

---

## Resources

- [Agent Skills Specification](https://agentskills.io/specification) - Official format specification
- [skills.sh](https://skills.sh) - Skills directory and CLI
- [Claude Code Documentation](https://docs.anthropic.com/claude-code) - Claude Code official docs

---

## Show Your Support

```
If this project helped you, please consider:

  1. Starring this repository
  2. Sharing it with friends and colleagues
  3. Contributing your own skills

Every star, share, and contribution helps grow this community!
```

---

Made with care by [Ajay Wadhara](https://github.com/ajaywadhara)
