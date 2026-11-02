# Granite 4.1 8B
Model: granite-4.1-8b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Certainly! Below is a TypeScript utility function named `validateEmail` that checks whether a given string is a valid email address using a regular expression. The function also handles edge cases such as empty strings or improperly formatted inputs.

### TypeScript Utility Function

```typescript
function validateEmail(email: string): boolean {
    // Regular expression for validating an Email
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    // Check if the input is a non-empty string and matches the regex pattern
    return typeof email === 'string' && email.length > 0 && emailRegex.test(email);
}

// Example usage:
console.log(validateEmail("example@domain.com")); // true
console.log(validateEmail("invalid-email"));      // false
console.log(validateEmail(""));                   // false
```

### Explanation

1. **Regular Expression (`emailRegex`)**: The regex pattern `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` ensures that:
   - The email starts with one or more characters that can be alphanumeric or certain special characters (`.`, `_`, `%`, `+`, `-`).
   - Followed by an `@` symbol.
   - Then a domain name consisting of alphanumeric characters and dots (`.`), but not starting or ending with a dot.
   - Ends with a top-level domain (TLD) that is at least two alphabetical characters long.

2. **Type Guard**: The function first checks if the input `email` is of type `string` and is non-empty to prevent invalid operations on undefined types or empty values.

3. **Edge Cases Handling**:
   - **Empty String**: An empty string returns `false`.
   - **Invalid Format**: Any string not matching the regex pattern (e.g., missing `@`, incorrect TLD length, etc.) returns `false`.

### Usage in Form Validation

In a form validation system, this utility function can be employed to ensure that user-entered email addresses are syntactically correct before proceeding with further processing, such as sending emails or storing data in a database. Here’s how it could integrate into a typical HTML form:

```html
<form id="emailForm">
    <label for="userEmail">Email:</label>
    <input type="text" id="userEmail" name="userEmail" required>
    <button type="submit">Submit</button>
</form>

<script>
document.getElementById('emailForm').addEventListener('submit', function(event) {
    const emailInput = document.getElementById('userEmail');
    const emailValue = emailInput.value;
    
    if (!validateEmail(emailValue)) {
        event.preventDefault(); // Prevent form submission
        alert('Please enter a valid email address.');
    }
});
</script>
```

In this example, when the form is submitted:
- The value of the `userEmail` input field is retrieved.
- `validateEmail` checks if the email is valid.
- If invalid, the form submission is prevented (`event.preventDefault()`), and an alert prompts the user to correct the email address. 

This ensures data integrity by filtering out incorrect emails at the client side before any server-side processing occurs.

127 t/s, 682 tokens, 5s, 5%
