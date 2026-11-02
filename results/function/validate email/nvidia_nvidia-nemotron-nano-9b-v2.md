# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here's a TypeScript utility function `validateEmail` that checks if a string is a valid email address using a regular expression, handles edge cases like empty strings, and includes type guards implicitly through its return type:

```typescript
function validateEmail(input: string): boolean {
  const trimmed = input.trim();
  if (trimmed === '') {
    return false; // Reject empty or whitespace-only inputs
  }
  // Regex pattern explanation:
  // - Local part: allows letters, numbers, and special characters ._%+-
  // - Domain part: requires at least one dot and a TLD of 2+ letters
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(trimmed);
}
```

### How to Use in a Form Validation System:
1. **Real-time validation**: Attach this function to an email input field's `onChange` or `onBlur` event to validate as the user types.
2. **Form submission check**: Call `validateEmail(emailInput.value)` before form submission. If it returns `false`, prevent submission and show an error message.
3. **Error feedback**: Display a user-friendly message like "Please enter a valid email address" when validation fails.

### Example Usage:
```typescript
const emailInput = document.getElementById('email') as HTMLInputElement;
emailInput.addEventListener('input', () => {
  const isValid = validateEmail(emailInput.value);
  if (!isValid) {
    emailInput.setCustomValidity('Invalid email format');
  } else {
    emailInput.setCustomValidity('');
  }
});
```

This function balances simplicity and practicality, covering most common email formats while rejecting clearly invalid cases. For stricter validation (e.g., checking DNS records), additional steps would be required.

103 t/s, 3276 tokens, 32s, 20%
