---
description: Frontend library discipline and component patterns
---

# UI COMPONENTS STANDARDS

## Library Discipline (CRITICAL)
If a UI library is detected or active in the project, **YOU MUST USE IT**.

*   **Preferred Library:** Shadcn UI is the default choice for existing and new components.
*   **Do not** build custom components (modals, dropdowns, buttons) from scratch if the library provides them.
*   **Do not** pollute the codebase with redundant CSS.
*   *Exception:* You may wrap or style library components, but the underlying primitive must come from the library.

## Shared Components
*   **Reusability First:** Always check if a component already exists before creating a new one.
*   **Colocation:** Shared components live in a dedicated folder (e.g., `components/ui/`).
*   If a new primitive is needed, add it via Shadcn CLI (`npx shadcn-ui@latest add <component>`).

## Stack Preferences
*   Modern Frameworks (React/Vue/Svelte)
*   Tailwind/Custom CSS
*   Semantic HTML5

## Visual Standards
*   Focus on micro-interactions, perfect spacing, and "invisible" UX.
*   Prioritize performance: minimize repaints/reflows.
