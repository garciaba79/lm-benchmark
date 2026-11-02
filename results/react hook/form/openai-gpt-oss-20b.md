# GPT-OSS 20B
Model: openai/gpt-oss-20b
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
import { useState, useCallback, useRef } from 'react';

export default function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);
  const initialRef = useRef(initialValues);

  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    setValues(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  }, []);

  const reset = useCallback(() => {
    setValues(initialRef.current);
  }, []);

  return [values, handleChange, reset];
}
```

124 t/s, 228 tokens, 2s, 2%
