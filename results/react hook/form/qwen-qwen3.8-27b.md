# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Hook Form
Created: 11/03/2026, 02:22:36 AM
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

export function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);

  const handleChange = useCallback((event) => {
    const { name, value } = event.target;
    setValues((prev) => ({
      ...prev,
      [name]: value,
    }));
  }, []);

  const reset = useCallback(() => {
    setValues(initialValues);
  }, [initialValues]);

  return [values, handleChange, reset];
}
```

23 t/s, 126 tokens, 6s
