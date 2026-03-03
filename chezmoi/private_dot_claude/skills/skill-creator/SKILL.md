---
name: skill-creator
description: Interactive guide for creating and improving skills that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations. Use when users want to create a new skill, update an existing skill, or review a skill for quality. Triggers on "create a skill", "build a skill", "new skill", "improve this skill", "review this skill".
---

# Skill Creator

This skill provides guidance for creating effective skills — modular, self-contained packages that capture procedural knowledge, workflows, and domain expertise so Claude can apply them consistently.

## Core Concepts

### What Skills Are

A skill is a folder containing instructions that teach Claude how to handle specific tasks or workflows. Instead of re-explaining preferences and processes every conversation, teach Claude once.

### Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

1. **Metadata** (name + description in YAML frontmatter) — always in Claude's system prompt (~100 words)
2. **SKILL.md body** — loaded when Claude determines the skill is relevant (keep under 5k words)
3. **Bundled resources** (scripts/, references/, assets/) — loaded only as needed by Claude

### Skill Anatomy

```
skill-name/
├── SKILL.md                    # Required - main instructions
├── scripts/                    # Optional - executable code
├── references/                 # Optional - documentation loaded as needed
└── assets/                     # Optional - templates, fonts, icons used in output
```

## Skill Creation Process

Follow these steps in order. Skip a step only when there is a clear reason it does not apply.

### Step 1: Understand with Concrete Examples

To create an effective skill, first establish clear examples of how it will be used.

Ask:
- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP)?
- What domain knowledge or best practices should be embedded?
- What would a user say that should trigger this skill?

Define 2-3 concrete use cases before writing any code:

```
Use Case: [Name]
Trigger: User says "[example phrase]" or "[alternative phrase]"
Steps:
1. [First action]
2. [Second action]
3. [Third action]
Result: [Expected outcome]
```

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Choose an Approach

**Problem-first:** User describes an outcome ("I need to set up a project workspace"). The skill orchestrates the right tool calls in the right sequence. The skill handles the tools.

**Tool-first:** User has tool access ("I have Notion MCP connected"). The skill teaches Claude optimal workflows and best practices. The skill provides expertise.

Most skills lean one direction. Identify which framing fits before designing.

### Step 3: Plan Reusable Contents

Analyze each use case to identify what should be bundled:

- **scripts/** — Code that gets rewritten repeatedly or needs deterministic reliability. Token-efficient; may be executed without loading into context.
- **references/** — Documentation Claude should consult while working (schemas, API docs, policies, detailed guides). Keeps SKILL.md lean; loaded only when needed. For large files (>10k words), include grep search patterns in SKILL.md.
- **assets/** — Files used in output (templates, images, fonts, boilerplate). Not loaded into context; copied or modified in final output.

Information should live in either SKILL.md or references, not both.

### Step 4: Initialize the Skill

When creating a new skill from scratch, run:

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

This generates the skill directory with a SKILL.md template and example resource directories. Skip this step if iterating on an existing skill.

### Step 5: Write the Skill

#### Frontmatter (Critical)

The YAML frontmatter determines when Claude loads the skill. Consult `references/frontmatter-rules.md` for full specification. Key rules:

- **name:** kebab-case, must match folder name, no spaces or capitals
- **description:** Must include WHAT the skill does + WHEN to use it. Formula: `[What it does] + [When to use it] + [Key capabilities]`. Under 1024 characters. No XML angle brackets. Include specific trigger phrases users would say.

Good example:
```yaml
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".
```

Bad example:
```yaml
description: Helps with projects.
```

#### Instructions Body

**Writing style:** Use imperative/infinitive form (verb-first instructions), not second person. Write "To accomplish X, do Y" rather than "You should do X."

**Be specific and actionable:**
```
# Good
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)

# Bad
Validate the data before proceeding.
```

**Structure recommendations** — choose based on skill purpose:
- **Workflow-based:** Sequential processes with decision trees
- **Task-based:** Multiple operations/capabilities
- **Reference/Guidelines:** Standards, specifications, brand rules
- **Capabilities-based:** Interrelated features

**Reference bundled resources clearly:**
```
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

**Include error handling** with specific troubleshooting for common failures.

**Include examples** showing realistic user requests and expected workflow.

**Keep SKILL.md focused.** Move detailed documentation to `references/` and link to it. Keep only essential procedural instructions and workflow guidance in SKILL.md.

**No README.md** inside the skill folder. All documentation goes in SKILL.md or references/.

#### Optional Frontmatter Fields

- `license:` — MIT, Apache-2.0, etc.
- `compatibility:` — Environment requirements (1-500 chars)
- `metadata:` — author, version, mcp-server

### Step 6: Validate and Package

Validate the skill structure:

```bash
python scripts/quick_validate.py <path/to/skill-folder>
```

Package into a distributable zip:

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

### Step 7: Test and Iterate

Consult `references/testing-and-iteration.md` for the full testing approach. Key areas:

1. **Triggering tests** — Does the skill load for obvious tasks? Paraphrased requests? Does it stay silent on unrelated topics?
2. **Functional tests** — Does it produce valid outputs? Do API/tool calls succeed? Are edge cases handled?
3. **Performance comparison** — Compare the same task with and without the skill enabled. Count tool calls, tokens consumed, and user corrections needed.

**Iteration signals:**
- **Undertriggering** (skill doesn't load when it should): Add more detail and trigger phrases to the description
- **Overtriggering** (skill loads for irrelevant queries): Add negative triggers ("Do NOT use for..."), be more specific
- **Instructions not followed**: Keep instructions concise, use bullet points, put critical instructions at the top with `## Important` or `## Critical` headers. Move detailed reference to separate files.

## Patterns

Consult `references/patterns.md` for detailed workflow patterns including:
- Sequential workflow orchestration
- Multi-MCP coordination
- Iterative refinement
- Context-aware tool selection
- Domain-specific intelligence

## Troubleshooting

Consult `references/troubleshooting.md` for solutions to common issues:
- Skill won't upload
- Skill doesn't trigger / triggers too often
- Instructions not followed
- MCP connection issues
- Large context performance issues
