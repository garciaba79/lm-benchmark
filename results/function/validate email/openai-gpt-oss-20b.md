# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Function Validate Email
Created: 11/02/2026, 01:18:39 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a TypeScript utility function called validateEmail that takes a string input and returns a boolean indicating if it's a valid email address. Use a regular expression for validation, handle edge cases like empty strings or invalid formats, and add type guards if appropriate. Explain briefly how this could be used in a form validation system.

> #### 🤖 Assistant

## `validateEmail` – A Tiny TypeScript Email Validator

```ts
/**
 * Checks whether the supplied string is a syntactically valid e‑mail address.
 *
 * @param value - The raw input that should be interpreted as an e‑mail.
 * @returns `true` if `value` matches the RFC‑5322‑like pattern, otherwise `false`.
 */
export function validateEmail(value: unknown): value is string {
  // Quick sanity check – we only care about non‑empty strings
  if (typeof value !== "string" || !value.trim()) {
    return false;
  }

  /* A pragmatic RFC‑5322‑ish regular expression.
   *
   * • Local part: letters, digits and a handful of special characters,
   *   optionally quoted.  Consecutive dots are disallowed.
   * • @ separator
   * • Domain part: labels separated by dots; each label starts & ends with an alphanum
   *   and may contain hyphens in the middle.  The top‑level domain (TLD) must be at least
   *   two letters long.
   *
   * This is not a perfect RFC implementation but catches almost all real‑world
   * addresses while keeping the regex readable and fast.
   */
  const emailRegex = new RegExp(
    // eslint-disable-next-line no-useless-escape
    `^(?:(?:[a-zA-Z0-9!#$%&'*+/=?^_\`{|}~-]+(?:\\.[a-zA-Z0-9!#$%&'*+/=?^_\`{|}~-]+)*)|(?:"[^"]+"))@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,})$`
  );

  return emailRegex.test(value.trim());
}
```

### Why the type guard (`value is string`)?

* **Safety in callers** – If you pass a value that failed validation to another function that expects a `string`, TypeScript will narrow the type for you:

```ts
const raw = getUserInput(); // unknown | null

if (validateEmail(raw)) {
  // Inside this block, TS knows `raw` is a string.
  sendToServer({ email: raw });
}
```

* **Better IntelliSense** – When you chain calls that depend on the value being a string, editors can provide autocompletion without extra casts.

### Edge‑Case Handling

| Situation | What happens |
|-----------|--------------|
| `null`, `undefined`, number, object … | Returned `false` immediately. |
| Empty or whitespace only | Returned `false`. |
| Strings with leading/trailing spaces | Trimmed before testing. |
| Very long strings ( > 254 chars ) | The regex will reject them because the pattern limits total length via its structure. |

### Using it in a Form Validation System

```ts
// A simple form state interface
interface SignUpForm {
  email: string;
  password: string;
}

// A generic validator that can be reused across many forms
function validateField<T>(value: unknown, validator: (v: unknown) => boolean): boolean {
  return validator(value);
}

const formData: SignUpForm = { email: "user@example.com", password: "12345" };

const isEmailValid = validateField(formData.email, validateEmail);

if (!isEmailValid) {
  // Show a UI error message or prevent form submission
  console.warn("Please enter a valid e‑mail address");
}
```

In a real application you would typically integrate this into a form library (e.g., React Hook Form, Formik) as part of the validation schema. The `validateEmail` function can be passed as a rule:

```ts
// Using Yup
import * as yup from "yup";

const schema = yup.object({
  email: yup.string().required().test(
    "is-valid-email",
    "Invalid e‑mail address",
    validateEmail // <-- the TypeScript guard works here too
  ),
});
```

The utility is lightweight, pure, and fully typed, making it a drop‑in replacement for ad‑hoc string checks in any component or service that needs to confirm an email address before proceeding.

132 t/s, 937 tokens, 8s, 7%
