# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

```typescript
// Importing necessary package for regular expressions
import { isString } from "lodash";

/**
 * Validates an email address using a regular expression.
 * @param email The email address to validate.
 * @returns true if the email is valid, false otherwise.
 */
function validateEmail(email: string): boolean {
    // Regular expression pattern for validating an email
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    // Check if the input is a non-empty string and matches the regex
    return isString(email) && regex.test(email);
}

// Function to test the validateEmail function with various data points
function testValidateEmail() {
    console.log(validateEmail("example@example.com")); // Expected: true
    console.log(validateEmail("invalid-email")); // Expected: false
    console.log(validateEmail("")); // Expected: false
    console.log(validateEmail(123)); // Expected: false
}

// Running the test function to verify the correctness of validateEmail
testValidateEmail();
```

In this solution, we've created a TypeScript utility function `validateEmail` that uses a regular expression to check if an email address is valid. The function first checks if the input is a string and then applies the regex pattern to ensure it matches the standard email format. We've also included a test function `testValidateEmail` that demonstrates how this function can be used in a form validation system, providing examples of valid and invalid inputs.

339 t/s, 321 tokens, 1s, 5%
