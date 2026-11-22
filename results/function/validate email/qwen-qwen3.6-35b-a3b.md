# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Function Validate Email
Created: 11/22/2026, 03:13:37 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

```typescript
/**
 * Validates whether the given string is a valid email address.
 * 
 * @param input - The string to validate as an email address.
 * @returns True if the input is a valid email address, false otherwise.
 */
export function validateEmail(input: string | null | undefined): boolean {
  // Handle null, undefined, or empty string cases
  if (input === null || input === undefined || input === '') {
    return false;
  }

  // Trim whitespace and check if the resulting string is empty
  const trimmed = input.trim();
  if (trimmed === '') {
    return false;
  }

  // Regular expression for validating an email address
  // This regex covers most standard email formats:
  // - Local part: allows alphanumeric characters, dots, underscores, percent signs, plus signs, and hyphens
  // - Domain: allows alphanumeric characters, hyphens, and dots
  // - TLD: at least two characters, alphabetic only
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  return emailRegex.test(trimmed);
}

/**
 * Type guard to check if a value is a non-empty string.
 * Useful for narrowing types in conditional blocks.
 * 
 * @param value - The value to check.
 * @returns True if the value is a non-empty string, false otherwise.
 */
export function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim() !== '';
}
```

### Explanation

**How `validateEmail` Works:**

1. **Null/Undefined/Empty Handling**: The function first checks if the input is `null`, `undefined`, or an empty string. These cases immediately return `false` since they cannot represent valid email addresses.

2. **Whitespace Trimming**: The input is trimmed of leading and trailing whitespace. If the trimmed string is empty, it returns `false`.

3. **Regular Expression Validation**: The regex `/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/` validates the email format:
   - `^` and `$` ensure the entire string matches the pattern.
   - `[a-zA-Z0-9._%+-]+` matches the local part (before `@`), allowing common characters.
   - `@` matches the literal at-sign.
   - `[a-zA-Z0-9.-]+` matches the domain name.
   - `\.[a-zA-Z]{2,}` matches the top-level domain (e.g., `.com`, `.org`), requiring at least two alphabetic characters.

4. **Return Value**: Returns `true` if the email matches the pattern, `false` otherwise.

**Type Guard `isNonEmptyString`:**

This utility narrows the type of a value from `unknown` to `string` while also ensuring it's non-empty after trimming. It's useful in conditional logic where you need to guarantee a value is a meaningful string before further processing.

### Usage in a Form Validation System

In a form validation system, `validateEmail` can be used to check user input in real-time or on form submission:

```typescript
// Example: Validating an email field in a form
const emailInput = document.getElementById('email') as HTMLInputElement;
const emailValue = emailInput.value;

if (validateEmail(emailValue)) {
  console.log('Email is valid.');
  // Proceed with form submission or next step
} else {
  console.log('Please enter a valid email address.');
  // Display an error message to the user
}
```

The `isNonEmptyString` type guard can be used when handling potentially untyped data (e.g., from `event.target.value` in some frameworks) to safely narrow the type before passing it to `validateEmail`. This approach ensures robust validation, prevents runtime errors from invalid inputs, and provides clear feedback to users during form interaction.

43 t/s, 884 tokens, 21s, 6%
