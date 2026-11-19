# DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic
Model: deepseek-v4-pro-qwen3.5-9b-uncensored-heretic
Test: component count
Created: 11/18/2026, 11:45:43 PM
Exported from: LM Studio (via test script)
Context unknown

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

```tsx
import React from 'react';

interface CounterProps {
  initialCount?: number;
}

const Counter: React.FC<CounterProps> = ({ initialCount = 0 }) => {
 const [count, setCount] = React.useState<number>(initialCount);

 const increment = () => {
 setCount((prev) => prev + 1);
 };

 const decrement = () => {
 if (count > 0) {
 setCount((prev) => prev - 1);
 }
 };

 return (
 <div style={styles.container}>
 <h1 style={styles.heading}>{count}</h1>
 <button onClick={increment} style={styles.button}>
 Increment
 </button>
 <button onClick={decrement} style={styles.button}>
 Decrement
 </button>
 </div>
 );
};

// Basic CSS-in-JS styles object
const styles = {
 container: {
 display: 'flex',
 flexDirection: 'column' as const,
 alignItems: 'center',
 justifyContent: 'center',
 minHeight: '100vh',
 fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
 backgroundColor: '#f5f7fa',
 padding: '2rem',
 },
 heading: {
 fontSize: '4rem',
 fontWeight: 800,
 color: '#1a1a2e',
 marginBottom: '2rem',
 transition: 'color 0.3s ease',
 },
 button: {
 backgroundColor: '#4f46e5',
 color: 'white',
 border: 'none',
 padding: '0.8rem 2rem',
 fontSize: '1.2rem',
 fontWeight: 600,
 borderRadius: '12px',
 cursor: 'pointer',
 transition: 'background-color 0.2s ease, transform 0.1s ease',
 margin: '0.5rem',
 boxShadow: '0 4px 6px rgba(79, 70, 229, 0.3)',
 },
} as const;

export default Counter;
```

156 t/s, 470 tokens, 3s
