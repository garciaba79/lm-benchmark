# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
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

  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1);
  };

  const handleDecrement = () => {
    setCount(prevCount => Math.max(0, prevCount - 1));
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <h1 style={{ fontSize: '3rem' }}>{count}</h1>
      <button onClick={handleIncrement} style={{ padding: '10px 20px', margin: '5px' }}>Increment</button>
      <button onClick={handleDecrement} style={{ padding: '10px 20px', margin: '5px' }}>Decrement</button>
    </div>
  );
};

export default Counter;
```

### Explanation:

- **Props**: The component accepts an optional `initialCount` prop of type number. If not provided, it defaults to 0.
  
- **State**: The count is managed using the `useState` hook.

- **Handlers**:
  - `handleIncrement`: Increases the count by 1.
  - `handleDecrement`: Decreases the count by 1 but ensures it never goes below 0.

- **Styling**: Inline styles are used to center the content both vertically and horizontally. The heading is styled with a large font size, and buttons have some padding for better visibility.

### Usage:

You can use this component in your React application like so:

```tsx
import React from 'react';
import ReactDOM from 'react-dom';
import Counter from './Counter';

const App: React.FC = () => {
  return (
    <div>
      <h1>Welcome to the Counter App</h1>
      <Counter initialCount={5} />
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
```

This will render a counter starting from 5, with buttons to increment and decrement it.

149 t/s, 494 tokens, 3s, 4%
