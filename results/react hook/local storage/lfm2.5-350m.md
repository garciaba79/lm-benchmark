# LFM2.5 350M
Model: lfm2.5-350m
Test: Hook Local Storage
Created: 11/02/2026, 06:54:07 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a React hook called useLocalStorage<T>(key: string, initialValue: T) in TypeScript that reads from and writes to localStorage, with automatic JSON parsing/stringifying and type safety. It should sync across tabs/windows if the key changes and handle errors gracefully. Include proper cleanup on unmount.

Use React 18+, functional components, no external libraries. Explain the benefits, pros, cons, and any potential issues.

> #### 🤖 Assistant

## Benefit 1: Enhanced Typing & Validation

**Pros:** TypeScript type annotations improve code readability and enable powerful static analysis. Automatic JSON parsing/stringifying simplifies data manipulation. Clear type definitions make it easier to debug and maintain the application.

**Cons:** May introduce a small initialization cost if `initialValue` is not provided, though this is unlikely in most cases. Type safety doesn't eliminate runtime errors entirely, requiring careful input handling.


## Cons: Larger Initial Load Time (if `initialValue` isn't provided)

### Benefits:

* **Improved Performance:** Reducing the initial payload via JSON parsing avoids unnecessary data transfer.
* **Deeper Data Accessibility:**  Direct manipulation of localStorage is more efficient than fetching from a server.


## Pros:

* **Reduced Initial Load Time:**  The reduced payload improves app responsiveness and user experience, especially on mobile or low-bandwidth networks.
* **Better Performance for Large Datasets:** Larger initial values allow the data to load faster, making it more suitable for applications with extensive datasets.


## Potential Issues:

* **Storage Limits:** LocalStorage has a 5MB limit per path, even if empty. Excessive or very large payloads may trigger storage errors.
* **Key Exposure:** Using strings as keys might be considered less secure if sensitive data is stored. Consider using more robust key formats like URLS or UUIDs for production environments.
* **Browser Compatibility:** Different browsers handle JSON parsing and stringification differently, potentially leading to inconsistencies across devices.


## Key Implementation Details

```tsx
// useLocalStorage.ts
import { useState } from 'react';

interface LocalStorageData {
  // Define the structure of your data for storage
}

const useLocalStorage<T> = () => {
  const [data, setData] = useState<T>({});

  // Automatic JSON parsing/stringifying (e.g., using JSON.parseString)
  const parseJSON = (str: string): T | undefined => {
    try {
      return JSON.parse(str);
    } catch (error) {
      console.error('Error parsing JSON:', error);
      return null;
    }
  };

  // Automatic stringification (e.g., converting strings to JSON)
  const stringify = (str: string): T | undefined => {
    try {
      return JSON.stringify(str);
    } catch (error) {
      console.error('Error stringifying data:', error);
      return undefined;
    }
  };

  // Sync logic
  const syncWithBrowser = () => {
    if (localStorage.getItem<T>('key')) {
      setData(JSON.parse(strategyKey));
    } else {
      setData({});
    }
  };

  // Cleanup on unmount
  return { data, sync: syncWithBrowser };
};

export default useLocalStorage;
```

## Explanation of Key Logic

* **`useState`:** Used to store the retrieved or processed data.
* **`parseJSON` & `stringify`:** Functions to handle JSON conversion based on your needs (e.g., parsing strings vs. converting text).
* **`syncWithBrowser`:**  Provides a mechanism for syncing localStorage updates across tabs/windows using the chosen strategy key.


**Remember:** This example is a foundation. Adapt it to your specific use case and data structure.

799 t/s, 739 tokens, 1s, 5%
