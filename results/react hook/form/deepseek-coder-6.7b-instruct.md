# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
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

Sure, here is a custom React Hook called `useForm` that meets your requirements:

```jsx
import { useState } from 'react';

export const useForm = (initialValues) => {
  // Initialize state with initial values
  const [values, setValues] = useState(initialValues);
  
  // Handle change event for inputs
  const handleChange = e => {
    setValues({ ...values, [e.target.name]: e.target.value });
  };
    
  // Reset form to initial values
  const reset = () => {
      setValues(initialValues);
  }
  
  return [values, handleChange, reset];
};
```

148 t/s, 164 tokens, 1s, 2%
