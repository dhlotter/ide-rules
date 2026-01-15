---
description: API design patterns and REST conventions
---

# API STANDARDS

## REST Conventions
*   Use plural nouns for resource endpoints (`/users`, `/orders`).
*   Use HTTP methods correctly: GET (read), POST (create), PUT/PATCH (update), DELETE (remove).
*   Return appropriate status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error).

## Response Format
*   Use consistent JSON structure with `data`, `error`, and `meta` fields.
*   Include pagination info for list endpoints.

## Error Handling
*   Return descriptive error messages with error codes.
*   Never expose stack traces in production.

## Versioning
*   Use URL versioning (`/api/v1/`) or header versioning.
*   Maintain backward compatibility within major versions.
