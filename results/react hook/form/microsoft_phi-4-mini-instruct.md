# Microsoft Phi 4 Mini Instruct
Model: microsoft_phi-4-mini-instruct
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

```jsx
import { useState } from 'react';

function useForm(initialValues) {
  const [values, setValues] = useState(Object.keys(initialValues).reduce((obj, key) => ({ ...obj, [key]: initialValues[key] }), {}));

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setValues({
      ...values,
      [name]: value
    });
  };

  const reset = () => {
    setValues(initialValues);
  };

  return [values, handleChange, reset];
}

export default useForm;
```

179 t/s, 133 tokens, 1s, 1%
