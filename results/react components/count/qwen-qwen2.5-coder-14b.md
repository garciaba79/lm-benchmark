# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
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

```typescript
import React, { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const decrement = () => {
    if (count > 0) {
      setCount(prevCount => prevCount - 1);
    }
  };

  // Basic CSS object for styling
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      fontFamily: 'Arial, sans-serif',
    },
    heading: {
      fontSize: '4rem',
      marginBottom: '2rem',
    },
    button: {
      padding: '0.5rem 1rem',
      margin: '0.5rem',
      fontSize: '1rem',
      cursor: 'pointer',
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      <button onClick={increment} style={styles.button}>Increment</button>
      <button onClick={decrement} style={styles.button}>Decrement</button>
    </div>
  );
};

export default Counter;
```

### Explanation:

- **Props and Default Value**: The `Counter` component accepts an optional `initialCount` prop with a default value of `0`.
- **State Management**: We use the `useState` hook to manage the count state, initialized to `initialCount`.
- **Increment/Decrement Functions**: These functions update the state using functional updates to ensure consistency.
- **Styling**: Inline styles are used for basic styling. The component is centered on the page with a simple layout.
- **Export**: The component is exported as the default export.

This component follows modern React principles, including the use of TypeScript for type safety and functional components with hooks for state management.

79 t/s, 458 tokens, 6s, 4%
