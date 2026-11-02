# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
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

Here is an example of how you can implement this in TypeScript with React functional components using hooks (useState):

```tsx
import * as React from 'react';

interface Props {
  initialCount?: number; // optional prop for the initial count value. Default to 0 if not provided.
}

const Counter: React.FC<Props> = ({initialCount = 0}) => {
   const [count, setCount] = React.useState(initialCount);
   
   return (
      <div style={{textAlign:'center', marginTop:'50px'}}> 
        <h1 style={{fontSize: '48px'}}>{count}</h1>
        
         <button 
           onClick={() => setCount(prevCount => prevCount + 1)}
           style={{marginRight: '20px', fontSize:'20px', padding:'10px 20px'}}  
         > 
            Increment 
        </button>
        
         <button 
           onClick={() => setCount(prevCount => Math.max(prevCount - 1, 0))}
           style={{fontSize:'20px', padding:'10px 20px'}}  
         > 
            Decrement 
        </button>
      </div>
    );
};

export default Counter;
```
This component uses React hooks to manage state. The `useState` hook is used here for managing the count value, and it takes an initial count as a prop (defaulting to 0 if not provided). Inside the JSX of this component, we display the current count in a large heading, with two buttons that call `setCount` when clicked - one increments by 1, the other decrements by 1 but never goes below zero. The inline styles are used for styling purposes.

157 t/s, 430 tokens, 3s, 4%
