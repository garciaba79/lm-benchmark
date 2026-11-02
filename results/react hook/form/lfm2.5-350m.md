# LFM2.5 350M
Model: lfm2.5-350m
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
function useForm({ initialValues }) {
  const [values, handleChange, reset] = [];
  
  return { values, handleChange, reset };
}
```

679 t/s, 38 tokens, 0s, 1%
