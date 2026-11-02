# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

```typescript
function validateEmail(email: string): boolean {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return typeof email === 'string' && !!email.length && regex.test(email);
}
```
This function uses a regular expression to check if the input string is in the format of an email address. It returns true only when:
1) The input is a non-empty string, and
2) The input matches the regular expression pattern for an email address.

The type guard `typeof email === 'string'` ensures that the function only accepts strings as inputs. This helps to prevent runtime errors if the function receives unexpected data types.

In a form validation system, this utility could be used like so:
```typescript
function submitForm(email: string): void {
    if (!validateEmail(email)) {
        alert('Please enter a valid email address');
        return;
    }
    // Proceed with form submission...
}
```
In this example, the `submitForm` function uses `validateEmail` to check whether the user's input is a valid email. If it isn't, an alert is displayed and the function returns early, preventing the form from being submitted. This helps prevent potential errors or security vulnerabilities that could arise from submitting invalid data.

150 t/s, 327 tokens, 2s, 1%
