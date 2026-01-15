---
description: Simple commit workflow for main branch without pre-flight checks.
---

# Git Main Commit Workflow

This command guides the agent through a simple commit process directly to the `main` branch without running pre-flight checks (no lint, build, or tests). Use this for repositories that don't require validation before committing, such as documentation repos, config repos, or simple projects.

## Phase 1: Branch Confirmation
- **Always commit to the `main` branch.**
- Check if currently on `main` branch using `git branch --show-current` or `git rev-parse --abbrev-ref HEAD`.
- If not on `main` branch:
  - Switch to `main` branch: `git checkout main` or `git switch main`
  - Pull latest changes: `git pull origin main`
- Inform the user: "Committing to main branch."

## Phase 2: Generate Commit Message
- Prepare a **detailed and comprehensive** commit message that:
    - Analyzes the recent chat history to understand the context and motivation for changes.
    - Reviews all staged/unstaged changes using `git diff --cached` or `git status`.
    - Summarizes the changes with specific file names, functions, and modifications.
    - Follows conventional commit format (e.g., `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`).
- Generate the message and proceed directly to commit (no approval needed).

## Phase 3: Execution
1. Stage all changes: `git add .`
2. Commit with the generated message: `git commit -m "[message]"`
3. Push to the main branch: `git push origin main`

## Phase 4: Final Verification
1. Confirm with the user that the changes are committed and pushed to the main branch.
