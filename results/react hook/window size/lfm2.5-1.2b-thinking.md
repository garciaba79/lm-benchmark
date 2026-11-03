# LFM2.5 1.2B Thinking
Model: lfm2.5-1.2b-thinking
Test: Hook Window Size
Created: 11/02/2026, 11:29:22 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here's an implementation of the `useWindowSize` hook in TypeScript using React 18+ hooks only, with proper cleanup:

```typescript
import { useEffect, useRef } from 'react';

interface WindowSize {
  width: number;
  height: number;
}

const useWindowSize = () => {
  const windowSizeRef = useRef<WindowSize | null>(null);

  useEffect(() => {
    // Initialize on first mount
    if (!windowSizeRef.current) {
      windowSizeRef.current = { width: window.innerWidth, height: window.innerHeight };
    } else {
      windowSizeRef.current = { width: window.innerWidth, height: window.innerHeight };
    }
  }, []);

  // Cleanup on unmount
  return () => {
    if (windowSizeRef.current) {
      window.removeEventListener('resize', handleWindowSize);
    }
  };

  private handleWindowSize() {
    const currentWidth = window.innerWidth;
    const currentHeight = window.innerHeight;
    windowSizeRef.current = { width: currentWidth, height: currentHeight };
  }
};

export default useWindowSize;
```

**Key features:**
1. **Initialization:** Sets initial dimensions on first render
2. **Cleanup:** Removes resize event listener when component unmounts to prevent memory leaks
3. **Type safety:** Uses TypeScript interfaces for type consistency
4. **Efficiency:** Only initializes once and updates on every resize event

The hook:
- Returns a stable object { width: number, height: number }
- Automatically updates on window resizing
- Gracefully cleans up resources on unmount
- Handles edge cases (first mount, component removal) properly

Usage example:
```tsx
const Header = () => {
  const size = useWindowSize();
  return <div style={{ width: size.width, height: size.height }}>Container</div>;
};
```

514 t/s, 5063 tokens, 10s
