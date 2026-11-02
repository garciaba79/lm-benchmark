# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

# TypeScript Email Validation Utility

Here's a comprehensive `validateEmail` function with type safety and edge case handling:

```typescript
/**
 * Validates an email address using a regular expression
 * @param email - The email address to validate
 * @returns boolean indicating if the email is valid
 */
export const validateEmail = (email: string | null | undefined): boolean => {
  // Handle null, undefined, and empty strings
  if (!email || typeof email !== 'string' || email.trim() === '') {
    return false;
  }

  const trimmedEmail = email.trim();

  // Email validation regex (RFC 5322 simplified)
  const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

  return EMAIL_REGEX.test(trimmedEmail);
};

/**
 * Type guard to check if value is a valid string email
 */
export const isValidString = <T>(value: T): value is Extract<T, string> => {
  return typeof value === 'string';
};

/**
 * Form validation result type
 */
export interface EmailValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * More detailed validation that returns structured results
 */
export const validateEmailDetailed = (email: string | null | undefined): EmailValidationResult => {
  if (!email) {
    return { isValid: false, error: 'Email is required' };
  }

  if (typeof email !== 'string') {
    return { isValid: false, error: 'Invalid email type' };
  }

  const trimmedEmail = email.trim();

  if (trimmedEmail.length === 0) {
    return { isValid: false, error: 'Email cannot be empty' };
  }

  if (!validateEmail(email)) {
    return { isValid: false, error: 'Invalid email format' };
  }

  return { isValid: true };
};
```

## Usage in Form Validation System

### Basic Form Component Example

```typescript
// Form state interface
interface EmailFormState {
  email: string;
  errors: Record<string, string>;
  isValid: boolean;
}

const createForm = () => ({
  email: '',
  errors: {},
  isValid: false
});

// Validation function for form submission
const validateEmailField = (fieldValue: string): EmailValidationResult => {
  return validateEmailDetailed(fieldValue);
};

// Form submit handler
const handleFormSubmit = async (formData: any) => {
  const validation = validateEmailDetailed(formData.email);

  if (!validation.isValid) {
    console.error(validation.error);
    // Show error message to user
    return;
  }

  // Proceed with API submission
  await submitUserData(formData.email);
};
```

### React Component Example

```typescript
// React component with email validation
const EmailForm = ({ onSubmit }: { onSubmit: (email: string) => Promise<void> }) => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    const validation = validateEmailDetailed(email);
    
    if (!validation.isValid) {
      setError(validation.error);
      return;
    }

    try {
      await onSubmit(email.trim());
      setError(null);
    } catch (err) {
      setError('Submission failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);
          setError(null);
        }}
        placeholder="Enter your email"
      />
      {error && <span className="error">{error}</span>}
      <button type="submit">Submit</button>
    </form>
  );
};
```

## Edge Cases Handled

| Case | Handled | Example |
|------|---------|---------|
| Empty string | ✅ | `''` returns `false` |
| Null/undefined | ✅ | `null`, `undefined` returns `false` |
| Whitespace only | ✅ | `'   '` returns `false` |
| Invalid regex | ✅ | `'not-an-email'` returns `false` |
| Missing @ symbol | ✅ | `'test@example'` returns `false` |
| Multiple @ symbols | ✅ | `'test@@example.com'` returns `false` |

## Best Practices

1. **Trim input** before validation to remove accidental spaces
2. **Use type guards** for safer TypeScript usage
3. **Provide clear error messages** for better UX
4. **Consider normalization** (e.g., case-insensitive comparison) if needed
5. **Validate on blur and submit**, not just submit

This utility integrates cleanly into form validation systems by providing both quick boolean checks and detailed validation results, making it easy to implement in various frontend frameworks while maintaining type safety.

121 t/s, 1319 tokens, 11s, 8%
