# Qwen3 14B
Model: qwen/qwen3-14b
Test: Hook Form
Created: 11/03/2026, 01:10:39 AM
Exported from: LM Studio (via test script)
Context unknown

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
function useForm(initialValues) {
  const [values, setValues] = React.useState(initialValues);

  const handleChange = (e) => {
    const { name, value } = e.target;
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
```

74 t/s, 88 tokens, 1s
