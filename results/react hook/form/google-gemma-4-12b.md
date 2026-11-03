# Gemma 4 12B
Model: google/gemma-4-12b
Test: Hook Form
Created: 11/03/2026, 01:01:30 AM
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

function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const reset = () => {
    setValues(initialValues);
  };

  return [values, handleChange, reset];
}
```

82 t/s, 119 tokens, 2s
