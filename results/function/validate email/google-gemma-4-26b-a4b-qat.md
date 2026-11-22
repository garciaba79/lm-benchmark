# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Function Validate Email
Created: 11/22/2026, 03:01:31 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is a robust implementation of the `validateEmail` utility in TypeScript.

### The Implementation

```typescript
/**
 * A Type Guard that checks if a value is a non-empty string.
 * This helps narrow down types before running heavy regex logic.
 */
function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

/**
 * Validates an email address using a regular expression.
 * 
 * @param email - The string to validate.
 * @returns A boolean indicating if the email is valid.
 */
export const validateEmail = (email: unknown): boolean => {
  // 1. Handle edge cases: check if input is a non-empty string
  if (!isNonEmptyString(email)) {
    return false;
  }

  /**
   * Regex breakdown:
   * ^[^@\s]+          -> Starts with one or more characters that are not @ or whitespace
   * @                 -> A literal @ symbol
   * [^@\s]+           -> Followed by one or more characters that are not @ or whitespace (domain name)
   * \.                -> A literal dot
   * [^@\s]{2,}$       -> Ends with at least two characters that are not @ or whitespace (TLD)
   */
  const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/;

  return emailRegex.test(email.trim());
};

// --- Test Cases ---
console.log(validateEmail("user@example.com")); // true
console.log(validateEmail("user.name+tag@sub.domain.org")); // true
console.log(validateEmail(""));                 // false (empty string)
console.log(validateEmail(null));               // false (not a string)
console.log(validateEmail("plainaddress"));     // false (invalid format)
console.log(validateEmail("@missinguser.com")); // false (invalid format)
console.log(validateEmail("user@domain"));      // false (missing TLD)
```

### Key Features

1.  **Type Safety (`unknown` & Type Guards):** Instead of accepting just `string`, I used `unknown`. This makes the function "defensive." If a developer accidentally passes `null` or an `object` from an API response, the function won't crash; it will simply return `false`. The `isNonEmptyString` function acts as a **Type Guard**, narrowing the type from `unknown` to `string` safely.
2.  **Edge Case Handling:** 
    *   **Whitespace:** It uses `.trim()` to ensure that an email like `" user@example.com "` is treated as valid.
    *   **Empty Strings:** It explicitly rejects empty strings or strings containing only spaces.
    *   **Regex Complexity:** The regex used is a "practical" regex. While it's not the 100% exhaustive RFC 5322 standard (which is massive and overkill for most web apps), it prevents the most common errors without being computationally expensive or overly restrictive.

---

### Use in a Form Validation System

In a real-world application (like a React, Vue, or Angular form), this utility would typically be used in one of three ways:

#### 1. On Input Change (Real-time Feedback)
As the user types, you can call this function to toggle an error state. This provides immediate UX feedback (e.g., turning the input border red if the format is invalid).
```typescript
const onEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const isValid = validateEmail(e.target.value);
  setEmailError(!isValid && e.target.value.length > 0);
  setEmail(e.target.value);
};
```

#### 2. On Form Submission (Final Gatekeeper)
Before sending data to an API, you run the function to prevent unnecessary network requests.
```typescript
const handleSubmit = async (formData: FormData) => {
  if (!validateEmail(formData.email)) {
    alert("Please enter a valid email address.");
    return;
  }
  // Proceed with API call...
};
```

#### 3. Schema Validation Integration
If you are using a library like **Zod** or **Yup** for schema validation, this function can be wrapped into a custom validator to ensure your entire form object is valid before it ever reaches your backend.

55 t/s, 999 tokens, 18s, 7%
