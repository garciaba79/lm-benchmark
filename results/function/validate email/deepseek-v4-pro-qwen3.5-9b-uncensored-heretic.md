# DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic
Model: deepseek-v4-pro-qwen3.5-9b-uncensored-heretic
Test: Function Validate Email
Created: 11/18/2026, 11:42:41 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is a TypeScript utility function that validates email addresses using a robust regular expression, along with an explanation of its use in form validation.

### TypeScript Utility Function

```typescript
/**
 * Validates whether a given string is a valid email address.
 * 
 * @param input - The string to validate.
 * @returns true if the input is a valid email, false otherwise.
 */
export function validateEmail(input: unknown): boolean {
  // Type guard: Ensure the input is actually a string before proceeding
  if (typeof input !== 'string') {
    return false;
  }

  const trimmedInput = input.trim();

  // Edge case: Empty or whitespace-only strings are invalid
  if (trimmedInput.length === 0) {
    return false;
  }

  // Regex explanation:
  // ^                    : Start of string
  // [a-zA-Z0-9._%+-]+   : One or more alphanumeric characters, dots, underscores, 
  //                     percent signs, plus signs, or hyphens (local part)
  // @                   : Literal @ symbol
  // [a-zA-Z0-9.-]+      : Domain name (alphanumeric, dots, hyphens)
  // \.                  : Literal dot before TLD
  // [a-zA-Z]{2,}        : Top-level domain of at least 2 letters
  // $                    : End of string
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  return emailRegex.test(trimmedInput);
}
```

### How to Use in a Form Validation System

In a form validation system (e.g., using React Hook Form, Zod, or custom logic), this function acts as the core rule for the `email` field. Here is how it integrates:

1. **On Input Change**: When a user types into an email input field, call `validateEmail(value)` to provide real-time feedback (e.g., showing a green checkmark or red error message).
2. **On Submission**: Before submitting the form data to your backend API, run this function on every email field value. If it returns `false`, reject the submission and display an error like "Please enter a valid email address."
3. **Type Safety**: Because of the type guard (`typeof input !== 'string'`), if you accidentally pass a number or null to your form handler, the validation gracefully fails instead of crashing with a runtime error.

**Example usage in a React component:**

```tsx
import { useState } from 'react';
import { validateEmail } from './utils/emailValidator';

function ContactForm() {
  const [email, setEmail] = useState('');
  const isValid = validateEmail(email);

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <label>Email Address</label>
      <input 
        type="text" 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      {isValid ? (
        <span style={{ color: 'green' }}>✓ Valid email format</span>
      ) : (
        <span style={{ color: 'red' }}>✗ Invalid or empty email</span>
      )}
      
      <button type="submit" disabled={!isValid}>
        Submit
      </button>
    </form>
  );
}
```

### Key Edge Cases Handled
- **Empty/Whitespace**: Returns `false` for strings that are empty or contain only spaces.
- **Type Safety**: Explicitly checks if the input is a string, preventing crashes from non-string inputs (like `null`, `undefined`, or numbers).
- **Format Strictness**: The regex ensures there is exactly one `@` symbol, no consecutive dots in the domain, and a valid TLD length.

139 t/s, 850 tokens, 6s
