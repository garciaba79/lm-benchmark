# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Function Validate Email
Created: 11/15/2026, 09:41:18 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is the TypeScript utility function for email validation, complete with explanations and usage context.

## TypeScript Email Validation Function

```typescript
/**
 * Validates whether the provided string is a syntactically valid email address.
 * 
 * This uses a relatively standard regular expression for general email format checking.
 * It handles basic structure validation but does not guarantee the existence or deliverability 
 * of the email (that requires more complex checks).
 *
 * @param email The string to validate.
 * @returns True if the string matches a common email format, false otherwise.
 */
export function validateEmail(email: string): boolean {
    // 1. Type Guard / Edge Case Handling: Check for non-string or empty input immediately.
    if (typeof email !== 'string' || email.trim() === '') {
        return false;
    }

    // 2. Regular Expression for Email Validation
    // This regex is a good balance between strictness and real-world usability.
    // It checks for: [local-part] @ [domain] . [tld]
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // 3. Perform the match
    return emailRegex.test(email);
}

// --- Example Usage ---

console.log("--- Validation Tests ---");

const email1 = "test@example.com";       // Valid
const email2 = "invalid-email";          // Invalid (missing @ and domain)
const email3 = "user.name+tag@sub.domain.co.uk"; // Valid (complex local part)
const email4 = "";                        // Empty string
const email5 = "plainaddress";            // Missing @ and domain

console.log(`"${email1}" is valid: ${validateEmail(email1)}`); // true
console.log(`"${email2}" is valid: ${validateEmail(email2)}`); // false
console.log(`"${email3}" is valid: ${validateEmail(email3)}`); // true
console.log(`"${email4}" is valid: ${validateEmail(email4)}`); // false
console.log(`"${email5}" is valid: ${validateEmail(email5)}`); // false
```

### Explanation of the Code

1. **Input Type and Edge Case Handling (Type Guard):**
   - `if (typeof email !== 'string' || email.trim() === '')`: This is crucial for robustness. It immediately checks if the input is actually a string and if it contains any content after removing leading/trailing whitespace. If it fails this check, we return `false` immediately, preventing errors in the regex step and handling empty inputs gracefully.

2. **Regular Expression (`emailRegex`):**
   - ` /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/`: This is a commonly used pattern for basic email structure:
     - `^`: Start of the string.
     - `[a-zA-Z0-9._%+-]+`: Matches the "local part" (before the `@`). It allows alphanumeric characters plus common symbols (`.`, `_`, `%`, `+`, `-`). The `+` means one or more of these characters must be present.
     - `@`: Matches the literal "at" symbol.
     - `[a-zA-Z0-9.-]+`: Matches the domain name (e.g., `example`).
     - `\.`: Matches a literal dot (`.`).
     - `[a-zA-Z]{2,}`: Matches the Top-Level Domain (TLD, e.g., `com`, `net`, `co.uk`). It requires at least two alphabetic characters.
     - `$`: End of the string.

3. **Validation:**
   - `emailRegex.test(email)`: The `.test()` method executes the regex against the input string and returns a boolean (`true` if a match is found, `false` otherwise).

---

## Use in a Form Validation System

This utility function is a perfect starting point for **client-side validation** (validation performed in the user's browser) within a form system.

### How it Works in a System:

1. **Event Listener:** When a user attempts to submit a registration or contact form, an event listener (e.g., on the `submit` event) is attached to the form.
2. **Data Retrieval:** Before submission, the values entered into the email field are retrieved from the DOM.
3. **Validation Call:** The application calls our utility function:
   ```typescript
   const userInput = document.getElementById('emailInput').value;
   if (!validateEmail(userInput)) {
       // Stop form submission and show an error
       alert("Please enter a valid email address.");
       event.preventDefault(); 
   } else {
       // Allow form submission to proceed (or move to next step)
   }
   ```
4. **User Experience:** If `validateEmail` returns `false`, the system immediately blocks the submission and displays an error message, guiding the user to correct the input *before* sending potentially bad data to the server.

### Important Caveat: Server-Side vs. Client-Side Validation

It is crucial to understand that **this client-side validation should never be the only check.**

*   **Client-Side (This Function):** Improves UX by providing instant feedback. It catches typos immediately.
*   **Server-Side (Mandatory Check):** Because regular expressions can be bypassed, a server *must* re-validate every single email address it receives before saving it to the database. This ensures data integrity and prevents malicious input.

195 t/s, 1269 tokens, 7s
