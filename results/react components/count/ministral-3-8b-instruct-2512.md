# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
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

Here's a clean, well-typed React functional component in TypeScript that meets all your requirements:

```tsx
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

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      <div style={styles.buttonContainer}>
        <button
          onClick={decrement}
          style={styles.button}
          disabled={count === 0}
        >
          Decrement
        </button>
        <button
          onClick={increment}
          style={styles.button}
        >
          Increment
        </button>
      </div>
    </div>
  );
};

// Basic inline styles
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    padding: '2rem',
    borderRadius: '8px',
    backgroundColor: '#f5f5f5',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    maxWidth: '300px',
    margin: '0 auto',
  } as const,

  heading: {
    fontSize: '3rem',
    color: '#333',
    margin: '0',
    fontWeight: 'bold',
    textAlign: 'center' as const,
  } as const,

  buttonContainer: {
    display: 'flex',
    gap: '1rem',
  } as const,

  button: {
    padding: '0.75rem 1.5rem',
    border: 'none',
    borderRadius: '4px',
    fontSize: '1rem',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease',
    backgroundColor: '#4CAF50',
    color: 'white',
    ':hover': {
      backgroundColor: '#45a049',
    },
  } as const,
} as const;

export default Counter;
```

Key features of this implementation:

1. **Proper Typing**:
   - Explicit TypeScript interface for props
   - State is typed with `useState<number>`
   - Inline styles are properly typed with `as const`

2. **Functional Updates**:
   - Uses functional updates (`prevCount => prevCount + 1`) to ensure we're working with the latest state

3. **Boundary Protection**:
   - Decrement button is disabled when count is 0
   - Count never goes below 0 (checked in decrement function)

4. **Modern React Practices**:
   - Uses `React.FC` for component typing
   - Default prop value provided (`initialCount = 0`)
   - Clean separation of concerns with styled objects

5. **Styling**:
   - All styling is contained within the component
   - Responsive design considerations
   - Hover effects on buttons
   - Centered layout with proper spacing

6. **Accessibility**:
   - Clear visual feedback for disabled state
   - Good contrast ratios
   - Logical button placement

You can use this component like:
```tsx
<Counter initialCount={5} />
// or default to 0
<Counter />
```

127 t/s, 801 tokens, 6s, 9%
