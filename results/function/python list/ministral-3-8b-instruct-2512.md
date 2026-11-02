# Ministral 3 8B Instruct 2512
Model: ministral-3-8b-instruct-2512
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean Python function that meets your requirements, including error handling and an example usage:

```python
from collections import defaultdict

def count_fruits(fruit_list):
    """
    Counts occurrences of each unique fruit in a list.

    Args:
        fruit_list: List of strings representing fruits.

    Returns:
        Dictionary with fruits as keys and their counts as values.

    Raises:
        ValueError: If the input list is empty or contains non-string items.
    """
    if not fruit_list:
        return {}

    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings. Found invalid item: {item}")

    counts = defaultdict(int)
    for fruit in fruit_list:
        counts[fruit] += 1

    return dict(counts)

# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        ["apple", "banana", "apple", "cherry"],  # Normal case
        [],                                      # Empty list
        ["apple", 123, "banana"],                # Invalid item (should raise error)
        ["orange", "orange", "orange"]           # All same fruit
    ]

    for i, fruits in enumerate(test_cases):
        print(f"\nTest case {i+1}: {fruits}")
        try:
            result = count_fruits(fruits)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)
```

Key features:
1. Uses `defaultdict` for clean counting implementation
2. Proper error handling for empty lists and non-string items
3. Clear docstring explaining the function's purpose
4. Example usage with multiple test cases showing both success and error scenarios

The output will show:
- Normal counting behavior
- Empty list returns empty dict
- Non-string item raises ValueError
- All same fruit case works correctly

You can use just the `count_fruits()` function in your code, or run the example usage section to see it in action.

127 t/s, 443 tokens, 4s, 7%
