# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
Test: component count
Created: 11/02/2026, 05:35:23 AM
Exported from: LM Studio (via test script)
Context 16K

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

Here is the complete TypeScript functional component:

```typescript
import React, { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // Initialize state with provided prop or default to 0
  const [count, setCount] = useState(initialCount);

  // Handler for increment button click
  const handleIncrement = () => {
    setCount(count + 1);
  };

  // Handler for decrement button click
  const handleDecrement = () => {
    // Ensure count does not go below 0
    if (count > 0) {
      setCount(count - 1);
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '10px' }}>Current Count: {count}</h1>
      
      <button 
        onClick={handleIncrement} 
        style={{ marginRight: '10px', padding: '8px 16px', backgroundColor: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer' }}
      >
        Increment
      </button>
      
      <button 
        onClick={handleDecrement} 
        style={{ marginLeft: '10px', padding: '8px 16px', backgroundColor: '#f44336', color: 'white', border: 'none', cursor: 'pointer' }}
      >
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

289 t/s, 363 tokens, 1s, 3%
