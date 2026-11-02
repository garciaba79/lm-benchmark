# Ornith 1.5 9B
Model: ornith-1.5-9b
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
import { useRef, useState } from "react";

export default function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);
  const initialRef = useRef(initialValues);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const reset = () => {
    setValues(initialRef.current);
  };

  return [values, handleChange, reset];
}
```

143 t/s, 431 tokens, 3s, 3%
