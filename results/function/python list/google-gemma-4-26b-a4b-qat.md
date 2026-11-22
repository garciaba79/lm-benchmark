# Gemma 4 26B A4B QAT
Model: google/gemma-4-26b-a4b-qat
Test: Function Python List
Created: 11/22/2026, 03:01:10 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here is the clean Python implementation using the standard library.

```python
from typing import List, Dict, Any

def count_fruit_occurrences(items: List[Any]) -> Dict[str, int]:
    """
    Counts the occurrences of each string in a list.

    Args:
        items: A list of items to count.

    Returns:
        A dictionary where keys are unique strings and values are their counts.

    Raises:
        ValueError: If any item in the list is not a string.
    """
    # Handle empty list case
    if not items:
        return {}

    counts = {}
    
    for item in items:
        # Error handling: Ensure every item is a string
        if not isinstance(item, str):
            raise ValueError(f"All items in the list must be strings. Found: {type(item).__name__} ('{item}')")
        
        # Update count in dictionary
        counts[item] = counts.get(item, 0) + 1
            
    return counts

# --- Example Usage ---

# 1. Successful case
fruits = ["apple", "banana", "apple", "cherry"]
try:
    result = count_fruit_occurrences(fruits)
    print(f"Input list: {fruits}")
    print(f"Result dictionary: {result}")
except ValueError as e:
    print(f"Error: {e}")

print("-" * 30)

# 2. Empty list case
empty_list = []
print(f"Input empty list: {empty_list}")
print(f"Result: {count_fruit_occurrences(empty_list)}")

print("-" * 30)

# 3. Error case (containing an integer)
mixed_list = ["apple", 42, "banana"]
try:
    print(f"Input mixed list: {mixed_list}")
    count_fruit_occurrences(mixed_list)
except ValueError as e:
    print(f"Caught expected error: {e}")
```

### Explanation:
1.  **Type Hinting**: I used `List[Any]` and `Dict[str, int]` to make the function signature professional and clear about what data types to expect and return.
2.  **`dict.get(item, 0)`**: This is a clean, idiomatic way to handle keys that aren't in the dictionary yet. It attempts to find the current count; if it doesn't exist, it defaults to `0`, then adds `1`.
3.  **Error Handling**:
    *   **Empty List**: The `if not items:` check explicitly handles empty inputs by returning an empty dictionary immediately.
    *   **Type Check**: Using `isinstance(item, str)` is the standard way to validate types in Python. If a non-string is found, it raises a `ValueError` with a descriptive message including the problematic value's type.
4.  **Complexity**: The function runs in $O(n)$ time, where $n$ is the number of elements in the list, as it only iterates through the list once.

56 t/s, 696 tokens, 13s, 5%
