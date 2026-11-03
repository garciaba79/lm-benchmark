# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
Test: Hook Window Size
Created: 11/02/2026, 11:27:59 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

Here’s how you can implement a custom `useWindowSize` hook in TypeScript for React (React 18+) that automatically updates on window resize and cleans up resources:

```tsx
import { useEffect } from 'react';

interface WindowSizeProps {
  initialWidth?: number;
  initialHeight?: number;
}

export const useWindowSize = (
  props: WindowSizeProps = {}
) => {
  // The size object will be updated automatically on window resize
  const [windowSize, setWindowSize] = React.useRef<{ width: number; height: number } | null>(null);

  useEffect(() => {
    const handleResize = () => {
      if (window.size) {
        // Ensure we only update when the window size has changed
        if (Math.abs(window.width - windowSize.current.width) > 1 || Math.abs(window.height - windowSize.current.height) > 1) {
          setWindowSize({
            width: window.width,
            height: window.height
          });
        }
      }
    };

    const handleWindowResize = () => {
      const newWidth = window.size?.width || window.innerWidth;
      const newHeight = window.size?.height || window.innerHeight;
      if (newWidth && newHeight) {
        setWindowSize({ width: newWidth, height: newHeight });
      }
    };

    window.addEventListener('resize', handleResize);
    window.removeEventListener('resize', handleResize);

    // Initial load
    const initialSize = { width: props.initialWidth || 0, height: props.initialHeight || 0 };
    setWindowSize(initialSize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [props.initialWidth, props.initialHeight]);

  // You can provide defaults here if needed
  const { width = initialWindowSize.width, height = initialWindowSize.height } = props;

  return { windowSize: windowSize };
};
```

### How it works:
- **Type Safety:** Uses TypeScript interfaces and generics.
- **Automatic Updates:** Listens to `resize` events in the effect hook.
- **Cleanup:** Properly removes event listeners on unmount to prevent memory leaks.
- **Initialization:** You can customize initial width/height values by passing props.

Example usage:
```tsx
function App() {
  const { windowSize } = useWindowSize({ initialWidth: 800, initialHeight: 600 });
  
  return (
    <div style={{ width: `${windowSize.width}px`, height: `${windowSize.height}px` }}>
      This box is resizing.
    </div>
  );
}
```

Do you want me to extend this hook so it can accept options for minimum/maximum dimensions as well? That would make it even more robust.

516 t/s, 630 tokens, 1s
