# Workflow & Deployment Protocols

This document outlines the standard behavioral protocols for tasks involving deployment and source control.

## Core Principles

**CRITICAL RULES FOR AI AGENT:**
1. **NEVER auto-commit** - The Agent will **NEVER** commit changes to git automatically.
2. **NEVER auto-merge** - The Agent will **NEVER** merge branches automatically.
3. **Always suggest, never execute** - The Agent will suggest git commands but wait for explicit user instruction.

## Rules vs Workflows/Commands

**Rules define default behavior; workflows/commands grant temporary, scoped exceptions.**

- **Rules** (in `.agent/rules/` or `.claude/rules/`) define persistent behavioral guidelines that the agent must always follow by default.
- **Workflows/Commands** (in `.agent/workflows/` or `.claude/commands/`) are one-time, ad-hoc requests that may temporarily override rules **only within the scope of that specific user request**.
- When a user explicitly invokes a workflow/command (e.g., `/deploy`), the agent may perform actions that would normally violate rules, but **only for that single request**.
- In all subsequent interactions, the agent reverts to following the rules unless another explicit workflow/command is invoked.
- Workflows/commands do **NOT** permanently modify or overwrite rules.

**Example:** The rule states "NEVER auto-commit." However, when the user explicitly runs `/deploy`, the agent may commit and push as part of that workflow. In the next interaction, the agent will not auto-commit unless `/deploy` is invoked again.

