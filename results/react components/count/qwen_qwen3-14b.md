# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: component count
Created: 11/02/2026, 05:35:23 AM
Exported from: LM Studio (via test script)
Context 8K

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
import React, { useState } from 'react';

// Define the props interface with optional `initialCount` and default value
interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // Initialize state with the provided initial count or default to 0
  const [count, setCount] = useState<number>(initialCount);

  // Handle increment logic
  const handleIncrement = () => {
    setCount(count + 1);
  };

  // Handle decrement logic with a guard against negative values
  const handleDecrement = () => {
    setCount(prevCount => Math.max(prevCount - 1, 0));
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      textAlign: 'center',
      backgroundColor: '#f9f9f9',
      padding: '20px'
    }}>
      {/* Display the current count in a large heading */}
      <h1 style={{ 
        fontSize: '3em', 
        marginBottom: '2em',
        color: '#333'
      }}>
        {count}
      </h1>

      {/* Container for buttons with horizontal layout and spacing */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '1.5em'
      }}>
        {/* Increment Button */}
        <button
          onClick={handleIncrement}
          style={{
            padding: '0.75em 1.5em',
            fontSize: '1em',
            borderRadius: '5px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.2s ease'
          }}
        >
          Increment
        </button>

        {/* Decrement Button */}
        <button
          onClick={handleDecrement}
          style={{
            padding: '0.75em 1.5em',
            fontSize: '1em',
            borderRadius: '5px',
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.2s ease'
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

### ✅ Features Implemented:

- **TypeScript Typing**: All props and state are properly typed.
- **Default Prop Handling**: `initialCount` defaults to `0` if not provided.
- **State Management**: Uses React's `useState` hook for managing the count.
- **Increment/Decrement Logic**:
  - Increment increases the count by 1.
  - Decrement decreases it by 1, but ensures it never goes below 0.
- **Styling**:
  - Inline styles are used to center content and style buttons.
  - Buttons have hover effects via `transition` for a better UX.
- **Modern React Practices**: Functional component with hooks, no class components or external CSS.

---

### 📌 Notes:

- The component is self-contained and does not rely on any external libraries or stylesheets.
- It follows best practices by using TypeScript interfaces and function components.

10 t/s, 2225 tokens, 227s, 29%
