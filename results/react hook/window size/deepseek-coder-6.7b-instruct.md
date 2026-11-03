# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
Test: Hook Window Size
Created: 11/02/2026, 12:40:06 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here is how you can create a custom useWindowSize hook in TypeScript using the new features of React 18 (React Hooks):

```tsx
import { useState, useEffect } from 'react';

const useWindowSize = () => {
    const [windowSize, setWindowSize] = useState({ width: window.innerWidth, height: window.innerHeight });
    
    // Handle resize event and update state with new dimensions
    const handleResize = () => { 
        setWindowSize({ width: window.innerWidth, height: window.innerHeight })
    };
  
    useEffect(() => {
      // Add the event listener when component mounts
      window.addEventListener('resize', handleResize);
      
      return () => {
          // Remove the event listener on cleanup to prevent memory leaks
          window.removeEventListener('resize', handleResize) 
        };  
    }, []);
    
    return windowSize;
};
```
In this hook, we use `useState` and `useEffect` from React Hooks API to manage the state of our component. The initial value for width and height is set as current innerWidth and innerHeight respectively when the component mounts. 

The event listener is added in a side effect that runs only once on component mount (empty dependency array []). When this hook is used, it will return an object with `width` and `height` properties representing the window's size at any given moment. The returned value updates automatically whenever the browser window resizes thanks to the event listener we set up in useEffect.

154 t/s, 360 tokens, 2s
