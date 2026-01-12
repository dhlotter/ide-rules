## How it Works
- Rules are managed in a separate git repository linked as a submodule in `.ide-config`.
- Rules are organized directly into `.agent/`, `.cursor/`, and `.claude/` folders.
- The `setup.sh` script **copies** these folders directly to the project root.
- Each IDE has its own independent configuration, though they often share similar rules.

## Maintenance
If rules are outdated, run:
- **Terminal**: `bash .ide-config/setup.sh`
- **Antigravity/Claude**: Run `/update-rules` (which runs the terminal command for you).

## Adding New Rules
1. Edit files directly in the respective IDE folders (`.agent/`, `.cursor/`, or `.claude/`).
2. Run the `setup.sh` script to propagate changes.
