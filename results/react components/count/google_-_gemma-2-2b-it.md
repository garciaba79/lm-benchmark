# Gemma 2 2B Instruct
Model: google_-_gemma-2-2b-it
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

```typescript
import React, { useState } from 'react';

interface Props {
  initialCount: number;
}

const CounterApp: React.FC<Props> = ({ initialCount }) => {
  const [count, setCount] = useState(initialCount);

  const increment = () => {
    setCount((prev) => prev + 1);
  };

  const decrement = () => {
    if (count > 0) {
      setCount((prev) => prev - 1);
    }
  };

  return (
    <div style={{ textAlign: 'center', margin: '20px auto' }}>
      <h1>Count: {count}</h1>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
    </div>
  );
};

export default CounterApp;
```


**Explanation:**

1. **Imports:** We start by importing the necessary modules from React: `React` and `useState`.
2. **Props Type:** The interface `Props` specifies that the component expects a prop called `initialCount`, which should be of type number (defaulting to 0).
3. **Functional Component:**  We define our functional component as a TypeScript class named `CounterApp` using the `React.FC` decorator, ensuring it adheres to React's Functional Components requirements. The input props are passed into the function via a destructuring assignment syntax: `{ initialCount }`.

4. **State Management:** We use the built-in  state management hook `useState` to track and manage the `count` variable inside the component using `setCount`. This allows us to update the count based on button clicks.
5. **Increment Function:** The `increment()` function is a simple helper that increases the count by 1 when called, updating the state with `setCount((prev) => prev + 1)`

6. **Decrement Function:**  The `decrement()` function checks if the current count is greater than zero before decrementing. If so, it decrements the count using `setCount((prev) => prev - 1)`.
7. **JSX Structure:** We create a `div` to hold all our elements and style them using inline styles for centering:

*   **Heading:**  The heading is styled with `h1` tag in the JSX code, displaying the current count.
*   **Buttons:** The increment and decrement buttons are rendered as `<button>` tags with appropriate `onClick` handlers to call the corresponding functions. 


This component provides a simple counter that can be used for various purposes like tracking user input or managing data within an application.

Let me know if you have any other questions!

234 t/s, 580 tokens, 3s, 9%
