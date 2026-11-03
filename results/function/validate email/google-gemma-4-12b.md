# Gemma 4 12B
Model: google/gemma-4-12b
Test: Function Validate Email
Created: 11/03/2026, 12:56:51 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is the TypeScript implementation of the `validateEmail` utility.

### The Implementation

```typescript
/**
 * A type guard that checks if a string is a valid email address.
 * 
 * @param email - The string to validate.
 * @returns boolean indicating if the format is valid.
 */
export function validateEmail(email: unknown): email is string {
  // Edge case: Handle non-string inputs or empty/whitespace strings
  if (typeof email !== 'string' || email.trim().length === 0) {
    return false;
  }

  /**
   * This regex checks for a standard format: 
   * localPart @ domain . extension
   */
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  const trimmedEmail = email.trim();
  return emailRegex.test(trimmedEmail);
}

// --- Examples of usage ---
console.log(validateEmail("user@example.com")); // true
console.log(validateEmail("invalid-email"));    // false
console.log(validateEmail(""));                 // false
console.log(validateEmail(12345));              // false (Type guard handles non-strings)
```

### Key Technical Decisions:

1.  **Type Guard (`email is string`)**: By using a Type Guard instead of just returning `boolean`, TypeScript's compiler knows that if the function returns `true`, the variable is definitely a string. This prevents "Type 'unknown' is not assignable to type 'string'" errors later in your code.
2.  **Input Handling (`unknown`)**: I used `unknown` as the input type rather than `string`. This makes the function more robust because it can safely handle unexpected types (like numbers or nulls) coming from API responses without crashing the application.
3.  **Trim Logic**: The `.trim()` method ensures that accidental leading or trailing spaces (common when users copy-paste into forms) don't cause a valid email to fail validation.

---

### How to use this in a Form Validation System

In a real-world production app, this function would serve as the "logic layer" inside your UI components or form handlers. Here are three ways it can be integrated:

#### 1. Immediate Feedback (UX)
When a user types into an input field, you can call `validateEmail` on every keystroke (debounced). If it returns `false`, you can highlight the input box in red and display a message like *"Please enter a valid email address."*

#### 2. Schema Validation (Backend/Validation Libraries)
If using a library like **Zod** or **Joi**, you can wrap this logic into a custom refinement. For example, with Zod:
```typescript
const RegisterSchema = z.object({
  email: z.string().refine(validateEmail, {
    message: "Invalid email format",
  }),
});
```

#### 3. Submission Guard (Final Check)
Before sending data to an API, you can run a validation pass over the entire form object. If `validateEmail` returns `false` for any field, the "Submit" button remains disabled or triggers a summary of errors at the top of the page.

82 t/s, 726 tokens, 9s
