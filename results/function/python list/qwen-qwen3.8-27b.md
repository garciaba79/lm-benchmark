# Qwen3.8 27B
Model: qwen/qwen3.8-27b
Test: Function Python List
Created: 11/03/2026, 01:42:33 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list: list) -> dict:
    """
    Count occurrences of each unique fruit in a list of strings.
    
    Args:
        fruit_list: A list of strings representing fruits.
        
    Returns:
        A dictionary with each unique fruit as key and its count as value.
        
    Raises:
        ValueError: If the list is empty or contains non-string items.
    """
    if not fruit_list:
        return {}
    
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings, but found {type(item).__name__}: {item!r}")
    
    counts = {}
    for fruit in fruit_list:
        if fruit in counts:
            counts[fruit] += 1
        else:
            counts[fruit] = 1
    
    return counts


# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(fruits)
    print("Input:", fruits)
    print("Result:", result)
    
    # Test with empty list
    empty_result = count_fruits([])
    print("\nEmpty list input: []")
    print("Result:", empty_result)
    
    # Test with non-string item
    try:
        count_fruits(["apple", 123, "banana"])
    except ValueError as e:
        print(f"\nError caught: {e}")
```

22 t/s, 342 tokens, 16s
