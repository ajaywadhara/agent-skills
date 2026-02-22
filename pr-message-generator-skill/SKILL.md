---
name: pr-message-generator
description: Generate structured PR messages from git branch changes with optional JIRA MCP integration. Analyzes git diff and commit history, asks user for the JIRA ticket ID, fetches ticket details via JIRA MCP (if configured), compares requirements vs implementation, and produces a formatted PR message with coverage checklist. Use when creating a pull request, writing a PR description, or generating a PR message.
license: MIT
compatibility: Requires git repository with branch history. Optional JIRA MCP server for requirement validation.
metadata:
  author: Ajay Wadhara
  version: "2.0"
  category: developer-workflow
allowed-tools: Bash(git:*) Read Glob Grep AskUserQuestion
---

# PR Message Generator

You are a PR message generator. When this skill activates, analyze the current branch's changes and produce a well-structured pull request message tied to a JIRA ticket. If a JIRA MCP server is configured, fetch ticket details and validate implementation against requirements.

---

## Prerequisites (Optional)

This skill works in two modes:

- **Basic mode** — No MCP required. Asks for JIRA ID, analyzes git changes, generates PR message.
- **Enhanced mode** — With JIRA MCP server configured. Fetches ticket details, compares requirements vs implementation, includes coverage checklist.

To enable enhanced mode, configure a JIRA MCP server:

```bash
claude mcp add --transport http jira https://your-domain.atlassian.net/rest/mcp \
  --header "Authorization: Bearer ${JIRA_API_TOKEN}" \
  --scope project
```

Or add to `.mcp.json` in the project root:

```json
{
  "mcpServers": {
    "jira": {
      "type": "http",
      "url": "https://your-domain.atlassian.net/rest/mcp",
      "headers": {
        "Authorization": "Bearer ${JIRA_API_TOKEN}"
      }
    }
  }
}
```

---

## Your Task

### Step 1: Ask for JIRA Ticket ID

Use the `AskUserQuestion` tool to ask the user for the JIRA ticket ID. Present it as a simple text input question.

**Question:** "What is the JIRA ticket ID for this PR? (e.g., PROJ-1234)"

Do NOT proceed without the JIRA ID. Wait for the user's response.

### Step 2: Fetch JIRA Ticket Details (Enhanced Mode)

Check if a JIRA MCP server is available. If it is, fetch the ticket details using the MCP tool:

1. **Get ticket summary and description** — The high-level what and why
2. **Get acceptance criteria** — From the description or a custom field (look for bullet points, checkboxes, or "Acceptance Criteria" heading)
3. **Get ticket type** — Story, Bug, Task, Sub-task, etc.
4. **Get priority and labels** — For context on urgency and categorization

If JIRA MCP is NOT available, skip this step and proceed in basic mode. Do not fail or warn excessively — just proceed without ticket details.

### Step 3: Gather Git Context

Run two commands:

1. **Committed changes** — commit messages + files touched:
   ```bash
   git log --oneline --no-merges --stat
   ```

2. **Uncommitted local changes** — staged and unstaged work not yet committed:
   ```bash
   git diff HEAD --stat
   ```

If `git diff HEAD --stat` returns output, include those changes in the PR message alongside the committed work. If it returns nothing, all changes are already committed — just use the log.

### Step 4: Analyze Changes

From the git diff and commit history, identify:
- **What changed** — The primary purpose of the changes (feature, bugfix, refactor, chore, etc.)
- **Which areas were affected** — Modules, layers, or components touched
- **Key modifications** — Important code changes, new files, deleted files, config changes
- **Testing** — Whether tests were added or modified

### Step 5: Compare Requirements vs Implementation (Enhanced Mode)

If JIRA ticket details were fetched in Step 2, perform a requirements gap analysis:

1. **Extract acceptance criteria** — Parse each criterion from the JIRA ticket into a discrete checkable item
2. **Map criteria to code changes** — For each criterion, find the corresponding implementation in the diff:
   - Search for relevant classes, methods, endpoints, configs, or tests
   - Mark as covered if implementation evidence exists
   - Mark as gap if no corresponding code is found
3. **Detect scope creep** — Identify significant code changes that don't map to any acceptance criterion
4. **Assess coverage** — Calculate how many criteria are addressed vs total

### Step 6: Generate PR Message

Produce the PR message in the following exact format.

**If in Enhanced Mode (JIRA details available):**

