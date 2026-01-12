---
description: Preferred framework and services stack
---

# TECH STACK

> [!IMPORTANT]
> **Respect Existing Stacks:** If a project already uses a different tech stack, **DO NOT** suggest changing it. Adapt to what's already in place.

## Build
*   **Bundler:** Vite

## Frontend
*   **Framework:** React
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS
*   **UI Library:** Shadcn UI

## Backend (Choose One)

### Option A: Supabase Stack
*   **Functions:** Supabase Edge Functions
*   **Database:** Supabase (Postgres)
*   **Authentication:** Supabase Auth

### Option B: Convex Stack
*   **Functions:** Convex Mutations/Actions
*   **Database:** Convex
*   **Authentication:** Clerk

## Services
*   **Payments:** Lemon Squeezy / Stripe
*   **Emails:** Resend
*   **Analytics:** PostHog

## Dependency Management
*   **Context First:** Always read `package.json` before proposing new dependencies.
*   Prefer established, well-maintained packages.
*   Avoid adding dependencies for trivial functionality.
