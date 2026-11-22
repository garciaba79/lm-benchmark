# Qwen3.6 35B A3B
Model: qwen/qwen3.6-35b-a3b
Test: Function Python List
Created: 11/22/2026, 03:13:14 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruits: list) -> dict:
    """
    Takes a list of strings and returns a dictionary with each unique string as key
    and its count as value.
    
    Raises:
        ValueError: If any item in the list is not a string.
    """
    if not fruits:
        return {}
    
    for item in fruits:
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings. Found: {type(item).__name__}")
    
    result = {}
    for fruit in fruits:
        if fruit in result:
            result[fruit] += 1
        else:
            result[fruit] = 1
    
    return result


# Example usage
if __name__ == "__main__":
    # Example 1: Normal case
    fruits = ["apple", "banana", "apple", "cherry"]
    print(f"Input: {fruits}")
    print(f"Output: {count_fruits(fruits)}")
    print()
    
    # Example 2: Empty list
    empty_fruits = []
    print(f"Input: {empty_fruits}")
    print(f"Output: {count_fruits(empty_fruits)}")
    print()
    
    # Example 3: Invalid input
    invalid_fruits = ["apple", 123, "banana"]
    print(f"Input: {invalid_fruits}")
    try:
        count_fruits(invalid_fruits)
    except ValueError as e:
        print(f"Error: {e}")
```

43 t/s, 351 tokens, 8s, 3%
