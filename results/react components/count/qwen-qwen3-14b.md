# Qwen3 14B
Model: qwen/qwen3-14b
Test: component count
Created: 11/03/2026, 01:10:09 AM
Exported from: LM Studio (via test script)
Context unknown

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

Here's a simple and clean React functional component in TypeScript that meets all your requirements:

```tsx
import React, { useState } from 'react';

// Define types
type CounterProps = {
  initialCount?: number;
};

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // State for current count
  const [count, setCount] = useState<number>(initialCount);

  // Handle increment action
  const handleIncrement = () => {
    setCount(count + 1);
  };

  // Handle decrement action with a minimum value of 0
  const handleDecrement = () => {
    if (count > 0) {
      setCount(count - 1);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f0f4f8',
    }}>
      {/* Display current count */}
      <h1 style={{
        fontSize: '3rem',
        marginBottom: '2rem',
        color: '#333',
      }}>
        {count}
      </h1>

      {/* Buttons */}
      <div style={{
        display: 'flex',
        gap: '1rem',
      }}>
        <button
          onClick={handleIncrement}
          style={{
            padding: '0.75rem 1.5rem',
            fontSize: '1rem',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'background-color 0.2s ease',
          }}
        >
          Increment
        </button>
        <button
          onClick={handleDecrement}
          style={{
            padding: '0.75rem 1.5rem',
            fontSize: '1rem',
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'background-color 0.2s ease',
          }}
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

---

### ✅ Features Covered:
- **`initialCount` prop**: Accepts a number with a fallback of `0`.
- **State Management**: Uses `useState` to manage the count.
- **Buttons**:
  - "Increment" increases the count by 1.
  - "Decrement" decreases it, but never goes below `0`.
- **Styling**: Inline styles are used for simplicity and no external CSS is needed.
- **Type Safety**: TypeScript types are used throughout (`CounterProps`, `useState` with proper typing).
- **Modern React Best Practices**:
  - Functional component with hooks.
  - Proper prop typing.
  - No unnecessary dependencies or libraries.

---

You can now use this `Counter` component in your app by importing and passing an optional `initialCount`. For example:

```tsx
import React from 'react';
import Counter from './Counter';

const App: React.FC = () => {
  return <Counter initialCount={5} />;
};

export default App;
```

Let me know if you'd like to add features like animations, themes, or accessibility enhancements!

79 t/s, 721 tokens, 9s
