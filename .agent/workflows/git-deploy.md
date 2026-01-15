---
description: Interactive deployment workflow with safety checks and branch confirmation.
---

# Interactive Deployment Workflow

This command guides the agent through a safe deployment process, ensuring all checks are met and explicit user approval is granted at every stage.

## Phase 1: Pre-flight Checks
The agent MUST run the following checks and fix any issues found:
1. **Lint Check**: Run `npm run lint`.
2. **Build Check**: Run `npm run build`.
3. **Test Check**: Run `npm test` (if available).

## Phase 2: Configuration & Approval
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

## Phase 3: Execution
Once (and ONLY once) the branch and commit message are approved:
1. Stage all changes: `git add .`
2. Commit with the approved message: `git commit -m "[message]"`
3. Push to the confirmed branch: `git push origin [branch-name]`

## Phase 4: Final Verification
1. Wait for the production/preview build to complete.
2. Confirm with the user that the changes are live and functioning correctly.
