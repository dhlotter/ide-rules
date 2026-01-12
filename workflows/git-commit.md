---
description: Streamlined git commit workflow without pre-flight checks.
---

# Git Commit Workflow

This command guides the agent through a safe commit process without running pre-flight checks (like lint or build). It ensures branch confirmation and explicit user approval for the commit message.

## Phase 1: Configuration & Approval
Before proceeding to commit, the agent MUST:

### 1. Identify and Confirm Branch
- List available local branches using `git branch`.
- Present the list to the user.
- **WAIT** for the user to specify or confirm the target branch.

### 2. Propose Commit Message
- Prepare a **very detailed and comprehensive** commit message that:
    - Analyzes the recent chat history to understand the context and motivation for changes.
    - Reviews all staged changes using `git diff --cached` or `git status`.
    - Summarizes the changes with specific file names, functions, and modifications.
    - Follows conventional commit format (e.g., `feat:`, `fix:`, `refactor:`).
- Present the message to the user.
- **WAIT** for the user to approve or request edits to the message.

## Phase 2: Execution
Once (and ONLY once) the branch and commit message are approved:
1. Stage all changes: `git add .`
2. Commit with the approved message: `git commit -m "[message]"`
3. Push to the confirmed branch: `git push origin [branch-name]`

## Phase 3: Final Verification
1. Confirm with the user that the changes are pushed and live.
