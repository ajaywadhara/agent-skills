# Contributing to Agent Skills

Thank you for your interest in contributing! This guide will help you get started.

## Ways to Contribute

### 1. Report Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/ajaywadhara/agent-skills/issues/new) with:

- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Which skill is affected

### 2. Improve Existing Skills

- Fix typos or unclear instructions
- Add missing examples
- Update outdated references
- Improve trigger phrase coverage

### 3. Submit New Skills

Have a skill idea? We'd love to see it!

## Creating a New Skill

### Step 1: Check If It Already Exists

Search existing skills and issues to avoid duplicates.

### Step 2: Follow the Specification

Your skill must follow the [Agent Skills Specification](https://agentskills.io/specification):

```
your-skill/
├── SKILL.md              # Required
├── references/           # Optional
└── scripts/              # Optional
```

### Step 3: Use the Template

```markdown
---
name: your-skill-name
description: Clear description of what this skill does and when to use it. Include keywords that help AI identify when to activate this skill.
license: MIT
metadata:
  author: Your Name
  version: "1.0"
  category: your-category
---

# Skill Title

Clear instructions for the AI assistant.

## When to Use

- Trigger phrase 1
- Trigger phrase 2

## Instructions

Step-by-step guidance...

## Examples

Show input/output examples...
```

### Step 4: Validate Your Skill

```bash
npx skills-ref validate ./your-skill
```

### Step 5: Test Locally

1. Copy your skill to `.claude/skills/`
2. Test with various prompts
3. Verify it activates correctly
4. Check that instructions produce good results

## Submitting Changes

### For Small Changes (Typos, Minor Fixes)

1. Fork the repository
2. Make your changes
3. Submit a Pull Request

### For New Skills or Major Changes

1. **Open an issue first** to discuss your idea
2. Fork the repository
3. Create a feature branch: `git checkout -b skill/your-skill-name`
4. Add your skill following the structure
5. Test thoroughly
6. Submit a Pull Request

## Pull Request Guidelines

### Title Format

```
Add: new-skill-name
Fix: issue description in existing-skill
Update: what was updated in skill-name
```

### PR Description

Include:
- What the skill does
- Why it's useful
- How you tested it
- Any limitations or known issues

### Checklist

- [ ] Follows the Agent Skills Specification
- [ ] SKILL.md has valid frontmatter
- [ ] Name uses lowercase and hyphens only
- [ ] Description is clear and includes trigger keywords
- [ ] Tested with AI assistant
- [ ] No sensitive information included

## Code of Conduct

- Be respectful and constructive
- Help others learn
- Give credit where due
- Keep discussions focused

## Questions?

Open an issue with the `question` label or reach out to the maintainers.

---

Thank you for helping make Agent Skills better!
