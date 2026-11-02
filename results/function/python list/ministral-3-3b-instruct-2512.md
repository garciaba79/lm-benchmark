# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean Python function that meets your requirements:

```python
def count_fruits(fruit_list):
    """
    Counts occurrences of each unique fruit in a list.

    Args:
        fruit_list (list): List of strings representing fruits

    Returns:
        dict: Dictionary with fruits as keys and counts as values

    Raises:
        ValueError: If input is empty or contains non-string items
    """
    # Error handling for empty list
    if not fruit_list:
        return {}

    # Check all items are strings
    if not all(isinstance(item, str) for item in fruit_list):
        raise ValueError("All items in the list must be strings")

    # Count occurrences of each fruit
    counts = {}
    for fruit in fruit_list:
        counts[fruit] = counts.get(fruit, 0) + 1

    return counts

# Example usage
if __name__ == "__main__":
    # Test cases
    fruits1 = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(fruits1))  # Expected: {'apple': 2, 'banana': 1, 'cherry': 1}

    fruits2 = []
    print(count_fruits(fruits2))  # Expected: {}

    try:
        fruits3 = ["apple", 123, "banana"]
        print(count_fruits(fruits3))
    except ValueError as e:
        print(e)  # Expected error message
```

This implementation:
1. Returns an empty dictionary for empty input lists
2. Raises a ValueError if any item isn't a string
3. Uses dictionary comprehension with `get()` method to count occurrences efficiently
4. Includes example usage demonstrating all cases

The function is also properly documented with docstring explaining its purpose, arguments, return value, and possible exceptions.

234 t/s, 399 tokens, 2s, 6%
