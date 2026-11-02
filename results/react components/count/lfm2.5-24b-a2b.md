# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
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

Below is a **complete, self‑contained** React functional component written in TypeScript.  
It meets every requirement you listed:

* Accepts `initialCount` (default 0) via props  
* Shows the count in a large centered heading  
* Two buttons – “Increment” and “Decrement” – with proper state handling  
* Decrement never goes below 0  
* Uses only inline styles / CSS‑in‑JS objects (no external files or libraries)  
* All props & state are fully typed  

```tsx
import React, { useState } from 'react';

/* --------------------------------------------------------------
   1️⃣  Props definition – TypeScript interface
   -------------------------------------------------------------- */
interface CounterProps {
  /** Starting value for the counter (optional) */
  initialCount?: number;
}

/* --------------------------------------------------------------
   2️⃣  Inline style objects (CSS‑in‑JS)
   -------------------------------------------------------------- */
const containerStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column' as const,
  alignItems: 'center' as const,
  justifyContent: 'center' as const,
  padding: '2rem',
  border: '1px solid #ddd',
  borderRadius: '8px',
  width: '300px',
};

const headingStyle: React.CSSProperties = {
  fontSize: '2.5rem',
  marginBottom: '1rem',
  color: '#222',
};

const buttonContainerStyle: React.CSSProperties = {
  display: 'flex',
  gap: '0.75rem',
  marginTop: '1rem',
};

const baseButtonStyle: React.CSSProperties = {
  padding: '0.5rem 1rem',
  fontSize: '1rem',
  cursor: 'pointer',
  border: 'none',
  borderRadius: '4px',
  transition: 'background-color 0.2s',
};

const incrementButtonStyle = { ...baseButtonStyle, backgroundColor: '#007bff', color: '#fff' };
const decrementButtonStyle = { ...baseButtonStyle, backgroundColor: '#dc3545', color: '#fff' };

/* --------------------------------------------------------------
   3️⃣  Component
   -------------------------------------------------------------- */
const Counter: React.FC<CounterProps> = ({ initialCount }) => {
  // State typed as number; fallback to 0 when undefined (or null)
  const [count, setCount] = useState<number>(initialCount ?? 0);

  // Handlers
  const increment = () => setCount(prev => prev + 1);
  const decrement = () => setCount(prev => Math.max(prev - 1, 0));

  return (
    <div style={containerStyle}>
      {/* Large centered heading */}
      <h1 style={headingStyle}>Current Count</h1>

      {/* Button row */}
      <div style={buttonContainerStyle}>
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
    </div>
  );
};

export default Counter;
```

### How it works
1. **Props** – `CounterProps` defines an optional `initialCount`.  
2. **State** – `useState<number>` holds the current count, defaulting to 0 when no prop is supplied (`initialCount ?? 0`).  
3. **Behavior** –  
   * `increment` adds 1.  
   * `decrement` subtracts 1 but clamps the result with `Math.max(prev - 1, 0)`.  
4. **Styling** – All visual presentation lives in plain JavaScript objects (`React.CSSProperties`). The buttons get distinct colors (blue for increment, red for decrement).  

You can now import `<Counter />` anywhere in your app and use it like:

```tsx
import Counter from './Counter';

function App() {
  return <Counter initialCount={5} />;
}
```

The component follows modern React conventions (functional component + hooks) and is fully typed for safety. Enjoy!

108 t/s, 3794 tokens, 36s, 24%
