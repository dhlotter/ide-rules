---
description: Systematic troubleshooting protocol for fixing errors
---

# Fix Errors - Systematic Troubleshooting Protocol

**Objective**: Fix existing errors in the codebase WITHOUT implementing new features. Only fix what's broken.

## Rules

### 1. Investigation First (95% Confidence Rule)
- **STOP** before making ANY changes.
- **Git History Audit**: If the bug is a regression, run `git log -p [file]` to see recent changes that might have introduced it.
- Investigate the error thoroughly:
  - Read the full error message and stack trace.
  - Check relevant files mentioned in the error.
  - **Mandatory Root Cause Statement**: You MUST explicitly state the root cause in the chat before applying any code changes.
- **Use research tools**:
  - `grep_search` - To find related code patterns.
  - `read_terminal` - To check live error logs or build output.
  - `browser_subagent` - To reproduce and inspect UI-level errors.
- Only proceed when you have **95% confidence** you understand the problem.

### 2. Fix ONLY - No New Features
- ❌ **DO NOT** add new functionality.
- ❌ **DO NOT** refactor working code for non-essential reasons.
- ❌ **Anti-Patching**: Do NOT use `any` as a type fix or andding `// @ts-ignore` as a permanent solution. Fix the underlying type or logic.
- ✅ **DO** fix import paths, types, syntax, and configurations.

### 3. Test EVERY Fix
- After EACH fix:
  - **Verify UI**: Use `browser_subagent` to ensure the page loads and the specific error is gone.
  - **Verify Build**: Run `npm run build` to ensure the fix hasn't broken the production build.
  - **Neighboring Component Check**: Explicitly test components that deliver data to or receive data from the fixed code.
- **DO NOT** assume the fix works - TEST IT.

### 4. Iterative Process
```
1. Find error in logs/console/UI.
2. Audit Git history (if regression).
3. State Root Cause (95% confidence).
4. Apply minimal fix (No @ts-ignore).
5. Test fix works (UI + Build + Neighbors).
6. If new errors appear or build fails → Go to step 1.
7. If fixed → Go to step 1 (check for more errors).
8. If no more errors → DONE.
```

### 5. Error Priority
1. **Build/compilation errors** (blocking).
2. **Import/module errors** (blocking).
3. **Type errors** (if causing build to fail).
4. **Runtime errors** (crashes, null pointer exceptions).
5. **Console warnings** (lowest priority).

### 6. Report Progress
After each fix:
- ✅ **Root Cause**: State why it was broken.
- ✅ **Fix**: State what was changed.
- ✅ **Proof**: Show test results (Build status, Browser screenshots/logs).
