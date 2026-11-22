# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: Function Validate Email
Created: 11/22/2026, 02:51:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

```ts
/**
 * Validates an email address using a regex pattern.
 * Returns true if the input is a valid email format, false otherwise.
 */
export function validateEmail(email: string): boolean {
  // Type guard to ensure we're dealing with a primitive string (not undefined/null)
  if (!isStringPrimitive(email)) return false;

  const pattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

  return pattern.test(email);
}

/**
 * Simple type guard to distinguish between a primitive string and other types.
 */
function isStringPrimitive(value: unknown): value is string {
  return typeof value === 'string' && value.length > 0;
}
```

### How it could be used in a form validation system

In a React/Vue/Svelte or plain JS form, you’d call `validateEmail` whenever the user changes an email input field:

- On blur (when they leave the field) to give immediate feedback.
- Before submitting the entire form to ensure all required fields pass their validators.

Example (React-like):

```tsx
const [email, setEmail] = useState('');

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const value = e.target.value;
  setEmail(value); // update state
};

const handleSubmit = async () => {
  if (!validateEmail(email)) {
    alert('Please enter a valid email address.');
    return;
  }
  // proceed with submission...
};
```

This keeps validation logic centralized, testable, and reusable across your application.

104 t/s, 418 tokens, 4s, 3%
