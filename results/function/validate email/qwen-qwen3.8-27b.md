# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Function Validate Email
Created: 11/03/2026, 01:43:02 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

```typescript
/**
 * Validates whether the given string is a syntactically correct email address.
 *
 * @param input - The string to validate.
 * @returns true if the string is a valid email address, false otherwise.
 */
function validateEmail(input: unknown): boolean {
    // Type guard: ensure the input is a string before proceeding
    if (typeof input !== 'string') {
        return false;
    }

    // Trim leading/trailing whitespace to handle inputs with accidental spaces
    const trimmed = input.trim();

    // Handle empty strings
    if (trimmed.length === 0) {
        return false;
    }

    // RFC 5322 simplified regex for common email validation.
    // This regex handles:
    // - One or more local-part characters (alphanumeric, dots, underscores, hyphens, plus signs)
    // - An @ symbol
    // - One or more domain characters (alphanumeric, dots, hyphens)
    // - A dot-separated TLD of at least two characters
    // This is intentionally permissive to allow valid but unusual emails while rejecting obviously invalid ones.
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    return emailRegex.test(trimmed);
}

export { validateEmail };
```

### Usage in a Form Validation System

In a form validation system, `validateEmail` would typically be used as part of a field-level validator. For example, when a user submits a registration form, the frontend or backend validation pipeline would call `validateEmail` on the email field. If it returns `false`, the system can display an inline error message such as "Please enter a valid email address" and prevent form submission. On the backend, this serves as a first-line check before any more complex validation (like checking for existing accounts or sending a verification email). Because it handles non-string inputs and edge cases like empty strings, it can be safely integrated into generic validation pipelines without additional guards, making it reusable across multiple forms and APIs.

17 t/s, 456 tokens, 27s
