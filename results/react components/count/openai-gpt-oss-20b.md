# GPT-OSS 20B
Model: openai/gpt-oss-20b
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

```tsx
// Counter.tsx
import React, { FC, useState } from 'react';

interface CounterProps {
  /** Starting value for the counter (defaults to 0). */
  initialCount?: number;
}

const Counter: FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  // Handlers
  const increment = () => setCount((c) => c + 1);
  const decrement = () =>
    setCount((c) => (c > 0 ? c - 1 : 0)); // never go below zero

  /* Basic inline styles – feel free to tweak */
  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    fontFamily: 'sans-serif',
    marginTop: '2rem',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '4rem',
    marginBottom: '1.5rem',
  };

  const buttonContainerStyle: React.CSSProperties = {
    display: 'flex',
    gap: '1rem',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    backgroundColor: '#007bff',
    color: '#fff',
    transition: 'background-color 150ms ease',
  };

  const buttonHoverStyle: React.CSSProperties = {
    backgroundColor: '#0056b3',
  };

  // To keep the example simple, we’ll just use a state flag to toggle hover styles
  const [hoveredBtn, setHoveredBtn] = useState<string | null>(null);

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>{count}</h1>
      <div style={buttonContainerStyle}>
        <button
          type="button"
          style={{
            ...buttonStyle,
            ...(hoveredBtn === 'inc' ? buttonHoverStyle : {}),
          }}
          onClick={increment}
          onMouseEnter={() => setHoveredBtn('inc')}
          onMouseLeave={() => setHoveredBtn(null)}
        >
          Increment
        </button>
        <button
          type="button"
          style={{
            ...buttonStyle,
            ...(hoveredBtn === 'dec' ? buttonHoverStyle : {}),
          }}
          onClick={decrement}
          onMouseEnter={() => setHoveredBtn('dec')}
          onMouseLeave={() => setHoveredBtn(null)}
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

**Usage**

```tsx
import React from 'react';
import Counter from './Counter';

const App: React.FC = () => (
  <div>
    {/* Provide an initial value or let it default to 0 */}
    <Counter initialCount={5} />
  </div>
);

export default App;
```

The component:

- Accepts `initialCount` with a default of `0`.
- Uses `useState` typed as `number`.
- Prevents the count from dropping below zero.
- Applies clean, self‑contained inline styling without external dependencies.

132 t/s, 743 tokens, 6s, 6%
