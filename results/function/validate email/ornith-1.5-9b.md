# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here's a robust implementation with type guards and edge-case handling:

```typescript
/**
 * Type guard that narrows an unknown value to `string` at compile time.
 */
function isString(value: unknown): value is string {
  return typeof value === "string";
}

/**
 * Validates whether the given input is a valid email address.
 *
 * @param input - The value to validate (any type; non-strings are rejected).
 * @returns `true` if the input is a non-empty, well-formed email address.
 */
export function validateEmail(input: unknown): boolean {
  // Type guard: reject anything that isn't a string early.
  if (!isString(input)) {
    return false;
  }

  const trimmed = input.trim();

  // Reject empty / whitespace-only strings before running the regex.
  if (trimmed.length === 0) {
    return false;
  }

  // Basic email pattern: local-part@domain.tld
  const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return EMAIL_REGEX.test(trimmed);
}
```

### How the pieces work

- **Type guard (`isString`)** — By accepting `unknown` and narrowing with a type predicate, TypeScript lets you safely treat the value as a string *inside* the function while rejecting `null`, `undefined`, numbers, etc. at runtime. This is more defensive than just typing the parameter as `string`.
- **Trimming** — User input often has stray whitespace; trimming before validation avoids false negatives (e.g. `" user@x.com "`). You can drop this if you want to *reject* malformed spacing instead.
- **Empty-string check** — Guards against `""` and `"   "`, which the regex alone would also reject, but checking explicitly gives a clearer failure path.
- **Regex** — `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` requires a non-empty local part, an `@`, then a domain with at least one dot and no whitespace. It correctly rejects cases like `a@@b.com`, `user@domain` (no TLD), or `spaces here@example.com`.

### Using it in a form validation system

```typescript
interface SignupForm {
  email: string;
}

function validateSignup(form: SignupForm): Record<string, string> {
  const errors: Record<string, string> = {};

  if (!validateEmail(form.email)) {
    errors.email = "Please enter a valid email address.";
  }

  return errors;
}
```

You can then drive UI updates from the returned `errors` object (e.g. show red text under the field). In real projects you'd typically wire this into a library:

- **React Hook Form** — pass it as a validation function to `useForm({ mode: "onChange" })`.
- **Zod** — use `.email()` or `.refine(() => validateEmail(value), {...})` for schema-level validation.
- **Vuelidate / Yup** — register it as an async/validator rule.

### A note on the regex trade-off

This pattern is a good balance of simplicity and coverage, but it's not full RFC 5322 compliance. It won't catch things like invalid domain names (`user@exa mple.com`), reserved TLDs, or length limits. If you need stricter validation (e.g. requiring a valid TLD), use:

```typescript
const STRICT_REGEX = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/;
```

For truly rigorous email verification, consider sending a confirmation link — regex alone can never fully validate an address that doesn't exist yet.

134 t/s, 2527 tokens, 19s, 16%
