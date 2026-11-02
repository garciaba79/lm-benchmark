# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

**TypeScript utility**

```ts
// ------------------------------------------------------------------
// 1️⃣  Validation function – pure logic only
// ------------------------------------------------------------------
export const validateEmail = (email: string): boolean => {
  // Guard against non‑string or empty input early
  if (!email || typeof email !== 'string' || email.trim() === '') {
    return false;
  }

  // A reasonably strict but still practical regex.
  //   ^[^\s@]+          – at least one character before the @ (no spaces)
  //   @                 – the literal “@” symbol
  //   [^\s@]+\.          – one or more non‑space/“@” chars, then a dot
  //   [^\s@]+$           – domain part, ending with another non‑space/“@”
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return emailPattern.test(email);
};

// ------------------------------------------------------------------
// 2️⃣  Type guard that narrows the argument to a valid e‑mail string
// ------------------------------------------------------------------
export const isValidEmail = (email: unknown): email => {
  // The function returns `true` only when the value satisfies the pattern.
  return validateEmail(email);
};

/* Example usage:
   const userInput = "john.doe@example.com";
   if (isValidEmail(userInput)) {
     console.log('✅ Valid e‑mail');
   } else {
     console.log('❌ Invalid e‑mail');
   }
*/
```

### Why the two pieces?

| Piece | Purpose |
|------|---------|
| `validateEmail` | Pure function that **does** validation. It can be unit‑tested in isolation and works on any string (or non‑string) input safely. |
| `isValidEmail`   | A **type guard**. When you call it, TypeScript knows the argument is of type `email`. This lets callers use the value with tighter typing without extra conversion (`as string`). |

---

## How to use it in a form validation system

```ts
// Form handling component (React‑like pseudo‑code)
function handleSubmit(form: HTMLFormElement) {
  const emailInput = form.email.value as string;

  // Directly call the type guard – TypeScript knows `email` is valid.
  if (!isValidEmail(emailInput)) {
    // Show a user‑friendly error
    alert('Please enter a valid e‑mail address.');
    return;
  }

  // At this point we can safely parse or store the value as an e‑mail string.
  console.log('User submitted:', emailInput);
}
```

* **Error handling** – If the regex fails (empty, missing `@`, invalid domain, etc.) `isValidEmail` returns `false`, and you can display a validation message.  
* **Type safety** – The guard narrows `email: unknown` → `email`, so you never accidentally treat an invalid string as a proper e‑mail later in the codebase.  
* **Performance** – The check is performed once per submission, keeping the UI responsive.

---

### Edge cases handled

| Input | Result | Reason |
|-------|--------|--------|
| `''` (empty) | `false` | Trimmed empty → invalid |
| `null`, `undefined` | `false` | Non‑string guard catches them |
| `"   "` (spaces only) | `false` | Trimmed to empty → invalid |
| `"john..doe@example.com"` | `true` | Regex allows consecutive dots inside the local part |
| `"user@[invalid]"` | `false` | Domain part must end with a dot, not just brackets |
| `["not", "a", "string"]` | `false` | Not a string → guard returns false |

Feel free to tweak the regex (`/^[^\s@]+@[^\s@]+\.[^\s@]+$/`) if you need stricter or more permissive e‑mail validation (e.g., allowing internationalized domains). The type guard remains valid regardless of which regex you choose.

226 t/s, 1031 tokens, 5s, 7%
