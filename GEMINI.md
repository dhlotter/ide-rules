# IDE Rules & Workflows

This directory acts as the centralized "source of truth" for AI agent behaviors, coding standards, and operational workflows across multiple projects. It is designed to be pulled into other repositories to standardize the AI's assistance.

## Directory Overview

*   **`rules/`**: Contains the instructional files that define the AI's persona, coding standards, and behavioral protocols.
    *   **`king.md`**: The primary "Constitution" or core system prompt. It defines the AI's role (Senior Architect), operational modes (Standard vs. "ULTRATHINK"), and design philosophy.
    *   **`reference/`**: Specialized guidelines for specific domains (API standards, Security, UI components, etc.).
*   **`workflows/`**: detailed, step-by-step procedures for common development tasks (e.g., `git-commit.md`, `troubleshoot.md`, `design.md`). These serve as "Standard Operating Procedures" for the agent.
*   **`setup.sh`**: The distribution script. It installs or updates the rules and workflows from this repository into a target project's local configuration folders (e.g., `.cursor/`, `.claude/`, `.agent/`).

## Key Files & Concepts

### `setup.sh`
This script is the bridge between this repository and the developer's active projects.
*   **Function:** Copies content from `rules/` and `workflows/` to the appropriate hidden directories in the target project.
*   **Usage:** It can be run remotely via `curl` or locally.
*   **Target Locations:**
    *   Antigravity: `.agent/rules/`, `.agent/workflows/`
    *   Claude: `.claude/rules/`, `.claude/commands/`
    *   Cursor: `.cursor/rules/` (Reads from `.claude` as well)

### `rules/king.md`
This is the most critical file for agent behavior. It dictates:
*   **Role:** Senior Full-Stack Architect & Avant-Garde UI Designer.
*   **Directives:** "Zero Fluff", "Context First", and "Intentional Minimalism".
*   **Modes:** Defines the "ULTRATHINK" trigger for deep reasoning vs. standard execution.

## Usage & Contribution

1.  **Modifying Rules:**
    *   All changes to agent behavior or standards should be made in **this repository** (`dhlotter/ide-rules`), NOT in the local `.cursor` or `.claude` folders of a project.
    *   Edit the relevant markdown file in `rules/` or `workflows/`.

2.  **Propagating Changes:**
    *   After committing changes here, developers run the `setup.sh` script in their target projects to pull the latest rules.

3.  **Agent Behavior in This Repo:**
    *   When working within *this* specific repository, maintain the structure and clarity of the markdown files.
    *   Ensure any new rules added to `rules/` are properly referenced or categorized.
    *   If editing `setup.sh`, ensure cross-platform compatibility (bash).
