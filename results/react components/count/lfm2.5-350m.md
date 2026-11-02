# LFM2.5 350M
Model: lfm2.5-350m
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

```typescript
import React, { useState } from 'react';

interface IncrementProps {
  initialCount: number;
}

const IncrementComponent: React.FC<IncrementProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState<number>(initialCount);

  return (
    <header>
      <h1 style={{ textAlign: 'center' }}>Count: {count}</h1>
    </header>
    <button onClick={() => setCount(count + 1)}>Increment</button>
    <button onClick={() => setCount(count - 1)}>Decrement</button>
  );
};

export default IncrementComponent;
```

828 t/s, 165 tokens, 0s, 2%
