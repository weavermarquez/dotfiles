#!/usr/bin/env python3
"""
Quick validation script for skills

Checks:
- SKILL.md exists (exact case)
- No README.md inside skill folder
- Valid YAML frontmatter with --- delimiters
- name: kebab-case, matches folder name, max 40 chars
- name: no "claude" or "anthropic" (reserved)
- description: present, under 1024 chars, no XML angle brackets
- description: includes both WHAT and WHEN (heuristic check)
"""

import sys
import re
from pathlib import Path


def validate_skill(skill_path):
    """Validate a skill directory. Returns (valid, message) tuple."""
    skill_path = Path(skill_path)
    errors = []
    warnings = []

    # Check SKILL.md exists (exact case)
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        # Check for common misspellings
        for variant in ['skill.md', 'SKILL.MD', 'Skill.md', 'Skill.MD']:
            if (skill_path / variant).exists():
                return False, f"Found '{variant}' but must be exactly 'SKILL.md' (case-sensitive)"
        return False, "SKILL.md not found"

    # Check for README.md (should not exist inside skill folder)
    if (skill_path / 'README.md').exists():
        warnings.append("README.md found inside skill folder — all documentation should go in SKILL.md or references/")

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found (must start with ---)"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format (missing closing ---)"

    frontmatter = match.group(1)

    # Check required fields
    if 'name:' not in frontmatter:
        errors.append("Missing 'name' in frontmatter")
    if 'description:' not in frontmatter:
        errors.append("Missing 'description' in frontmatter")

    if errors:
        return False, "; ".join(errors)

    # Validate name field
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()

        # kebab-case check
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"Name '{name}' must be kebab-case (lowercase letters, digits, and hyphens only)")
        elif name.startswith('-') or name.endswith('-') or '--' in name:
            errors.append(f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens")

        # Length check
        if len(name) > 40:
            errors.append(f"Name '{name}' exceeds 40 character limit ({len(name)} chars)")

        # Must match folder name
        folder_name = skill_path.name
        if name != folder_name:
            errors.append(f"Name '{name}' does not match folder name '{folder_name}'")

        # Reserved names
        if 'claude' in name.lower() or 'anthropic' in name.lower():
            errors.append(f"Name '{name}' cannot contain 'claude' or 'anthropic' (reserved)")

    # Validate description field
    desc_match = re.search(r'description:\s*(.+?)(?:\n[a-z]|\n---|\Z)', frontmatter, re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()

        # Angle brackets check
        if '<' in description or '>' in description:
            errors.append("Description cannot contain XML angle brackets (< or >)")

        # Length check
        if len(description) > 1024:
            errors.append(f"Description exceeds 1024 character limit ({len(description)} chars)")

        # Heuristic: check for trigger phrases (WHEN component)
        trigger_indicators = [
            'use when', 'use for', 'triggers on', 'trigger on',
            'use this when', 'use if', 'when user', 'when the user',
            'asks for', 'asks to', 'mentions', 'says',
            'do not use', 'not for'
        ]
        has_trigger = any(indicator in description.lower() for indicator in trigger_indicators)
        if not has_trigger:
            warnings.append("Description may be missing trigger conditions (WHEN to use). Include phrases like 'Use when...' or specific user triggers.")

        # Heuristic: too short/vague
        if len(description) < 30:
            warnings.append("Description seems too short — include both WHAT the skill does and WHEN to use it")

    if errors:
        return False, "; ".join(errors)

    # Build result message
    result = "Skill is valid!"
    if warnings:
        result += "\n  Warnings:\n  - " + "\n  - ".join(warnings)

    return True, result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
