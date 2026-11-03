# Qwen3 14B
Model: qwen/qwen3-14b
Test: Function Validate Email
Created: 11/03/2026, 01:06:15 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is a TypeScript utility function called `validateEmail` that uses a regular expression to validate an email address:

```typescript
function validateEmail(email: string): boolean {
  // Regular expression pattern for basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Check if the input is empty or not a string
  if (typeof email !== 'string' || email.trim() === '') {
    return false;
  }

  // Test against the regex pattern
  return emailRegex.test(email);
}
```

---

### ✅ **Explanation of Key Parts**

- **Regular Expression**: `^[^\s@]+@[^\s@]+\.[^\s@]+$`  
  - Checks that:
    - The local part (before `@`) doesn't contain spaces or `@`.
    - There's exactly one `@` symbol.
    - The domain part has a valid format and contains at least one dot (`.`).

- **Edge Case Handling**:
  - Ensures the input is not an empty string or undefined.
  - Uses `.trim()` to handle leading/trailing whitespace.

---

### 📌 **Usage in a Form Validation System**

This function can be used within a form validation system like this:

```typescript
function validateForm(formData: { email: string }): boolean {
  if (!validateEmail(formData.email)) {
    console.error("Invalid email address");
    return false;
  }
  // Proceed with further validations or submission
  return true;
}
```

This function could be part of a form validation library, used in conjunction with React hooks (e.g., `useState`, `useEffect`), or integrated into an Angular or Vue form system.

---

### 📝 **Note on Regex Limitations**

The regex used here is **basic** and may not cover all valid email formats according to RFC 5322 standards (which are quite complex). However, it works well for most common use cases in web forms. For stricter validation, more advanced regex or libraries like [`validator.js`](https://github.com/validatorjs/validator) can be used.

80 t/s, 443 tokens, 6s
