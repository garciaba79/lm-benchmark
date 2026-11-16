# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Hook Form
Created: 11/15/2026, 09:43:37 PM
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
import { useState, useCallback } from 'react';

function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);

  const handleChange = useCallback((event) => {
    const { name, value } = event.target;
    setValues(prevValues => ({
      ...prevValues,
      [name]: value,
    }));
  }, []);

  const reset = useCallback(() => {
    setValues(initialValues);
  }, [initialValues]);

  return [values, handleChange, reset];
}

export default useForm;
```

174 t/s, 135 tokens, 1s
