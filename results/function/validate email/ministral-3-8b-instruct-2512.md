# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here's a TypeScript utility function `validateEmail` that uses a regular expression to validate email addresses, handles edge cases, and includes type guards:

```typescript
/**
 * Validates an email address using a regular expression.
 * @param email - The email string to validate.
 * @returns A tuple where the first element is a boolean indicating validity,
 *          and the second (if valid) is the normalized email in lowercase.
 */
function validateEmail(email: string): [boolean, string | null] {
    // Handle edge cases
    if (!email || typeof email !== 'string') {
        return [false, null];
    }

    // Trim whitespace and check for empty string after trimming
    const trimmedEmail = email.trim();
    if (trimmedEmail.length === 0) {
        return [false, null];
    }

    // Regular expression for basic email validation
    // This regex follows RFC 5322 standards with some simplifications
    const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const isValid = emailRegex.test(trimmedEmail);

    return [isValid, isValid ? trimmedEmail.toLowerCase() : null];
}

/**
 * Type guard for email validation
 */
function isValidEmail(email: unknown): email is string {
    const [isValid] = validateEmail(email);
    return isValid;
}
```

### Explanation of the Regex:
The regex pattern checks for:
1. Local part (before `@`):
   - Can contain letters, numbers, and certain special characters
   - Supports quoted strings (e.g., `"user name"@example.com`)
2. `@` symbol
3. Domain part:
   - Either an IP address in brackets or a standard domain name
   - Supports subdomains and common TLDs

### Usage in Form Validation:

Here's how you might use this in a form validation system:

```typescript
interface FormData {
    email: string;
    // other fields...
}

function validateForm(data: Partial<FormData>): boolean {
    if (!data.email) return false;

    const [isValid] = validateEmail(data.email);
    if (!isValid) {
        console.error('Invalid email format');
        return false;
    }

    // Proceed with other validations...
    return true;
}

// In a React component:
const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const formData = {
        email: emailInput.value,
        // collect other fields
    };

    if (!validateForm(formData)) {
        showValidationErrors();
        return;
    }

    // Submit the valid data
    submitToServer(formData);
};
```

### Type Guard Usage:
The `isValidEmail` type guard can be used with TypeScript's type narrowing:

```typescript
function processUserInput(input: unknown) {
    if (isValidEmail(input)) {
        const email = input; // TypeScript now knows this is a valid string email
        console.log(`Processing email: ${email}`);
    } else {
        console.error('Invalid email');
    }
}
```

### Notes:
1. This provides basic validation - for production use, you might want to add additional checks or use a more comprehensive library.
2. The function returns both the boolean result and the normalized email (lowercase) if valid.
3. The type guard helps TypeScript understand the type of the input after validation.

127 t/s, 804 tokens, 6s, 9%
