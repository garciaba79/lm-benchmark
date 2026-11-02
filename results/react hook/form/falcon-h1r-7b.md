# Falcon H1R 7B
Model: falcon-h1r-7b
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

```js
import React from "react";

function useForm(initialValues) {
  const initialRef = React.useRef(initialValues);
  const [values, setValues] = React.useState(() => initialRef.current);
  
  const handleChange = e => {
    const name = e.target.name;
    
    // Ignore unknown fields
    if (!Object.prototype.hasOwnProperty.call(initialRef.current, name)) return;
    
    let newValue = 
      e.target.type === "checkbox" ? e.target.checked : e.target.value;
      
    setValues({ ...values, [name]: newValue });
  };
  
  const reset = () => setValues(() => initialRef.current);
  
  return [values, handleChange, reset];
}

export default useForm;
```

98 t/s, 2638 tokens, 27s, 17%
