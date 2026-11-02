# LFM2.5 1.2B Thinking
Model: lfm2.5-1.2b-thinking
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

const useForm = (initialValues) => {
  const [formState] = { ...initialValues };
  const handleChange = (e) => {
    const fieldName = e.target.name;
    Object.assign(formState[fieldName], e.target.value);
  }
  const reset = () => {
    formState = initialValues;
  };
  return [formState, handleChange, reset];
}

525 t/s, 4485 tokens, 9s, 28%
