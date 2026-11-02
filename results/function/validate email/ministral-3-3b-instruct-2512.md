# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here’s a TypeScript utility function `validateEmail` that checks if an input string is a valid email address using a regex pattern, along with explanations of its use in form validation:

### **TypeScript Utility Function**
```typescript
/**
 * Validates whether a given string is a properly formatted email address.
 * @param email - The email string to validate.
 * @returns `true` if the email is valid, `false` otherwise (including empty strings).
 */
function validateEmail(email: string): boolean {
    // Regex pattern for basic email validation (RFC 5322 simplified)
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Handle edge cases: empty string or non-string input
    if (!email || typeof email !== 'string') {
        return false;
    }

    return emailRegex.test(email);
}

// Type guard for stricter validation (optional)
function isValidEmail(email: unknown): email is string {
    return validateEmail(String(email));
}
```

---

### **How It Works**
1. **Regex Breakdown**:
   - `^[a-zA-Z0-9._%+-]+` → Matches the local part (before `@`) of an email.
   - `@[a-zA-Z0-9.-]+` → Matches the domain name (after `@`).
   - `\.[a-zA-Z]{2,}$` → Ensures a valid TLD (e.g., `.com`, `.org`).

2. **Edge Cases**:
   - Returns `false` for empty strings or non-string inputs.
   - Rejects malformed emails like `"user@.com"` or `"invalid-email"`.

3. **Type Guard (`isValidEmail`)**:
   - Useful in TypeScript when checking if a value is a valid email string (e.g., `if (isValidEmail(userInput))`).

---

### **Usage in Form Validation**
This function can be integrated into a form validation system like this:

#### **Example: React Hook Form Integration**
```typescript
import { useFormContext, Controller } from 'react-hook-form';

function MyForm() {
    const { control, handleSubmit } = useFormContext();

    const onSubmit = (data: any) => console.log(data);

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Controller
                name="email"
                control={control}
                rules={{ required: "Email is required", validate: validateEmail }}
                render={({ field }) => (
                    <input {...field} type="email" placeholder="Enter email" />
                )}
            />
            <button type="submit">Submit</button>
        </form>
    );
}
```

#### **Key Benefits**:
- **Reusable**: Validates emails across components.
- **Type-Safe**: Helps catch invalid inputs early (e.g., `null` or non-strings).
- **Extensible**: Can be customized for stricter rules (e.g., enforce 256 chars, allow subdomains).

#### **Limitations**:
- The regex is simplified; real-world validation may need adjustments (e.g., support for internationalized domains). For production, consider libraries like [`validator`](https://www.npmjs.com/package/validator) or use a dedicated email validation API.

233 t/s, 707 tokens, 3s, 8%
