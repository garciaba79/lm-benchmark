# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Hook Form
Created: 11/02/2026, 06:44:56 AM
Exported from: LM Studio (via test script)
Context 32K

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

    const handleChange = e => {
        setValues({ ...values, [e.target.name]: e.target.value });
    };

    const reset = () => {
        setValues(initialValues);
    };

    return [values, handleChange, reset];
};

export default useForm;
```

139 t/s, 118 tokens, 1s, 1%
