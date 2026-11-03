# Microsoft Phi 4 Mini Instruct
Model: microsoft_phi-4-mini-instruct
Test: Hook Window Size
Created: 11/02/2026, 11:45:17 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a React hook called useWindowSize in TypeScript that returns the current window dimensions as an object { width: number, height: number }. It should update automatically on window resize and handle cleanup properly. Use React 18+ hooks only, no external libraries.

> #### 🤖 Assistant

import * as React from 'react';

interface WindowDimensions {
    width: number;
    height: number;
}

const useWindowSize = () => {
    const [windowDimensions, setWindowDimensions] = React.useState<WindowDimensions>({
        width: window.innerWidth,
        height: window.innerHeight
    });

    // Set up the event listener for resizing when mounted.
    React.useEffect(() => {
        const handleResize = (event) => {
            setWindowDimensions({
                width: window.innerWidth,
                height: window.innerHeight
            });
        };

        window.addEventListener('resize', handleResize);

        return () => {
            // Clean up the event listener when component unmounts or dependencies change.
            window.removeEventListener('resize', handleResize);
        };
    }, []);  // Empty array ensures this effect runs only once after initial render.

    const { width, height } = windowDimensions;

    return [width, height];
};

export default useWindowSize;

165 t/s, 206 tokens, 1s
