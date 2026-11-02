# Granite 4.1 8B
Model: granite-4.1-8b
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
function useForm(initialValues) {
  const [values, setValues] = React.useState(initialValues);
  const initialValuesRef = React.useRef(initialValues);

  function handleChange(e) {
    setValues(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  }

  function reset() {
    setValues(initialValuesRef.current);
  }

  return [values, handleChange, reset];
}
```

118 t/s, 92 tokens, 1s, 1%
