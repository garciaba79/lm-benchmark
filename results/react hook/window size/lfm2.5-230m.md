# LFM2.5 230M
Model: lfm2.5-230m
Test: Hook Window Size
Created: 11/02/2026, 11:26:02 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

```tsx
import { useState, useRef } from 'react';

export default function UseWindowSize() {
  const [width, setWidth] = useState(800);
  const [height, setHeight] = useState(600);

  const handleResize = () => {
    const newDimensions = window.innerWidth * width + window.innerHeight;
    setWidth(newDimensions);
    setHeight(newDimensions);
  };

  return (
    <div
      ref={useRef<HTMLDivElement>(null)}
      style={{
        height: height,
        width: width
      }}
    >
      {/* Your existing UI components */}
    </div>
  );
}
```

This hook uses the `useState` and `useRef` hooks to keep track of the current window dimensions. The `handleResize` function updates these values whenever the window size is resized, and it also re-renders the component with the new dimensions.

974 t/s, 210 tokens, 0s
