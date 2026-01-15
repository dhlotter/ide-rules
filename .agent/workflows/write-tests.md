# write-tests

Write unit tests for utility functions and backend logic. Mock all external dependencies.

## Critical Rules

1. **ONLY test logic** — Utility functions, data transformations, business rules
2. **NEVER test UI** — No component rendering, no "renders correctly" tests
3. **MOCK everything external** — Prisma, APIs, server-only, third-party services
4. **CO-LOCATE tests** — Place `foo.test.ts` next to `foo.ts`
5. **Follow existing patterns** — Check for `testing.mdc` in IDE rules folder (`.cursor/rules/`, `.claude/rules/`, or `.agent/rules/`), otherwise use patterns below

## What to Test (High Priority)

- Business logic and conditional flows
- Data transformations and parsing
- Edge cases and error handling
- Input validation logic
- Complex utility functions
- Frontend logic (reducers, state machines, pure functions extracted from components)

## SKIP — What NOT to Test

**Do NOT write tests for any of these:**

| Skip | Example |
|------|---------|
| React component rendering | "component renders without crashing" |
| UI appearance | "button has correct class/style" |
| Icon/label mappings | "newsletter group uses newspaper icon" |
| Static config values | "default timeout is 5000" |
| Simple type re-exports | Testing a type alias exists |
| Trivial getters | `getName() { return this.name }` |
| Simple Zod schemas | `z.object({ name: z.string() })` — only test `refine`/`superRefine` with complex logic |

## Mocking Patterns

```ts
// Server-only
vi.mock("server-only", () => ({}));

// Prisma
import prisma from "@/utils/__mocks__/prisma";
vi.mock("@/utils/prisma");

// Use existing helpers
import { getEmail, getEmailAccount, getRule } from "@/__tests__/helpers";
```

## Workflow

### Step 0: Determine Scope

Auto-detect: staged → branch diff → specified files

```bash
# Check staged files
git diff --cached --name-only

# Or check branch diff
git diff main...HEAD --name-only

# Or use specific files provided by user
```

### Step 1: Identify Test Targets

Look for functions with:
- Conditional logic (if/else, switch)
- Data transformation
- Error handling paths
- Multiple return scenarios

**Example:** A function that validates email and formats it differently based on domain is a good candidate. A function that just returns a constant is not.

### Step 2: Create Test File

Place next to source: `utils/example.ts` → `utils/example.test.ts`

**Basic Structure:**

```ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { yourFunction } from "./example";

// Mock external dependencies at the top
vi.mock("server-only", () => ({}));

describe("yourFunction", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("handles happy path", () => {
    // Test main success case
  });

  it("handles edge case", () => {
    // Test boundary conditions
  });

  it("handles error case", () => {
    // Test error paths
  });
});
```

**Complete Example:**

```ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { validateEmail, formatUserData } from "./user-utils";

vi.mock("server-only", () => ({}));

describe("validateEmail", () => {
  it("returns true for valid email", () => {
    expect(validateEmail("user@example.com")).toBe(true);
  });

  it("returns false for invalid email", () => {
    expect(validateEmail("not-an-email")).toBe(false);
  });

  it("handles null/undefined", () => {
    expect(validateEmail(null)).toBe(false);
    expect(validateEmail(undefined)).toBe(false);
  });
});

describe("formatUserData", () => {
  it("transforms user object correctly", () => {
    const input = { firstName: "John", lastName: "Doe", age: 30 };
    const expected = { name: "John Doe", age: 30 };
    expect(formatUserData(input)).toEqual(expected);
  });

  it("handles missing fields", () => {
    const input = { firstName: "John" };
    expect(() => formatUserData(input)).toThrow("lastName is required");
  });
});
```

**For Async Functions:**

```ts
describe("fetchUserData", () => {
  it("returns user data on success", async () => {
    const mockData = { id: 1, name: "John" };
    vi.mocked(prisma.user.findUnique).mockResolvedValue(mockData);
    
    const result = await fetchUserData(1);
    expect(result).toEqual(mockData);
  });

  it("throws error when user not found", async () => {
    vi.mocked(prisma.user.findUnique).mockResolvedValue(null);
    
    await expect(fetchUserData(999)).rejects.toThrow("User not found");
  });
});
```

### Step 3: Run Tests

```bash
cd apps/web && pnpm test --run
```

**Run specific test file:**
```bash
cd apps/web && pnpm test --run utils/example.test.ts
```

**Run in watch mode (for development):**
```bash
cd apps/web && pnpm test utils/example.test.ts
```

Do NOT use sandbox for test commands.

## Test Quality Checklist

Before finishing, verify each test:
- [ ] Tests behavior, not implementation
- [ ] Would catch a real bug if logic changed
- [ ] Doesn't duplicate another test
- [ ] Isn't testing framework/library code
- [ ] Has clear, descriptive test names
- [ ] Tests one thing per `it()` block
- [ ] Uses appropriate assertions (`toBe`, `toEqual`, `toThrow`, etc.)

## Step 4: Summary

After writing tests, provide a brief summary:

```
Tests written for `utils/example.ts`:

Covered:
- validateInput: null handling, invalid format, valid input
- transformData: empty array, nested objects, error case

Not covered (and why):
- getConfig: static values only, no logic to test
- CONSTANTS export: no behavior to test

Run coverage? (y/n)
```

## Optional: Coverage

If requested, run coverage to identify gaps:

```bash
cd apps/web && pnpm test --run --coverage -- path/to/file.test.ts
```

**Understanding Coverage:**
- **Line coverage**: Which lines of code were executed
- **Branch coverage**: Which if/else paths were taken
- **Function coverage**: Which functions were called
- Aim for 80%+ on logic-heavy code, but don't obsess over 100%

## Common Patterns

### Testing Error Cases

```ts
it("throws error for invalid input", () => {
  expect(() => processData(null)).toThrow("Input is required");
  expect(() => processData("")).toThrow("Input cannot be empty");
});
```

### Testing with Mocks

```ts
import prisma from "@/utils/__mocks__/prisma";

it("calls database with correct parameters", async () => {
  await createUser({ name: "John" });
  expect(prisma.user.create).toHaveBeenCalledWith({
    data: { name: "John" }
  });
});
```

### Testing Edge Cases

```ts
it("handles empty array", () => {
  expect(processItems([])).toEqual([]);
});

it("handles very large numbers", () => {
  expect(calculate(Number.MAX_SAFE_INTEGER)).toBeDefined();
});

it("handles special characters", () => {
  expect(sanitize("test@#$%")).toBe("test");
});
```
