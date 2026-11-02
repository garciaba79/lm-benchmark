# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
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

Here's a well-structured and typed React functional component in TypeScript that meets all your requirements:

```tsx
import React, { useState } from 'react';

// Define props interface with optional initialCount
interface CountProps {
  initialCount?: number;
}

const Counter: React.FC<CountProps> = ({ initialCount = 0 }) => {
  // State initialized with prop or default 0
  const [count, setCount] = useState<number>(initialCount);

  // Increment handler
  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  // Decrement handler with floor at 0
  const decrement = () => {
    if (count > 0) {
      setCount(prevCount => prevCount - 1);
    }
  };

  // Inline styles for components
  const headingStyle = {
    fontSize: '3rem',
    textAlign: 'center',
    marginBottom: '20px',
    color: '#333'
  };

  const buttonStyle = {
    padding: '10px 20px',
    margin: '5px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    transition: 'background-color 0.3s'
  };

  const incrementButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#4CAF50' // Green
  };

  const decrementButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#f44336' // Red
  };

  return (
    <div style={{ maxWidth: '300px', margin: '0 auto', padding: '20px' }}>
      <h1 style={headingStyle}>{count}</h1>
      
      <button 
        style={incrementButtonStyle} 
        onClick={increment}
      >
        Increment
      </button>
      
      <button 
        style={decrementButtonStyle} 
        onClick={decrement}
      >
        Decrement
      </button>
    </div>
  );
};

export default Counter;
```

### Key Features:
1. **Type Safety**: 
   - `CountProps` interface defines optional `initialCount` prop
   - State is properly typed as number
   - All event handlers use type-safe state updates

2. **Styling**:
   - Uses inline styles for all components
   - Semantic color coding (green for increment, red for decrement)
   - Responsive container with max-width and auto margin
   - Smooth transitions on button hover

3. **Functionality**:
   - Count never goes below 0
   - Clean state management with `useState`
   - Proper event handling with arrow functions

4. **Best Practices**:
   - Functional component with hooks
   - Pure render (state changes trigger re-renders)
   - Clear separation of concerns
   - Prop default value handling

To use this component, simply import and include it in your app:

```tsx
import Counter from './Counter';

function App() {
  return <Counter initialCount={5} />; // Or omit prop for default 0
}
```

103 t/s, 1887 tokens, 19s, 13%
