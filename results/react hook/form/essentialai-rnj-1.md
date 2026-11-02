# Rnj 1
Model: essentialai/rnj-1
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

```python
def useForm(initial_values):
    def get_form_hook():
        values = {**initial_values}
        
        def handleChange(event):
            name = event.get('target', {}).get('name')
            value = event.get('target', {}).get('value')
            if name:
                values[name] = value
        
        def reset():
            nonlocal values
            values = {**initial_values}
        
        return [values, handleChange, reset]
    
    return get_form_hook()
```

118 t/s, 101 tokens, 1s, 1%
