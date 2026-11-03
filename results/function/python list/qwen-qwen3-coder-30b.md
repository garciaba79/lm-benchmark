# Qwen3 Coder 30B
Model: qwen/qwen3-coder-30b
Test: Function Python List
Created: 11/03/2026, 02:52:37 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list):
    """
    Count occurrences of each fruit in a list.
    
    Args:
        fruit_list (list): List of strings representing fruits
        
    Returns:
        dict: Dictionary with fruit names as keys and counts as values
        
    Raises:
        ValueError: If any item in the list is not a string
    """
    # Handle empty list
    if not fruit_list:
        return {}
    
    # Check that all items are strings
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings, got {type(item).__name__}: {item}")
    
    # Count fruits
    fruit_count = {}
    for fruit in fruit_list:
        fruit_count[fruit] = fruit_count.get(fruit, 0) + 1
    
    return fruit_count

# Example usage
if __name__ == "__main__":
    # Test with normal case
    fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(fruits)
    print(f"Input: {fruits}")
    print(f"Output: {result}")
    print()
    
    # Test with empty list
    empty_list = []
    result_empty = count_fruits(empty_list)
    print(f"Empty list input: {empty_list}")
    print(f"Output: {result_empty}")
    print()
    
    # Test error handling
    try:
        invalid_list = ["apple", "banana", 123, "cherry"]
        count_fruits(invalid_list)
    except ValueError as e:
        print(f"Error caught: {e}")
```

This function:
1. Takes a list of strings and returns a dictionary with fruit counts
2. Handles empty lists by returning an empty dictionary
3. Validates that all items are strings, raising a clear ValueError if not
4. Uses `dict.get()` for clean counting logic
5. Includes comprehensive docstring and example usage with print statements

The output will be:
```
Input: ['apple', 'banana', 'apple', 'cherry']
Output: {'apple': 2, 'banana': 1, 'cherry': 1}

Empty list input: []
Output: {}

Error caught: All items must be strings, got int: 123
```

62 t/s, 488 tokens, 8s
