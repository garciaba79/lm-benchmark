# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: component count
Created: 11/02/2026, 05:35:23 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a simple React functional component in TypeScript that does the following:

- Accepts a prop called `initialCount` of type number (default to 0 if not provided).
- Displays the current count in a large, centered heading.
- Has two buttons: "Increment" and "Decrement".
- Clicking "Increment" increases the count by 1.
- Clicking "Decrement" decreases the count by 1, but never lets it go below 0.
- Style the component nicely using inline styles or a basic CSS object (no external CSS files or libraries like Tailwind).
- Make sure all props and state are properly typed.
- Follow modern React principles and best practices.

Show the complete component code, including imports.

> #### 🤖 Assistant

```typescript
import * as React from 'react';
import { useState } from 'react';

interface CounterProps {
    initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({initialCount=0}) => {
    const [count, setCount] = useState(initialCount);

    return (
        <div style={{textAlign:'center'}}>
            <h1 style={{fontSize:'5em', marginBottom: '2em'}}>{count}</h1>
            <button onClick={() => setCount(Math.max(0, count - 1))} style={{marginRight: '1em'}}>Decrement</button>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
};

export default Counter;
```

150 t/s, 201 tokens, 2s, 1%
