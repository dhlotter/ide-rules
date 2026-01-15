---
description: Create a pull request from dev branch to main branch and merge it.
---

# Git Main PR Workflow

This command guides the agent through creating a pull request from the `dev` branch to the `main` branch and merging it. This workflow assumes that changes have already been committed and pushed to `dev`.

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

## Phase 4: Wait for CI/CD (if applicable)
- If CI/CD is configured, wait for the production/preview build to complete.
- Check PR status: `gh pr view [PR_NUMBER]` (if using GitHub CLI) or check the PR page.
- Ensure all checks pass before proceeding to merge.

## Phase 5: Merge PR
The agent should merge the PR using one of these methods (in order of preference):

### Method 1: GitHub CLI (gh)
If `gh` CLI is available:
1. Merge the PR: `gh pr merge [PR_NUMBER] --merge` (or `--squash` or `--rebase` based on project preferences)
2. If merge method is not specified, use `--merge` as default.
3. Confirm the merge was successful.

### Method 2: Manual Merge Instructions
If `gh` CLI is not available or merge fails:
1. Provide the PR URL to the user.
2. Instruct them to:
   - Navigate to the PR on GitHub
   - Click "Merge pull request"
   - Confirm the merge
   - Optionally delete the dev branch if prompted

### Method 3: Direct Git Merge (fallback)
If PR creation failed but we still need to merge:
1. Switch to main branch: `git checkout main` or `git switch main`
2. Pull latest: `git pull origin main`
3. Merge dev into main: `git merge origin/dev` or `git merge dev`
4. Push to main: `git push origin main`
5. **Note**: This bypasses PR review, so only use if PR creation failed and user explicitly approves.

## Phase 6: Final Verification
1. Confirm with the user that the PR has been merged into main.
2. Verify main branch is updated: `git fetch origin && git log origin/main --oneline -5`
3. Confirm with the user that the changes are live and functioning correctly (if applicable).
4. Optionally, remind the user to pull the latest main branch: `git checkout main && git pull origin main`
