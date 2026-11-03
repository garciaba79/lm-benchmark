# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Hook Form
Created: 11/03/2026, 02:57:50 AM
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

```javascript
const useForm = (initialValues) => {
  const [values, setValues] = useState(initialValues);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const reset = () => {
    setValues(initialValues);
  };
  
  return [values, handleChange, reset];
};
```

64 t/s, 95 tokens, 2s
