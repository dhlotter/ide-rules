# IDE Rules

A centralized repository for AI IDE rules and workflows. Pull-only design for simplicity — fixes go to this repo, then re-run setup.

## Quick Start

```bash
# From any project directory
curl -sSL https://raw.githubusercontent.com/dhlotter/ide-rules/main/setup.sh | bash
```

## What It Does

The setup script will:

1. **Prompt for IDE selection**: Claude, Cursor, Antigravity, or All
2. **Download latest rules** from GitHub (or use local if running from repo)
3. **Copy files** to the correct locations:

| IDE | Rules Location | Workflows/Commands |
|-----|----------------|-------------------|
| Antigravity | `.agent/rules/` | `.agent/workflows/` |
| Claude | `.claude/rules/` | `.claude/commands/` |
| Cursor | `.cursor/rules/` | `.cursor/rules/` |

## Repository Structure

```
ide-rules/
├── rules/
│   ├── king.md                 # Core rules (always loaded)
│   └── reference/
│       ├── api-standards.md    # API design patterns
│       ├── security.md         # Security best practices
│       ├── tech-stack.md       # Technology preferences
│       ├── ui-components.md    # UI/UX guidelines
│       └── workflow.md         # Development workflow
├── workflows/
│   ├── design.md               # Design review workflow
│   ├── featurebase.md          # Feature request workflow
│   ├── git-commit.md           # Commit workflow (no preflight)
│   ├── git-deploy.md           # Deploy workflow (with preflight)
│   ├── sync-ide-rules.md       # Update rules workflow
│   └── troubleshoot.md         # Debugging workflow
├── setup.sh                    # The magic script
└── README.md
```

## Updating Rules

**In a project:**
```bash
# Re-run the setup script to pull latest
~/ide-rules/setup.sh
```

**Fixing a bug or adding a rule:**
1. Make changes in this repository (`dhlotter/ide-rules/`)
2. Commit and push
3. Re-run setup in your projects

## Design Philosophy

| ✅ Pros | ⚠️ Trade-offs |
|---------|---------------|
| Dead simple — just run one command | Pull-only (fix bugs in main repo) |
| No Git complexity (submodules, subtrees) | No automatic sync (must re-run) |
| Works on any project instantly | Files are copies, not linked |
| Single source of truth | |
| Can run from anywhere | |

## Rule Hierarchy

Rules are loaded in the following order (later rules can override earlier ones):

1. **`king.md`** — Core rules, always loaded first
2. **`reference/*.md`** — Specialized topic rules
3. **Project-specific rules** — Any additional rules in the target project

## License

MIT
