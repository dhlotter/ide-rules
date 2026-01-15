---
description: Create a pull request from dev branch to main branch.
---

# Git Main PR Workflow

This command guides the agent through creating a pull request from the `dev` branch to the `main` branch. This workflow assumes that changes have already been committed and pushed to `dev`.

## Phase 1: Pre-flight Verification
Before creating the PR, the agent MUST:

### 1. Verify Dev Branch Status
- Check that we're working with the `dev` branch:
  - Run `git fetch origin` to get latest remote state.
  - Check if `dev` branch exists: `git branch -r | grep origin/dev`
  - Verify local `dev` is up to date: `git status` (should show "Your branch is up to date with 'origin/dev'" or similar)

### 2. Check for Uncommitted Changes
- Check for uncommitted changes: `git status --porcelain`
- If there are uncommitted changes, inform the user and ask if they want to commit them first using the `git-dev-commit` workflow.

### 3. Verify Dev Has Commits Ahead of Main
- Check if `dev` has commits that aren't in `main`:
  - Run `git log origin/main..origin/dev --oneline` (or `git log main..dev --oneline` if main exists locally)
- If no commits are found, inform the user that `dev` is already up to date with `main` and no PR is needed.
- If commits exist, show a summary of commits that will be included in the PR.

## Phase 2: PR Creation
The agent should create the PR using one of these methods (in order of preference):

### Method 1: GitHub CLI (gh)
If `gh` CLI is available:
1. Run `gh pr create --base main --head dev --title "[title]" --body "[body]"`
2. Use a descriptive title based on the commits being merged.
3. Include a detailed body that summarizes the changes.

### Method 2: Manual Instructions
If `gh` CLI is not available:
1. Provide the user with the PR URL format: `https://github.com/[owner]/[repo]/compare/main...dev`
2. Or provide step-by-step instructions:
   - Navigate to the repository on GitHub
   - Click "New Pull Request"
   - Set base branch to `main` and compare branch to `dev`
   - Fill in title and description
   - Click "Create Pull Request"

## Phase 3: PR Details
When creating the PR, include:

### Title
- Follow conventional commit format or clear description
- Example: "Merge dev to main: [feature description]" or "Release: [version/feature]"

### Body
- Summary of changes included in the PR
- List of key commits (from `git log origin/main..origin/dev`)
- Any breaking changes or migration notes
- Testing notes or verification steps

## Phase 4: Final Verification
1. Confirm with the user that the PR has been created.
2. Provide the PR URL or number for reference.
3. Wait for the production/preview build to complete (if CI/CD is configured).
4. Confirm with the user that the changes are live and functioning correctly (if applicable).
5. Remind the user to review and merge the PR when ready.
