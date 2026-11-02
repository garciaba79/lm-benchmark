# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here's a well-documented TypeScript utility function `validateEmail` that performs basic validation of an email address using a regular expression. It handles edge cases such as empty strings and invalid formats, and can be integrated into form validation systems.

---

### ✅ **Function Definition**

```typescript
function validateEmail(email: string): boolean {
  // Check for empty input (length 0)
  if (email.length === 0) {
    return false;
  }

  // Regular expression to match a basic email format:
  // - Local part can include letters, numbers, dots, underscores, hyphens, %, +, and -
  // - Domain part includes letters, numbers, dots, and hyphens
  // - Must end with a dot followed by at least two alphabetic characters (TLD)
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  return emailRegex.test(email);
}
```

---

### 🔍 **Explanation of the Regex**

The regular expression used is:

```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

- `^` and `$`: Anchors to ensure the entire string matches.
- `[a-zA-Z0-9._%+-]+`: Matches the **local part** of the email (before the `@`) — allows common characters like letters, digits, dots, underscores, hyphens, `%`, and `+`.
- `@`: The literal `@` symbol that separates local and domain parts.
- `[a-zA-Z0-9.-]+`: Matches the **domain part** before the TLD (top-level domain).
- `\.`: A literal dot to separate the domain from the TLD.
- `[a-zA-Z]{2,}`: Ensures the **TLD** is at least two alphabetic characters long.

---

### 🧪 **Examples of Valid and Invalid Emails**

| Input                          | Result |
|-------------------------------|--------|
| `"test@example.com"`          | ✅ True |
| `""`                          | ❌ False (empty string) |
| `"   "`                       | ❌ False (non-empty but invalid format) |
| `"user@domain"`               | ❌ False (no TLD) |
| `"user@sub.domain.co.uk"`     | ✅ True |
| `"user+name@example.com"`     | ✅ True |
| `"user.name@example.com"`     | ✅ True |
| `"user@.com"`                 | ❌ False (invalid domain format) |

---

### 📦 **Use in a Form Validation System**

This function can be used to validate email fields in web forms, particularly in front-end frameworks like React or Angular.

#### Example: In a React Component

```tsx
import React, { useState } from 'react';

const EmailForm = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateEmail(email)) {
      setError('Please enter a valid email address.');
    } else {
      setError('');
      // Proceed with form submission
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Submit</button>
    </form>
  );
};
```

---

### 📌 **Notes**

- This function does not handle **internationalized domain names (IDN)** or **emails with special Unicode characters**.
- It assumes the input is a string and does not perform additional type checks — this is enforced by TypeScript's static typing.

This utility provides a solid foundation for email validation in most common use cases.

9 t/s, 8033 tokens, 862s, 99%
