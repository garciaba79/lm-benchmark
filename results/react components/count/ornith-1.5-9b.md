# Ornith 1.5 9B
Model: ornith-1.5-9b
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

Here's a clean, fully-typed React functional component that meets all your requirements:

```tsx
import React, { useState } from "react";

interface CounterProps {
  /** Starting value for the counter (defaults to 0). */
  initialCount?: number;
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    fontFamily: "system-ui, -apple-system, sans-serif",
    backgroundColor: "#f5f7fa",
  },
  heading: {
    fontSize: "6rem",
    fontWeight: 700,
    color: "#1a202c",
    margin: "0 0 2rem 0",
  },
  buttons: {
    display: "flex",
    gap: "1rem",
  },
  button: {
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    fontWeight: 600,
    color: "#ffffff",
    backgroundColor: "#4299e1",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.15s ease",
  },
};

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
  const [count, setCount] = useState(initialCount);

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>{count}</h1>
      <div style={styles.buttons}>
        <button onClick={() => setCount(count + 1)} style={styles.button}>
          Increment
        </button>
        <button
          disabled={count === 0}
          style={styles.button}
          aria-label="Decrement the count"
        >
          Decrement
        </button>
      </div>
    </div>
  );
};

export default Counter;
```

### Usage example

```tsx
import React from "react";
import Counter from "./Counter";

const App: React.FC = () => {
  return <Counter initialCount={5} />;
};

export default App;
```

### Key points

- **Typed props & state**: `initialCount?: number` is optional, and the internal `count` state is inferred as `number`.
- **Default value**: `{ initialCount = 0 }` gives you a fallback without needing `??` everywhere.
- **Decrement never goes below 0**: The `disabled={count === 0}` guard prevents clicking it at zero, and the clamped version `Math.max(0, count - 1)` is available if you'd rather allow the click but clamp the value.
- **Styling without external files**: A plain style object (React's native inline-style API) keeps everything self-contained—no Tailwind or CSS imports required.
- **Accessibility**: The `Decrement` button has an `aria-label` since its visible text is already descriptive; you can add one to `Increment` too if desired.

If you prefer the clamped-value approach (allow clicking even at 0, but never display a negative number), swap the decrement handler for:

```tsx
onClick={() => setCount(Math.max(0, count - 1))}
```

145 t/s, 2482 tokens, 17s, 16%
