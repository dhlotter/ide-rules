# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is the centralized "source of truth" for AI IDE rules and workflows. It distributes standardized agent behavior configurations to multiple AI-powered IDEs (Claude, Cursor, Antigravity). Changes are made here, then propagated to target projects via `setup.sh`.

## Key Commands

```bash
# Test the setup script locally (installs to current directory)
./setup.sh

# Test installation to a specific target directory
./setup.sh /path/to/target/project
```

## Architecture

**Pull-only design**: Rules are edited in this repo, committed, then re-deployed. Never edit the `.claude/`, `.cursor/`, or `.agent/` folders in target projects directly.

### Content Hierarchy

1. **`rules/king.md`** — Core behavioral rules (loaded first, highest priority)
2. **`rules/reference/*.md`** — Domain-specific standards (API, security, UI, etc.)
3. **`workflows/*.md`** — Step-by-step procedures (become IDE commands)

### Distribution Targets

| IDE | Rules | Workflows |
|-----|-------|-----------|
| Antigravity | `.agent/rules/` | `.agent/workflows/` |
| Claude | `.claude/rules/` | `.claude/commands/` |
| Cursor | reads from `.claude/` | reads from `.claude/` |

### setup.sh Behavior

- Detects if running locally (from repo) or remotely (via curl)
- Clears and replaces target directories (clean sync, not merge)
- Removes legacy `.cursor/` directories (consolidated to `.claude/`)
- Falls back: gh CLI → git → curl for individual files

## Working in This Repo

- Maintain markdown structure and clarity
- New rules in `rules/` should be referenced in `king.md` under "Modular References"
- Ensure `setup.sh` remains cross-platform bash compatible
- The `backup/` directory contains archived content, not active configuration
