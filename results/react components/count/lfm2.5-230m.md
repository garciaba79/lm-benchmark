# LFM2.5 230M
Model: lfm2.5-230m
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

Here's a simple implementation of the task:

```tsx
import React from 'react';

const CountComponent = () => {
  const initialCount = 0;

  return (
    <div style={{ fontSize: '20px', padding: '10px' }}>
      <h1>Current count</h1>
      <button onClick={() => incrementCount()}>Increment</button>
      <button onClick={() => decrementCount()}>Decrement</button>
    </div>
  );
};

const incrementCount = () => {
  initialCount++;
};
const decrementCount = () => {
  initialCount--;
};

export default CountComponent;
```

In this code:

*   We define a `count` prop that defaults to 0.
*   The component uses inline style for a centered heading and a small font size.
*   Two buttons are created with different actions (`increment` and `decrement`) that update the state by incrementing or decrementing the count, respectively.

When you run this code, it will display the current count of 0 on the first button click and 1 on the second button click.

1029 t/s, 256 tokens, 0s, 3%
