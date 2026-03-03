# Frontmatter Rules

The YAML frontmatter is the most important part of a skill. It determines whether Claude loads the skill. Get this right.

## Required Format

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

That's all that's required to start.

## Field Requirements

### name (required)

- kebab-case only: lowercase letters, digits, hyphens
- No spaces: `Notion Project Setup` is wrong
- No underscores: `notion_project_setup` is wrong
- No capitals: `NotionProjectSetup` is wrong
- Must match the folder name exactly
- Max 40 characters
- Cannot start/end with hyphen or contain consecutive hyphens

### description (required)

**Must include BOTH:**
- What the skill does
- When to use it (trigger conditions)

**Formula:** `[What it does] + [When to use it] + [Key capabilities]`

**Constraints:**
- Under 1024 characters
- No XML angle brackets (< or >) — frontmatter appears in Claude's system prompt; malicious content could inject instructions
- Include specific tasks users might say
- Mention relevant file types if applicable

**Good examples:**

```yaml
# Specific and actionable
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# Includes trigger phrases
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# Clear value proposition
description: End-to-end customer onboarding workflow for PayFlow. Handles account creation, payment setup, and subscription management. Use when user says "onboard new customer", "set up subscription", or "create PayFlow account".

# With negative triggers to prevent over-triggering
description: Advanced data analysis for CSV files. Use for statistical modeling, regression, clustering. Do NOT use for simple data exploration (use data-viz skill instead).

# Scoped to prevent misuse
description: PayFlow payment processing for e-commerce. Use specifically for online payment workflows, not for general financial queries.
```

**Bad examples:**

```yaml
# Too vague — won't trigger correctly
description: Helps with projects.

# Missing triggers — Claude won't know when to load it
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

### license (optional)

- Use when making skill open source
- Common: MIT, Apache-2.0

### compatibility (optional)

- 1-500 characters
- Indicates environment requirements
- Example: intended product, required system packages, network access needs

### metadata (optional)

- Any custom key-value pairs
- Suggested: author, version, mcp-server

```yaml
metadata:
    author: ProjectHub
    version: 1.0.0
    mcp-server: projecthub
```

## Security Restrictions

**Forbidden in frontmatter:**
- XML angle brackets (< >)
- Skills with "claude" or "anthropic" in the name (reserved)

**Why:** Frontmatter appears in Claude's system prompt. Malicious content could inject instructions.

## Debugging Description Quality

Ask Claude: "When would you use the [skill name] skill?" Claude will quote the description back. Adjust based on what's missing.

**Quick checklist:**
- Is it too generic? ("Helps with projects" won't work)
- Does it include trigger phrases users would actually say?
- Does it mention relevant file types if applicable?
- Does it scope correctly to avoid over/under-triggering?
