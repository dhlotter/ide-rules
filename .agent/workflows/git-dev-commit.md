---
description: Commit workflow for dev branch with pre-flight checks (bolt, build, lint, tests).
---

# Git Dev Commit Workflow

This command guides the agent through committing changes to the `dev` branch with comprehensive pre-flight checks. It ensures code quality through testing, linting, and build verification before committing.

## Phase 1: Pre-flight Checks
The agent MUST run the following checks **before** committing. If any check fails, fix the issues before proceeding:

### 1. Check for npm bolt
- Check if `npm bolt` script exists in `package.json`:
  - Run `npm run bolt` if it exists.
  - If it fails, fix the issues before proceeding.

### 2. Build Check
- Run `npm run build` to ensure the build succeeds.
- This verifies that `npm bolt` (if run) was successful and the code compiles correctly.
- If build fails, fix the issues before proceeding.

### 3. Lint Check
- Run `npm run lint` to check code quality and style.
- Fix any linting errors before proceeding.

### 4. Test Check
- Check if test scripts exist in `package.json` (e.g., `npm test`, `npm run test`).
- Run the appropriate test command if available.
- If tests fail, fix the issues before proceeding.

**Order of Execution:**
The checks can be run in parallel or sequentially, but all must pass before proceeding to commit.

## Phase 2: Branch Confirmation
- **Always commit to the `dev` branch.**
- Check if currently on `dev` branch using `git branch --show-current` or `git rev-parse --abbrev-ref HEAD`.
- If not on `dev` branch:
  - Switch to `dev` branch: `git checkout dev` or `git switch dev`
  - If `dev` branch doesn't exist locally, create it: `git checkout -b dev` (and optionally set upstream: `git push -u origin dev`)
- Inform the user: "Committing to dev branch."

## Phase 3: Commit Message Proposal
- Prepare a **very detailed and comprehensive** commit message that:
    - Analyzes the recent chat history to understand the context and motivation for changes.
    - Reviews all staged/unstaged changes using `git diff --cached` or `git status`.
    - Summarizes the changes with specific file names, functions, and modifications.
    - Follows conventional commit format (e.g., `feat:`, `fix:`, `refactor:`, `chore:`).
- Present the message to the user.
- **WAIT** for the user to approve or request edits to the message.

## Phase 4: Execution
Once (and ONLY once) the commit message is approved:
1. Stage all changes: `git add .`
2. Commit with the approved message: `git commit -m "[message]"`
3. Push to the dev branch: `git push origin dev`

## Phase 5: Final Verification
1. Confirm with the user that the changes are committed and pushed to the dev branch.
2. Remind the user that they can use the `git-main-pr` workflow to create a PR from dev to main when ready.
