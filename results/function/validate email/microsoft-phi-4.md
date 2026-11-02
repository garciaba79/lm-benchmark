# Phi 4
Model: microsoft/phi-4
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

To create a TypeScript utility function called `validateEmail`, we can use a regular expression to check the validity of an email address. The function will take a string input and return a boolean indicating whether the email is valid. We'll also handle edge cases such as empty strings or invalid formats.

Here's how you can implement this:

```typescript
function validateEmail(email: string): boolean {
    // Regular expression for validating an email address
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Check if the input is a non-empty string and matches the regex pattern
    return typeof email === 'string' && email.trim() !== '' && emailRegex.test(email);
}

// Example usage:
console.log(validateEmail("example@example.com")); // true
console.log(validateEmail("invalid-email"));       // false
console.log(validateEmail(""));                    // false
console.log(validateEmail("user@domain.co"));      // true
console.log(validateEmail("user@domain.c"));       // false
```

### Explanation:

1. **Regular Expression**: The regex used here is a common pattern for validating email addresses:
   - `^[a-zA-Z0-9._%+-]+`: Matches the local part of the email, allowing letters, digits, and certain special characters.
   - `@[a-zA-Z0-9.-]+`: Ensures there's an "@" symbol followed by the domain name, which can include letters, digits, dots, and hyphens.
   - `\.[a-zA-Z]{2,}$`: Matches a dot followed by at least two alphabetic characters for the top-level domain.

2. **Type Guards**: We use `typeof email === 'string'` to ensure the input is a string and `email.trim() !== ''` to handle empty strings or strings with only whitespace.

3. **Edge Cases**: The function handles:
   - Empty strings.
   - Strings with only spaces.
   - Invalid formats that don't match the regex pattern.

### Usage in Form Validation:

In a form validation system, this utility function can be used to validate user input for email fields before submission. Here's how it might be integrated:

- **Frontend**: When a user submits a form, the `validateEmail` function can be called to check if the entered email is valid. If not, an error message can be displayed, and the form submission can be prevented until the user corrects the input.

- **Backend**: Before processing data or storing it in a database, you can use this function on the server side to ensure that only valid emails are accepted. This adds an extra layer of validation beyond client-side checks.

By using this utility function, developers can maintain consistent email validation logic across different parts of their application, ensuring robust and reliable input handling.

82 t/s, 590 tokens, 7s, 4%
