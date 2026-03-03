# Testing and Iteration

Skills can be tested at varying levels of rigor depending on needs:

- **Manual testing in Claude.ai** — Run queries directly and observe behavior. Fast iteration, no setup required.
- **Scripted testing in Claude Code** — Automate test cases for repeatable validation across changes.
- **Programmatic testing via skills API** — Build evaluation suites that run systematically against defined test sets.

Choose the approach that matches quality requirements and the visibility of the skill.

**Pro tip:** Iterate on a single task before expanding. The most effective skill creators iterate on a single challenging task until Claude succeeds, then extract the winning approach into a skill. This leverages Claude's in-context learning and provides faster signal than broad testing.

## Success Criteria

These are aspirational targets — rough benchmarks rather than precise thresholds. Aim for rigor but accept there will be an element of vibes-based assessment.

### Quantitative Metrics

- **Skill triggers on 90% of relevant queries**
  - How to measure: Run 10-20 test queries that should trigger the skill. Track how many times it loads automatically vs. requires explicit invocation.

- **Completes workflow in X tool calls**
  - How to measure: Compare the same task with and without the skill enabled. Count tool calls and total tokens consumed.

- **0 failed API calls per workflow**
  - How to measure: Monitor MCP server logs during test runs. Track retry rates and error codes.

### Qualitative Metrics

- **Users don't need to prompt Claude about next steps**
  - How to assess: During testing, note how often you need to redirect or clarify. Ask beta users for feedback.

- **Workflows complete without user correction**
  - How to assess: Run the same request 3-5 times. Compare outputs for structural consistency and quality.

- **Consistent results across sessions**
  - How to assess: Can a new user accomplish the task on first try with minimal guidance?

## Recommended Testing Approach

### 1. Triggering Tests

**Goal:** Ensure the skill loads at the right times.

Test cases:
- Triggers on obvious tasks
- Triggers on paraphrased requests
- Does NOT trigger on unrelated topics

Example test suite:
```
Should trigger:
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
- "Initialize a ProjectHub project for Q4 planning"

Should NOT trigger:
- "What's the weather in San Francisco?"
- "Help me write Python code"
- "Create a spreadsheet" (unless the skill handles sheets)
```

### 2. Functional Tests

**Goal:** Verify the skill produces correct outputs.

Test cases:
- Valid outputs generated
- API calls succeed
- Error handling works
- Edge cases covered

Example:
```
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When: Skill executes workflow
Then:
    - Project created in ProjectHub
    - 5 tasks created with correct properties
    - All tasks linked to project
    - No API errors
```

### 3. Performance Comparison

**Goal:** Prove the skill improves results vs. baseline.

Baseline comparison:
```
Without skill:
- User provides instructions each time
- 15 back-and-forth messages
- 3 failed API calls requiring retry
- 12,000 tokens consumed

With skill:
- Automatic workflow execution
- 2 clarifying questions only
- 0 failed API calls
- 6,000 tokens consumed
```

## Iteration Based on Feedback

Skills are living documents. Plan to iterate based on:

### Undertriggering Signals

- Skill doesn't load when it should
- Users manually enabling it
- Support questions about when to use it

**Solution:** Add more detail and nuance to the description — this may include keywords, particularly for technical terms.

### Overtriggering Signals

- Skill loads for irrelevant queries
- Users disabling it
- Confusion about purpose

**Solution:** Add negative triggers ("Do NOT use for..."), be more specific about scope.

### Execution Issues

- Inconsistent results
- API call failures
- User corrections needed

**Solution:** Improve instructions, add error handling. Keep instructions concise, use bullet points and numbered lists. Put critical instructions at the top. Move detailed reference to separate files.

### Instructions Not Followed

Common causes and fixes:

1. **Instructions too verbose** — Keep concise. Use bullet points. Move detailed reference to separate files.
2. **Instructions buried** — Put critical instructions at the top. Use `## Important` or `## Critical` headers. Repeat key points if needed.
3. **Ambiguous language** — Be specific:
   ```
   # Bad
   Make sure to validate things properly

   # Good
   CRITICAL: Before calling create_project, verify:
   - Project name is non-empty
   - At least one team member assigned
   - Start date is not in the past
   ```
4. **Model laziness** — Add explicit encouragement in a Performance Notes section:
   ```
   ## Performance Notes
   - Take your time to do this thoroughly
   - Quality is more important than speed
   - Do not skip validation steps
   ```
   Note: Adding this to user prompts is more effective than in SKILL.md.

### Large Context Issues

**Symptom:** Skill seems slow or responses degraded.

**Causes:** Skill content too large, too many skills enabled simultaneously, all content loaded instead of progressive disclosure.

**Solutions:**
1. Optimize SKILL.md size — move detailed docs to references/, link instead of inline, keep SKILL.md under 5,000 words
2. Reduce enabled skills — evaluate if more than 20-50 skills are enabled simultaneously, recommend selective enablement, consider skill "packs" for related capabilities
