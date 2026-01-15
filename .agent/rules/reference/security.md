---
description: Security protocols for secrets, validation, and defense-in-depth
---

# SECURITY PROTOCOLS

## Secrets Management

> [!CAUTION]
> **NEVER** hardcode secrets, API keys, or credentials in source code. If you detect this happening, **WARN THE USER IMMEDIATELY**.

*   **Local Development:** Store secrets in `.env.local` (gitignored by default).
*   **Production:** Use platform environment variables (Vercel, Supabase, etc.).
*   **Client-Side:** Only expose via build-time injection (`VITE_*`, `NEXT_PUBLIC_*`).

## Input Validation
*   Always sanitize and validate user input on both client and server.
*   Use schema validation libraries (Zod, Yup) for structured data.

## Defense in Depth
*   Assume client-side checks will fail; enforce logic server-side.
*   Implement rate limiting on sensitive endpoints.
*   Use parameterized queries to prevent SQL injection.
