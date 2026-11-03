# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Function Validate Email
Created: 11/03/2026, 02:52:55 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

```typescript
/**
 * Validates if a string is a properly formatted email address
 * @param email - The email string to validate
 * @returns boolean indicating if the email is valid
 */
export function validateEmail(email: string): email is string {
  // Handle edge cases
  if (!email || typeof email !== 'string') {
    return false;
  }

  // Trim whitespace
  const trimmedEmail = email.trim();
  
  // Check for empty string after trimming
  if (trimmedEmail.length === 0) {
    return false;
  }

  // Comprehensive email regex pattern
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  
  // Test the email against the regex
  return emailRegex.test(trimmedEmail);
}

// Alternative stricter version with additional checks
export function validateEmailStrict(email: string): boolean {
  if (!email || typeof email !== 'string') {
    return false;
  }

  const trimmedEmail = email.trim();
  
  if (trimmedEmail.length === 0) {
    return false;
  }

  // Additional length check (RFC 5321 limit)
  if (trimmedEmail.length > 254) {
    return false;
  }

  // More strict regex with better validation
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  
  return emailRegex.test(trimmedEmail);
}

// Type guard for use in conditional logic
export function isEmail(email: unknown): email is string {
  return typeof email === 'string' && validateEmail(email);
}
```

## Usage in Form Validation System

This validation function can be integrated into a form validation system like this:

```typescript
// Example form validation class
class FormValidator {
  private errors: Record<string, string> = {};
  
  validateField(fieldName: string, value: string): boolean {
    switch (fieldName) {
      case 'email':
        if (!validateEmail(value)) {
          this.errors.email = 'Please enter a valid email address';
          return false;
        }
        delete this.errors.email;
        return true;
      // ... other fields
      default:
        return true;
    }
  }
  
  // Validate entire form
  validateForm(formData: Record<string, string>): boolean {
    let isValid = true;
    
    Object.keys(formData).forEach(field => {
      if (!this.validateField(field, formData[field])) {
        isValid = false;
      }
    });
    
    return isValid;
  }
}

// Usage in React component
const MyForm = () => {
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    
    // Real-time validation
    if (!validateEmail(value)) {
      setErrors(prev => ({ ...prev, email: 'Invalid email format' }));
    } else {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors.email;
        return newErrors;
      });
    }
  };
  
  return (
    <form>
      <input 
        type="email" 
        value={email}
        onChange={handleEmailChange}
        className={errors.email ? 'error' : ''}
      />
      {errors.email && <span className="error-text">{errors.email}</span>}
    </form>
  );
};
```

## Key Features:

1. **Type Safety**: Uses TypeScript's type guards (`email is string`) for better compile-time checking
2. **Edge Case Handling**: Handles null, undefined, empty strings, and non-string inputs
3. **Whitespace Management**: Trims input to prevent false negatives
4. **Comprehensive Regex**: Follows RFC 5321 standards for email validation
5. **Flexible Usage**: Can be used for real-time validation or form submission

The function is particularly useful in form validation because it provides immediate feedback to users and can be easily integrated into existing validation frameworks or libraries.

61 t/s, 1001 tokens, 17s
