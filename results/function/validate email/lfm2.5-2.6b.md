# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

**TypeScript implementation**

```ts
// ------------------------------------------------------------
// 1️⃣  Regular expression – a reasonably strict email pattern
// ------------------------------------------------------------
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

/**
 * Type‑guard that tells TypeScript “the value is an Email”.
 *
 * The function returns `true` only when the string:
 * • is non‑empty,
 * • contains exactly one '@',
 * • has a domain part with at least one dot (e.g. example.com),
 * • and ends with a top‑level domain of two or more letters.
 */
function isValidEmail(value: string): value is Email {
  // Guard against non‑string inputs (the signature guarantees this, but we keep it explicit)
  if (typeof value !== 'string') return false;

  // Empty / whitespace‑only strings fail the regex – they will be rejected automatically
  if (!value) return false;

  return EMAIL_REGEX.test(value);
}

/**
 * Main utility – returns `true` iff the supplied string is a valid email address.
 *
 * @param email - The candidate e‑mail value.
 * @returns `true` for a well‑formed e‑mail, `false` otherwise.
 */
export function validateEmail(email: string): boolean {
  // `isValidEmail` already does all the heavy lifting (including type checking).
  return isValidEmail(email);
}
```

### How it works

| Step | What happens |
|------|--------------|
| **Input** | A plain JavaScript/TypeScript string is passed to `validateEmail`. |
| **Type guard** | `isValidEmail` first ensures we really have a `string`, then checks the regex. The regex enforces:<br>• local part (`[a-zA-Z0-9._%+-]+`) <br>• exactly one `@` <br>• domain (`[a-zA-Z0-9.-]+`) <br>• at least one dot and a **TLD of ≥ 2 letters** (`\.[a-zA-Z]{2,}`). |
| **Result** | `true` if the string matches, `false` otherwise. Empty strings are rejected because they don’t satisfy the regex (and we explicitly check `!value`). |

---

## Using it in a form‑validation system

```tsx
// Example: plain JavaScript/TypeScript form handler (works with React, Angular, etc.)
function onSubmit(event: Event) {
  const input = event.target as HTMLInputElement;

  if (!validateEmail(input.value)) {
    // Show an error message – e.g. set a field‑level flag or update the DOM
    console.error('Invalid email address');
    // In React you might do:
    //   setFieldError('email', 'Please enter a valid email');
  } else {
    // The address looks good → proceed with server upload, API call, etc.
    next(Event);
  }
}
```

* **Why use the type guard?**  
  - It lets TypeScript narrow the `value` variable to `Email` inside the function body (useful when you need the raw string later).  
  - It makes future code less error‑prone: if someone accidentally passes a number, the guard will immediately return `false`.

* **Edge cases handled**  
  - Empty string → `false`  
  - `"@example.com"` → fails because there’s no local part (regex requires at least one character before `@`).  
  - `"john.doe@"` → fails (missing domain).  
  - `"john@example"`` → fails (no dot in the domain).  

You can extend the regex (e.g., allow Unicode characters, internationalized domains) without changing the public API of `validateEmail`. The same function remains a safe, reusable utility for any form‑validation flow.

288 t/s, 2219 tokens, 8s, 14%