```
## <JIRA-ID> | <Short high-level summary in imperative mood>

### Summary
<1-3 sentences describing what this PR does and why, derived from JIRA ticket context>

### What Was Requested
<Brief paraphrase of the JIRA ticket description/goal — 1-2 sentences>

### What Was Implemented

#### Changes
- <Grouped change description 1>
- <Grouped change description 2>
- <Grouped change description 3>

#### Acceptance Criteria Coverage
- [x] <Criterion 1> — Implemented in `FileName.java`
- [x] <Criterion 2> — Implemented in `FileName.java`
- [ ] <Criterion 3> — **Not found in this PR**

> Coverage: X/Y criteria addressed

### Testing
- <What was tested or what tests were added/modified>

### Notes
- <Any deployment notes, migration steps, scope creep flags, or reviewer callouts — omit section if none>
```

**If in Basic Mode (no JIRA details):**

```
## <JIRA-ID> | <Short high-level summary in imperative mood>

### Summary
<1-3 sentences describing what this PR does and why>

### Changes
- <Grouped change description 1>
- <Grouped change description 2>
- <Grouped change description 3>

### Testing
- <What was tested or what tests were added/modified>

### Notes
- <Any deployment notes, migration steps, or reviewer callouts — omit section if none>
```

**Formatting Rules (both modes):**
- PR title line: `<JIRA-ID> | <summary>` — keep under 72 characters
- Summary: Focus on the **why**, not the **what**
- Changes: Group related file changes into logical descriptions (don't list every file individually)
- Use imperative mood ("Add", "Fix", "Update", not "Added", "Fixed", "Updated")
- Keep it concise — reviewers should understand the PR in under 30 seconds
- Omit the Notes section entirely if there are no special notes
- In enhanced mode, flag any uncovered acceptance criteria clearly with **Not found in this PR**
- In enhanced mode, if scope creep is detected, add a note: "Additional changes not in original ticket: ..."

### Step 7: Present the Output

Display the generated PR message in a single markdown code block so the user can copy it directly.

If in enhanced mode and there are uncovered criteria, add a brief note after the code block:
> "**Heads up:** X acceptance criteria from the JIRA ticket are not covered in this PR. Consider addressing them or splitting into a follow-up ticket."

---

## Examples

### Example 1: Enhanced Mode (with JIRA MCP)

**JIRA Ticket PROJ-456:**
- Summary: "As a user, I want to receive email notifications for account events"
- Acceptance Criteria:
  1. User can enable/disable email notifications
  2. User can choose which events trigger notifications
  3. Emails are sent via SMTP
  4. Notification preferences are persisted

**Branch changes:** Added NotificationService, preferences API, DB migration, tests

**Output:**

```
## PROJ-456 | Add email notification service with user preferences

### Summary
Introduce an email notification system that allows users to configure their notification preferences and receive emails for key account events.

### What Was Requested
Enable users to receive configurable email notifications for account events, with persistent preference storage.

### What Was Implemented

#### Changes
- Add `NotificationService` with email sending via SMTP
- Add `/api/v1/users/{id}/notification-preferences` endpoint (GET/PUT)
- Add `notification_preferences` table with Flyway migration
- Add unit and integration tests for notification flows

#### Acceptance Criteria Coverage
- [x] User can enable/disable email notifications — `NotificationPreferencesController.java`
- [x] Emails are sent via SMTP — `NotificationService.java`
- [x] Notification preferences are persisted — `V3__notification_preferences.sql`
- [ ] User can choose which events trigger notifications — **Not found in this PR**

> Coverage: 3/4 criteria addressed

### Testing
- Unit tests for NotificationService (8 cases)
- Integration test for preferences API endpoint
- Manual testing of email delivery via Mailtrap

### Notes
- Requires `SMTP_HOST` and `SMTP_PORT` environment variables in deployment config
- Event-level notification selection (criterion 4) planned for follow-up ticket
```

### Example 2: Basic Mode (no JIRA MCP)

**JIRA ID:** `PROJ-456`
**Branch changes:** Same as above

**Output:**

```
## PROJ-456 | Add email notification service with user preferences

### Summary
Introduce an email notification system that allows users to configure their notification preferences and receive emails for key account events.

### Changes
- Add `NotificationService` with email sending via SMTP
- Add `/api/v1/users/{id}/notification-preferences` endpoint (GET/PUT)
- Add `notification_preferences` table with Flyway migration
- Add unit and integration tests for notification flows

### Testing
- Unit tests for NotificationService (8 cases)
- Integration test for preferences API endpoint
- Manual testing of email delivery via Mailtrap

### Notes
- Requires `SMTP_HOST` and `SMTP_PORT` environment variables in deployment config
```
