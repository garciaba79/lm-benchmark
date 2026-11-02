# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Below is a self‑contained, production‑ready TypeScript utility that validates an e‑mail address using a regular expression.  
It guards against non‑string inputs, trims whitespace, and returns `false` for empty or malformed values. A tiny **type guard** (`isString`) is included to make the intent explicit when you call the function from different typed contexts.

---  

## 📦 Code  

```ts
/**
 * Simple type guard that checks if a value is a string (as opposed to any other type).
 * This can be useful when your validation routine receives values of mixed types,
 * e.g. from form inputs converted to unknown via TS‑any or generic helpers.
 */
function isString(value: unknown): value is string {
  // Fast path for primitives that are definitely not strings.
  if (typeof value !== 'string') return false;
  return true;
}

/**
 * Returns `true` if the supplied e‑mail address looks like a valid one,
 * otherwise returns `false`. The implementation:
 *  • trims surrounding whitespace,
 *  • rejects empty strings or falsy values,
 *  • uses a reasonably strict RFC‑compatible regular expression.
 *
 * **Note:** Full RFC 5322 validation is far more complex and rarely needed in UI.
 * The pattern below catches the vast majority of everyday addresses while staying fast.
 */
function validateEmail(input: unknown): boolean {
  // Guard against non‑string input early.
  if (!isString(input)) return false;

  const email = String(input).trim();      // Defensive trimming
  if (email.length === 0) return false;    // Empty after trim? → invalid

  /**
   * RegExp explanation:
   *
   *  ^                          – start of string
   *  [a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]+ – local part, allows most special chars but not spaces or control characters.
   *  @                           – at‑sign separating local and domain parts
   *  (?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?|         // first label of the domain (max 63 chars)
   *       [a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?)           // or second/third labels with hyphens allowed only inside
   *  \.                         – dot before TLD
   *  [a-zA-Z]{2,}               – top‑level domain (at least two letters)
   *  $                          – end of string
   *
   * This pattern matches typical user‑entered e‑mail addresses and blocks obvious typos.
   */
  const emailRegex = new RegExp(
    /^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}$/
  );

  return emailRegex.test(email);
}

/* Exported for module bundlers or separate import paths */
export const validateEmail = validateEmail;
```

---  

## 🛠️ How to use it in a form‑validation pipeline  

### 1️⃣ Inline validation (React, Vue, plain JavaScript)

```tsx
import React from 'react';
import { isString, validateEmail } from './emailValidator';

function EmailInput({ onChange, value, errorMessage }: {
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  value?: string;
  errorMessage?: string;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!isString(e.target.value) || !validateEmail(e.target.value)) {
      // Mark the field invalid; UI can store an error flag elsewhere
      console.warn('Invalid e‑mail', e.target.value);
    } else {
      console.log('Valid e‑mail:', e.target.value);
    }

    onChange(e);
  };

  return (
    <input
      type="email"
      value={value ?? ''}
      onChange={handleChange}
      // You could conditionally render an error message based on a stored flag here.
      {...{ aria-invalid: !isString(value) || !validateEmail(value) }}
    />
  );
}
```

### 2️⃣ Central validation hook (e.g., in a React Hook Form controller)

```tsx
import { Controller, useFormContext } from 'react-hook-form';
import { validateEmail } from './emailValidator';

export function RegisterForm() {
  const { control, triggerSubmit, submitting } = useFormContext();

  // Custom validation that runs when the field loses focus or on submit.
  const emailValidationRule = (value: unknown) => ({
    type: value instanceof String ? 'valid' : validateEmail(value as string) ? true : false,
    // If you need a custom message for the rule set it here:
    // when: submit,
  });

  <Controller
    name="email"
    control={control}
    rules={{ email: emailValidationRule }}
    render={({ field: { value, onBlur, onChange }, register }) => (
      <>
        <input type="text" {...register('email')} value={value as string} onChange={onChange} onBlur={() => onBlur()} placeholder="you@example.com"/>
        {/* Conditional error rendering */}
        {(field.error?.type !== undefined) && field.error?.message && (
          <span className="error">{field.error.message}</span>
        )}
      </>
    )}
  />

  <button type="submit" disabled={submitting}>Submit</button>
}
```

### 3️⃣ Plain JavaScript / Node utility  

```js
// emailValidator.ts compiled to ES module or bundled with TypeScript:
export const validateEmail = function(input) {
  if (typeof input !== 'string') return false;
  let email = String(input).trim();
  if (!email) return false;

  // Same regex as the TS version above.
  const re = /^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}$/;
  return re.test(email);
};

// Example usage:
if (!validateEmail('john@example.com')) console.error('Bad address');
```

---  

## 📚 Why this works well in a form system  

| ✅ Feature | How it helps validation flow |
|---|---|
| **Input type guard (`isString`)** | Prevents accidental `null`, `undefined`, numbers, or objects from slipping through. You can also combine it with other guards (e.g., length) for a comprehensive UI‑level check. |
| **Trimming** | Users often paste addresses that contain leading/trailing spaces; trimming normalises the value before testing. |
| **Regex is anchored (`^…$`)** | Guarantees the whole string matches, not just a substring (e.g., it won’t flag `"example.com"` as valid). |
| **Reasonable TLD rule (`\.[a-zA-Z]{2,}`)** | Rejects domain‑only strings and short gTLDs like `.x` that are not real e‑mail domains. |
| **Fast native RegExp test** | Runs in virtually constant time even on large forms; no heavyweight parsing of the RFC spec is required for typical UI scenarios. |
| **Return type is boolean** | Allows you to use it directly with framework validators, custom hooks, or simple if‑statements without extra boilerplate. |

---  

### TL;DR  

```ts
import { validateEmail } from './emailValidator';

function handleSubmit(e: React.FormEvent) {
  const email = document.getElementById('email')?.value;
  if (!validateEmail(email)) {
    e.preventDefault();          // Stop submission
    // Show an error UI, focus the field, etc.
  } else {
    // Proceed with submit…
  }
}
```

The utility is tiny, type‑safe, and easy to plug into any frontend or backend validation flow while still covering the most common pitfalls of e‑mail input. Happy coding! 🚀

105 t/s, 3113 tokens, 30s, 20%
