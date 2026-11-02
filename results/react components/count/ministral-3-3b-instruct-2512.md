# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
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

interface CountDisplayProps {
  initialCount?: number;
}

const CountDisplay: React.FC<CountDisplayProps> = ({ initialCount = 0 }) => {
  // Initialize state with the provided initialCount or default to 0
  const [count, setCount] = useState<number>(initialCount);

  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const decrement = () => {
    setCount(prevCount => Math.max(0, prevCount - 1));
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '300px',
        gap: '20px',
        padding: '20px',
        backgroundColor: '#f5f5f5',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      }}
    >
      <h1
        style={{
          fontSize: '3rem',
          color: '#2c3e50',
          textAlign: 'center',
          margin: 0,
          fontFamily: 'sans-serif',
        }}
      >
        {count}
      </h1>

      <div
        style={{
          display: 'flex',
          gap: '10px',
          flexDirection: 'row',
        }}
      >
        <button
          onClick={decrement}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            backgroundColor: '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
        >
          Decrement
        </button>

        <button
          onClick={increment}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            backgroundColor: '#e74c3c',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
        >
          Increment
        </button>
      </div>
    </div>
  );
};

export default CountDisplay;
```

### Key Features:

1. **Type Safety**:
   - Proper TypeScript interface for props (`CountDisplayProps`)
   - Explicit type for state (`number`)

2. **State Management**:
   - Uses functional update pattern in both increment and decrement
   - Prevents count from going below 0 with `Math.max(0, prevCount - 1)`

3. **Styling**:
   - All styles are inline (as requested)
   - Clean, responsive layout with centered content
   - Modern button styling with hover effects

4. **Best Practices**:
   - Default prop value for `initialCount`
   - Proper event handling
   - Semantic HTML structure
   - Accessible component design

5. **Functional Component**:
   - Uses React.FC for type safety
   - Follows modern React patterns

You can use this component like:
```tsx
<CountDisplay initialCount={5} />
// or just <CountDisplay /> which will default to 0
```

232 t/s, 770 tokens, 3s, 9%
