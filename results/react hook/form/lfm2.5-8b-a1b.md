# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
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

function useForm(initialValues) {
  const [formValues, setFormValues] = useState({ ...initialValues });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name && Object.prototype.hasOwnProperty.call(initialValues, name)) {
      setFormValues((prev) => ({ ...prev, [name]: value }));
    }
  };

  const reset = () => {
    setFormValues({ ...initialValues });
  };

  return [formValues, handleChange, reset];
}

export default useForm;
```

361 t/s, 443 tokens, 1s, 3%
