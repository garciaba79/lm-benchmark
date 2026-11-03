# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Hook Form
Created: 11/03/2026, 12:37:15 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a custom React hook called `useForm` that manages form state and provides an onChange handler and a reset function.

Requirements:
- Takes an object of initial values (e.g. { name: "", email: "" })
- Returns: [values, handleChange, reset]
- handleChange should work with standard inputs: <input name="email" onChange={handleChange} />
- reset() should restore initial values
- Do NOT use any external libraries

Only return the hook function. No explanation.

> #### 🤖 Assistant

```javascript
import { useState } from 'react';

const useForm = (initialValues) => {
  const [values, setValues] = useState(initialValues);

  /**
   * Handles changes for form inputs based on their 'name' attribute.
   * @param {Object} event - The change event object from the input.
   */
  const handleChange = (event) => {
    const { name, value } = event.target;
    setValues(prevValues => ({
      ...prevValues,
      [name]: value,
    }));
  };

  /**
   * Resets the form state back to the initial values provided.
   */
  const reset = () => {
    setValues(initialValues);
  };

  return [values, handleChange, reset];
};

export default useForm;
```

137 t/s, 189 tokens, 1s
