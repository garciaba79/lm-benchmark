# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Hook Form
Created: 11/22/2026, 03:08:31 AM
Exported from: LM Studio (via test script)
Context 16K

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

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setValues((prevValues) => ({
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

61 t/s, 136 tokens, 2s, 2%
