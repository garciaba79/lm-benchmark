# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is the TypeScript utility function `validateEmail`.

```typescript
/**
 * Validates an email address using a standard regex pattern.
 *
 * @param input The string to validate.
 * @returns True if the string matches the email format, otherwise false.
 */
export function validateEmail(input: string): boolean {
  // Edge case: Empty strings are not valid emails
  if (input.trim() === '') {
    return false;
  }

  // Regex pattern for a basic email validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  return emailRegex.test(input);
}
```

### How to use it in a form validation system

In a frontend or backend form validation context, you would typically wrap this function in a **custom error** class to provide clear feedback to the user.

Here is an example of how you might integrate it into a component:

```typescript
import { validateEmail } from './emailUtils'; // Import your utility

interface EmailFormError extends Error {
  message: string;
}

class InvalidEmailError extends EmailFormError {
  constructor(message = 'Please enter a valid email address') {
    super(message);
    this.name = 'InvalidEmail';
  }
}

function handleEmailSubmit(email: string) {
  // 1. Validate the input
  if (!validateEmail(email)) {
    throw new InvalidEmailError();
  }

  // 2. Proceed with form submission logic...
}
```

**Why use a utility function here?**
1. **Reusability:** It can be used across different components or services.
2. **Separation of Concerns:** The validation logic is isolated from the UI rendering logic, making your code easier to test and maintain.
3. **Type Safety:** By returning `boolean`, you can easily check if a field is valid before displaying an error message in the UI.

291 t/s, 406 tokens, 1s, 3%
