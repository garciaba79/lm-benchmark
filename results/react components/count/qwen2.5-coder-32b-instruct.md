# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
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

Certainly! Below is a simple React functional component written in TypeScript that meets your requirements. The component uses inline styles for styling and follows modern React principles, including proper typing of props and state.

```tsx
import React, { useState } from 'react';

// Define the type for the component's props
interface CounterProps {
  initialCount?: number; // Optional prop with a default value
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  // Use the initialCount prop to set the initial state of count
  const [count, setCount] = useState<number>(initialCount);

  // Function to increment the count
  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1);
  };

  // Function to decrement the count, ensuring it doesn't go below 0
  const handleDecrement = () => {
    setCount(prevCount => Math.max(prevCount - 1, 0));
  };

  // Basic inline styles for the component
  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f0f0f0',
    fontFamily: 'Arial, sans-serif',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '3rem',
    marginBottom: '20px',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '10px 20px',
    margin: '5px',
    fontSize: '1.2rem',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#007bff',
    color: '#fff',
    transition: 'background-color 0.3s ease',
  };

  const buttonHoverStyle: React.CSSProperties = {
    backgroundColor: '#0056b3',
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>{count}</h1>
      <button
        style={{ ...buttonStyle, ...(hover ? buttonHoverStyle : {}) }}
        onClick={handleIncrement}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
      >
        Increment
      </button>
      <button
        style={{ ...buttonStyle, ...(hover ? buttonHoverStyle : {}) }}
        onClick={handleDecrement}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
      >
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

### Explanation:
1. **Props Typing:** The `Counter` component accepts an optional prop `initialCount` of type `number`. If not provided, it defaults to `0`.

2. **State Management:** The `useState` hook is used to manage the count state.

3. **Button Logic:** 
   - The `handleIncrement` function increases the count by 1.
   - The `handleDecrement` function decreases the count by 1 but ensures it doesn't go below 0 using `Math.max`.

4. **Styling:** Inline styles are used for layout and button appearance, including hover effects.

5. **Hover Effects:** Added a simple hover effect to change the button color on mouse enter/leave events.

### Note:
- The hover state management was mistakenly included in the above code snippet. If you don't need hover effects, you can remove the `hover` state and related logic.
  
Here is the corrected version without hover effects:

```tsx
import React, { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1);
  };

  const handleDecrement = () => {
    setCount(prevCount => Math.max(prevCount - 1, 0));
  };

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f0f0f0',
    fontFamily: 'Arial, sans-serif',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '3rem',
    marginBottom: '20px',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '10px 20px',
    margin: '5px',
    fontSize: '1.2rem',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#007bff',
    color: '#fff',
    transition: 'background-color 0.3s ease',
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>{count}</h1>
      <button style={buttonStyle} onClick={handleIncrement}>
        Increment
      </button>
      <button style={buttonStyle} onClick={handleDecrement}>
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

This should work perfectly as per your requirements!

6 t/s, 1137 tokens, 202s, 8%
