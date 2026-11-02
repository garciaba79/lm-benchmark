# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

Here is an example of a TypeScript utility function called validateEmail that uses a regular expression to check if the input string follows the format of a valid email address:
```typescript
function validateEmail(input: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(input);
}

// Example usage in a form validation system
const emailInput = document.getElementById("email-input") as HTMLInputElement;

emailInput.addEventListener("blur", () => {
  if (!validateEmail(emailInput.value)) {
    alert("Invalid email address.");
  } else {
    console.log("Valid email address!");
  }
});
```

This function uses the regular expression `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` to test the input string. The regex checks that there are at least one character before and after the `@` symbol, and that there is at least one character between the `@` symbol and the period. If the input string does not match this pattern, then the function returns false, indicating that it is not a valid email address.
In the example usage, we attach an event listener to an HTML input element with the ID "email-input". When the user blurs (moves away from) the input field, we call the `validateEmail` function on the value of the input field. If the returned boolean is false, then we alert the user that they have entered an invalid email address. Otherwise, we log a message indicating that the email address is valid.
This utility function can be used in any form validation system where you need to validate an input string as an email address. It provides a simple way to check if an input is in the correct format and can help prevent errors caused by incorrect or invalid email addresses being submitted to your application.

77 t/s, 376 tokens, 5s, 3%
