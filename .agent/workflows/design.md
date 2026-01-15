---
description: Guidelines for creating distinctive, production-grade frontend interfaces with high design quality.
---

# **/design Workflow**

**Trigger**: Use the slash command **`/design`** to enter "Avant-Garde Design Mode" for a specific component or page.

## 1. Design Thinking Strategy

Before coding, commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a direction (e.g., Brutalism, Glassmorphism, Neomorphism, Swiss Style, Cyberpunk). Avoid "Generic Bootstrap".
- **Differentiation**: What makes this UNFORGETTABLE?
- **Intentionality**: Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

## 2. Aesthetics Guidelines

### Typography
- **Selection**: Choose fonts that are beautiful and unique. Avoid generic defaults (Arial, system-ui) unless requested.
- **Pairing**: Pair a distinctive display font (headers) with a refined body font (readability).

### Color & Theme
- **Cohesion**: Commit to a cohesive palette. Use CSS variables.
- **Confidence**: Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

### Motion & Micro-interactions
- **Implementation**: Use CSS-only solutions where possible (Tailwind `transition-*`, `animate-*`) or `framer-motion` for React.
- **Timing**: Focus on high-impact moments (page load, staggered reveals).
- **Interactivity**: Scroll-triggers and hover states should surprise and delight.

### Spatial Composition
- **Layout**: Experiment with asymmetry, overlap, diagonal flow, and grid-breaking elements.
- **Whitespace**: Use generous negative space OR controlled density. Never accidental gaps.

### Visual Depth
- **Texture**: Create atmosphere. Use gradients, noise textures, glass effects (backdrop-filter), and layered shadows.
- **Prohibition**: NEVER use generic flat colors without context.

## 3. Integration with System Rules

**CRITICAL COMPATIBILITY WITH `king.md`**:
1.  **Library Discipline**: You **MUST** still use the project's established UI library (e.g., Shadcn UI, Radix) for the *structural* primitives (Buttons, Modals, Inputs).
2.  **Aesthetic Overlay**: Apply these design rules via **styling** (Tailwind classes, CSS modules) *on top of* the library components. Do not rebuild primitives from scratch just to change a border radius.
3.  **Complexity Match**: Match implementation complexity to the aesthetic vision.
