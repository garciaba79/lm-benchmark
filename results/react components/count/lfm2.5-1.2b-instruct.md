# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
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

Certainly! Below is a simple React functional component in TypeScript that meets your requirements:

```tsx
import React from 'react';

interface CountProps {
  initialCount?: number;
}

const IncrementDecrementComponent: React.FC<CountProps> = ({
  initialCount = 0,
}) => {
  const [count, setCount] = React.useState(initialCount);

  const handleIncrement = () => {
    setCount(count + 1);
  };

  const handleDecrement = () => {
    if (count > 0) {
      setCount(Math.max(0, count - 1));
    }
  };

  return (
    <div style={{
      maxWidth: '400px',
      margin: '40px auto',
      fontFamily: 'Arial, sans-serif',
      padding: '20px',
      textAlign: 'center'
    }}>
      <h1 style={{
        color: '#2c3e50',
        fontSize: '2em',
        marginBottom: '20px',
      }}>{count}</h1>
      <button
        style={{
          padding: '10px 20px',
          backgroundColor: '#3498db',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
        onClick={handleIncrement}
      >
        Increment
      </button>
      <button
        style={{
          padding: '10px 20px',
          backgroundColor: '#2ecc71',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
        onClick={handleDecrement}
      >
        Decrement
      </button>
    </div>
  );
};

export default IncrementDecrementComponent;
```

### Explanation:
- **Props and State**: The component accepts an `initialCount` prop with a default value of `0`. It uses React's `useState` hook to manage the count.
- **Increment/Decrement Logic**: 
  - "Increment" increases the count by 1.
  - "Decrement" decreases the count by 1, ensuring it never goes below 0.
- **Styling**: Basic inline styles are used for layout and visual appeal. You can expand on this with more CSS if needed.
- **TypeScript Types**: The component is fully typed using TypeScript interfaces.
- **Modern React Practices**: Uses functional components, hooks (`useState`), and proper prop typing.

You can use this component in your application by importing it like so:

```tsx
import React from 'react';
import IncrementDecrementComponent from './IncrementDecrementComponent';

const App = () => {
  return (
    <div>
      <IncrementDecrementComponent initialCount={5} />
    </div>
  );
};

export default App;
```

580 t/s, 661 tokens, 1s, 5%
