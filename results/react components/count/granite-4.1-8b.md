# Granite 4.1 8B
Model: granite-4.1-8b
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

Certainly! Below is a simple React functional component written in TypeScript that meets your requirements. It uses inline styles for basic styling and adheres to modern React principles.

```tsx
import React, { useState } from 'react';

// Define a type for the props of the component
type CounterProps = {
  initialCount?: number; // Optional prop with default value of 0
};

/**
 * A simple counter component that displays a count and allows incrementing or decrementing it.
 * @param {CounterProps} props - The props passed to the component, including an optional initialCount.
 */
const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // Use state to keep track of the current count
  const [count, setCount] = useState<number>(initialCount);

  // Function to handle incrementing the count
  const handleIncrement = () => {
    setCount(count + 1);
  };

  // Function to handle decrementing the count, ensuring it doesn't go below 0
  const handleDecrement = () => {
    if (count > 0) {
      setCount(count - 1);
    }
  };

  // Inline styles for basic centering and button styling
  const style: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh', // Ensure the component takes up at least full viewport height
    textAlign: 'center',
    padding: '20px',
  };

  return (
    <div style={style}>
      {/* Display the current count in a large heading */}
      <h1>{count}</h1>

      {/* Increment button */}
      <button onClick={handleIncrement} style={{ margin: '5px', padding: '10px' }}>
        Increment
      </button>

      {/* Decrement button, disabled if count is 0 */}
      <button onClick={handleDecrement} style={{ margin: '5px', padding: '10px' }} disabled={count === 0}>
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

### Explanation:
- **Props**: The component accepts an optional `initialCount` prop of type `number`, which defaults to `0` if not provided.
- **State**: It uses the `useState` hook to manage the `count` state, initialized with `initialCount`.
- **Event Handlers**:
  - `handleIncrement`: Increments the count by `1`.
  - `handleDecrement`: Decrements the count by `1`, but only if the current count is greater than `0` to prevent negative values.
- **Styling**: Inline styles are used to center the content and style the buttons. The component ensures it occupies at least the full viewport height for visibility.
- **Accessibility**: The decrement button is disabled when the count reaches `0`, providing a small accessibility hint that no further decrement is possible.

This component can be imported and used in other parts of your React application, passing an optional `initialCount` prop if needed.

127 t/s, 649 tokens, 5s, 5%
