# Phi 4
Model: microsoft/phi-4
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

Here's a simple React functional component in TypeScript that meets your requirements:

```tsx
import React, { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  const increment = () => setCount((prev) => prev + 1);
  const decrement = () => setCount((prev) => Math.max(0, prev - 1));

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      textAlign: 'center',
    },
    heading: {
      fontSize: '48px',
      margin: '20px 0',
    },
    button: {
      padding: '10px 20px',
      margin: '5px',
      fontSize: '16px',
      cursor: 'pointer',
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      <button
        style={styles.button}
        onClick={increment}
        disabled={count >= Number.MAX_SAFE_INTEGER}
      >
        Increment
      </button>
      <button
        style={styles.button}
        onClick={decrement}
        disabled={count === 0}
      >
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

### Explanation:

- **Props**: The component accepts an optional `initialCount` prop of type number, defaulting to 0 if not provided.
- **State Management**: Uses the `useState` hook to manage the count state, initialized with `initialCount`.
- **Event Handlers**: Functions `increment` and `decrement` are defined to update the count. The decrement function ensures the count never goes below 0 using `Math.max(0, prev - 1)`.
- **Styling**: Inline styles are used for simplicity. The component is centered vertically and horizontally with basic styling for headings and buttons.
- **Best Practices**: 
  - TypeScript interfaces are used to define prop types.
  - Functional components and hooks follow modern React principles.
  - Buttons have `disabled` states to prevent invalid operations (e.g., decrementing below 0 or exceeding safe integer limits).

82 t/s, 506 tokens, 6s, 4%
