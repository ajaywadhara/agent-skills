# Claude Code — Subagent Starter Pack

Five ready-to-use [Claude Code](https://code.claude.com) subagents you can drop into any project — frontend or backend. Each one does a noisy, self-contained job in its **own context window**, so your main session stays sharp instead of filling up with logs, diffs, and file dumps.

> Companion to my video on Claude Code subagents (link in the description). The video builds `doc-writer` from scratch and explains *what* subagents are, *where* to use them, and *how* to make your own.

## What's inside

| Agent | What it does | Model | Tools | Touches your files? |
|---|---|---|---|---|
| `doc-writer` | Writes / updates docs — Javadoc, JSDoc/TSDoc, Python docstrings, README | Haiku | Read, Write, Edit, Glob, Grep | Docs only |
| `code-reviewer` | Reviews code for bugs, security, readability — ranked findings | Sonnet | Read, Glob, Grep | **No (read-only)** |
| `commit-writer` | Writes a Conventional Commits message from your staged diff | Haiku | Bash (read-only git) | **No (won't commit)** |
| `test-writer` | Writes unit tests in your framework and runs them | Sonnet | Read, Write, Edit, Glob, Grep, Bash | Test files |
| `a11y-checker` | Audits frontend code for accessibility issues | Sonnet | Read, Glob, Grep | **No (read-only)** |

## Install

**Per project** (recommended — commit them so your whole team gets the same agents):

```bash
# from your project root
mkdir -p .claude/agents
cp doc-writer.md code-reviewer.md commit-writer.md test-writer.md a11y-checker.md .claude/agents/
```

**For every project** (just you): copy them into `~/.claude/agents/` instead.

> ⚠️ Subagent files added on disk require a session restart to load — restart Claude Code after copying.
> (Agents created with the `/agents` command load immediately; only on-disk files need a restart.)

## Use

Ask in plain English — Claude will delegate to the right agent, or you can name it directly:

- `run doc-writer on the files I changed`
- `use code-reviewer on src/auth/`
- `commit-writer` &nbsp;*(after `git add`)*
- `write tests for src/auth/token.ts with test-writer`
- `run a11y-checker on components/Nav.tsx`

## Make them yours

Each file is just YAML frontmatter (`name`, `description`, `model`, `tools`) plus a system prompt written as **When to use → Rules → Final checklist** — a small structure that keeps an agent predictable. Change the `model`, tighten the `tools`, or edit the instructions to fit your stack. The fastest way to create your own from scratch is the `/agents` command.

## A note on safety

`commit-writer` and `test-writer` can run shell commands (the `Bash` tool). Claude Code's `tools` field is all-or-nothing per tool — it can't limit *which* commands run — so their guardrails (e.g. "read-only git, never commit") live in the system prompt, not a sandbox. In practice that's reliable and the worst case is a change you can undo, but if you want *hard* enforcement (block any `git commit`, allow only `SELECT`, etc.) that's a `PreToolUse` hook, not the `tools` field. The other agents can't run shell at all — `code-reviewer` and `a11y-checker` are strictly read-only, and `doc-writer` can write docs but has no shell access.

## License

[MIT](./LICENSE). Free to use, modify, and redistribute. The agents' prompt *structure* was inspired by open-source collections of engineering rules distilled from classic software books (also MIT-licensed); the prompts here are original reimplementations as Claude Code subagents.
