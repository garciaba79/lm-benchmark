# LFM2.5 230M
Model: lfm2.5-230m
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list):
    """
    Counts the number of each unique fruit in the list.
    
    Args:
        fruit_list (list): A list of strings representing fruits.
        
    Returns:
        dict: A dictionary with unique fruits as keys and their counts as values.
    """
    if not fruit_list:
        return {}
    
    fruit_count = {}
    for fruit in fruit_list:
        if type(fruit) != str:
            raise ValueError("All items must be strings")
        fruit_count[fruit] = fruit_count.get(fruit, 0) + 1
    
    return fruit_count

# Example usage:
print(count_fruits(["apple", "banana", "apple", "cherry"]))
```

This function checks if the input list is empty and returns an empty dictionary if so. It also raises a `ValueError` with a clear message if any item in the list is not a string. The example usage demonstrates how to call the function and print the result.

1019 t/s, 218 tokens, 0s, 2%
