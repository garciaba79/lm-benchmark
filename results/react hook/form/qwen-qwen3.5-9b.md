# Qwen3.5 9B
Model: qwen/qwen3.5-9b
Test: Hook Form
Created: 11/02/2026, 06:44:56 AM
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
import { useState } from 'react';

export const useForm = (initialValues) => {
  const [values, setValues] = useState(initialValues);

  const handleChange = (e) => {
    const targetName = e.target.name;
    if (targetName) {
      setValues((prev) => ({
        ...prev,
        [targetName]: e.target.value
      }));
    }
  };

  const reset = () => {
    setValues(initialValues);
  };

  return [values, handleChange, reset];
};
```

109 t/s, 5192 tokens, 48s, 32%
