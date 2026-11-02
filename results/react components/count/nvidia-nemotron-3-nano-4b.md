# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
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

Here is a self‑contained TypeScript functional component that meets all of the requirements:

```tsx
// CountComponent.tsx
import React, { useState } from "react";

/* -------------------------------------------------
   Props type – `initialCount` is optional; defaults to 0
------------------------------------------------- */
type ComponentProps = {
  /** Initial count value (non‑negative number) */
  initialCount?: number;
};

/* -------------------------------------------------
   Functional component with full TypeScript typing
------------------------------------------------- */
const CountDisplay: React.FC<ComponentProps> = ({
  initialCount,
}) => {
  /* `useState` stores a non‑negative integer */
  const [count, setCount] = useState<number>(Number(initialCount));

  /** Increment by one */
  const handleIncrement = () => setCount(c => c + 1);

  /** Decrement only if count > 0 (never below 0) */
  const handleDecrement = () => {
    setCount(prev => Math.max(0, prev - 1));
  };

  /* -------------------------------------------------
     Simple inline styling – no external CSS or libs
------------------------------------------------- */
  return (
    <div style={{ textAlign: "center", marginTop: 40 }}>
      {/* Large, centered heading showing the current count */}
      <h1 style={{ fontSize: "2rem" }}>{count}</h1>

      {/* Buttons with basic styling */}
      <button
        onClick={handleDecrement}
        style={{
          backgroundColor: "#4caf50",
          color: "white",
          padding: "8px 16px",
          borderRadius: "4px",
          fontSize: "1rem",
          marginRight: 12,
        }}
      >
        Decrement
      </button>

      <button
        onClick={handleIncrement}
        style={{
          backgroundColor: "#ff9800",
          color: "white",
          padding: "8px 16px",
          borderRadius: "4px",
          fontSize: "1rem",
          marginLeft: 12,
        }}
      >
        Increment
      </button>
    </div>
  );
};

/* Export the component for reuse */
export default CountDisplay;
```

### How it works

| Piece | Explanation |
|-------|-------------|
| **Prop** `initialCount` (optional) | Accepted via destructuring; defaults to `0`. |
| **State** `count` (`useState<number>`) | Holds the current count, always a non‑negative integer. |
| **Handlers** `handleIncrement` / `handleDecrement` | Simple closures that update state safely (decrease clamps at 0). |
| **Inlines CSS** | All styling is done via `style` objects on `<div>`, `<h1>`, and `<button>` elements. |
| **Modern practice** | Functional component (`React.FC`), pure JSX, no external CSS or libraries. |

You can drop this file into any React project that supports TypeScript (e.g., with Webpack or Vite) and use it like:

```tsx
import CountDisplay from "./CountComponent";

function App() {
  return (
    <div>
      {/* No extra props needed – defaults to 0 */}
      <CountDisplay />
      {/* Or provide an initial value: */}
      {/* <CountDisplay initialCount={5} /> */}
    </div>
  );
}
```

That’s the complete, typed React component you asked for.

225 t/s, 1028 tokens, 5s, 7%
