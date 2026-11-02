# Qwen2.5 Coder 1.5B Instruct
Model: qwen2.5-coder-1.5b-instruct
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list):
    # Error handling for empty list
    if not fruit_list:
        return {}
    
    # Error handling for non-string items
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")
    
    # Counting fruits
    fruit_count = {}
    for fruit in fruit_list:
        if fruit in fruit_count:
            fruit_count[fruit] += 1
        else:
            fruit_count[fruit] = 1
    
    return fruit_count

# Example usage
fruits = ["apple", "banana", "apple", "cherry"]
print(count_fruits(fruits))  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}
```

This function first checks if the input list is empty. If it is, it returns an empty dictionary. Then it iterates over each item in the list to ensure all items are strings. After that, it counts the occurrences of each fruit and stores them in a dictionary. Finally, it prints the resulting dictionary.

331 t/s, 236 tokens, 1s, 4%
