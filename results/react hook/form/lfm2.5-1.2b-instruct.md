# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
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
const useForm = (initialValues) => {
  const [values, setValues] = useState(initialValues);
  const [resetValue, setResetValue] = useState(initialValues);

  const handleChange = (name, newValue) => {
    setValues({
      ...values,
      [name]: newValue
    });
  };

  const resetForm = () => {
    setValues(resetValue);
  };

  return [values, handleChange, resetForm];
}
```

539 t/s, 113 tokens, 0s, 1%
