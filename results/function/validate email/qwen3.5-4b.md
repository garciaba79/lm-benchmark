# Qwen3.5 4B
Model: qwen3.5-4b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is a robust TypeScript utility function `validateEmail` that validates email addresses using regular expressions and includes type guards and edge case handling. It also demonstrates how this can be integrated into a form validation system.

```typescript
/**
 * Validates an email address using a regex pattern.
 * @param email - The string to validate as an email address.
 * @returns A boolean indicating whether the email is valid.
 */
export function validateEmail(email: string): boolean {
  if (typeof email !== 'string' || email.trim() === '') return false;

  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
}

/**
 * Type guard to check if a value is a valid email string.
 */
export function isValidEmail(value: unknown): value is string {
  return typeof value === 'string' && validateEmail(value.trim());
}

// Optional: Enhanced validation with additional checks (e.g., length, domain)
export const validateEmailEnhanced = (email: string): boolean => {
  if (!validateEmail(email)) return false;

  // Additional constraints for stricter validation
  const trimmed = email.trim();
  if (trimmed.length < 5 || trimmed.length > 254) return false;

  const parts = trimmed.split('@');
  if (parts.length !== 2) return false;

  const [local, domain] = parts;
  if (!local.includes('.') || !domain.includes('.')) return false;

  // Ensure local part doesn't start or end with a dot
  if (local.startsWith('.') || local.endsWith('.')) return false;

  // Ensure domain has at least one dot and ends with a valid TLD
  const domainParts = domain.split('.');
  if (domainParts.length < 2) return false;

  for (const part of domainParts) {
    if (!part || !/^[a-zA-Z0-9]+$/.test(part)) return false;
  }

  // Ensure TLD is at least 2 characters long
  const tld = domainParts[domainParts.length - 1];
  if (tld.length < 2) return false;

  return true;
};

// Example usage in a form validation system
interface FormValidation {
  email: string | null;
}

export function validateFormEmail(emailInput: string): boolean {
  const trimmed = emailInput.trim();
  if (!trimmed || !validateEmail(trimmed)) {
    return false;
  }
  // Optional: Use enhanced validation for stricter requirements
  // return validateEmailEnhanced(trimmed);
  return true;
}

// Example usage in a React form component
export const EmailFormComponent = () => {
  const [email, setEmail] = useState('');
  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    if (email) {
      setIsValid(validateEmail(email));
    } else {
      setIsValid(false);
    }
  }, [email]);

  return (
    <div>
      <input
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
      />
      {isValid && <span style={{ color: 'green' }}>✓ Valid Email</span>}
      {!isValid && <span style={{ color: 'red' }}>✗ Invalid Email</span>}
    </div>
  );
};

// Example usage in a form submission handler
export const submitForm = async (formData: FormValidation) => {
  if (!formData.email || !validateEmail(formData.email)) {
    throw new Error('Please enter a valid email address');
  }
  // Proceed with API call or other logic
};

// Example usage in TypeScript's type narrowing
export const processUserInput = (input: unknown): string | null => {
  if (!isValidEmail(input)) return null;
  return input as string;
};
```

### How to Use This in a Form Validation System

1. **Client-Side Validation:**  
   Call `validateEmail()` on form submission or during real-time input updates (e.g., React `onChange` handlers) to provide immediate feedback to the user.

2. **Type Safety with Type Guards:**  
   Use `isValidEmail()` to narrow types in TypeScript, ensuring that only valid email strings are processed further.

3. **Enhanced Validation for Strict Requirements:**  
   For applications requiring stricter validation (e.g., enterprise systems), use `validateEmailEnhanced()` which enforces additional constraints like domain structure and length limits.

4. **Form Submission Logic:**  
   Integrate the function into form submission handlers to prevent invalid data from being sent to APIs or databases.

5. **User Feedback UI:**  
   Display validation status (valid/invalid) directly in the input field using conditional rendering based on `isValid` state.

This utility provides a flexible, type-safe foundation for email validation across various scenarios and can be easily extended with additional rules as needed.

176 t/s, 1287 tokens, 7s, 8%
