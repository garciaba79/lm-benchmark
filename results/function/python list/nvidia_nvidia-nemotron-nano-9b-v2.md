# Nvidia NVIDIA Nemotron Nano 9B v2
Model: nvidia_nvidia-nemotron-nano-9b-v2
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean Python function with error handling and example usage:

```python
def count_fruits(fruit_list):
    if not fruit_list:
        return {}
    for fruit in fruit_list:
        if not isinstance(fruit, str):
            raise ValueError("All items must be strings")
    counts = {}
    for fruit in fruit_list:
        counts[fruit] = counts.get(fruit, 0) + 1
    return counts

# Example usage
print(count_fruits(["apple", "banana", "apple", "cherry"]))  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}
print(count_fruits([]))  # Output: {}
```

This implementation:
1. Returns an empty dictionary for empty input lists
2. Validates all elements are strings before counting
3. Uses `dict.get()` for efficient counting
4. Raises clear ValueError with message if non-string items found

The example shows both normal operation and empty list handling. To test the error case, you could add:
```python
try:
    count_fruits(["apple", 123, "banana"])
except ValueError as e:
    print(e)  # Output: All items must be strings
```

104 t/s, 1236 tokens, 12s, 8%
