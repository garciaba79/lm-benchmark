# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's the clean Python function that meets the specified requirements:

```python
def count_fruits(fruits):
    if not fruits:
        return {}
    for item in fruits:
        if not isinstance(item, str):
            raise ValueError("All items must be strings")
    counts = {}
    for fruit in fruits:
        counts[fruit] = counts.get(fruit, 0) + 1
    return counts

# Example usage with print statements
print(count_fruits(["apple", "banana", "apple", "cherry"]))  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}
print(count_fruits([]))  # Output: {}
try:
    count_fruits([1, 2, 3])
except ValueError as e:
    print(e)  # Output: All items must be strings
```

This function first checks if the input list is empty and returns an empty dictionary if true. It then verifies that all elements in the list are strings, raising a `ValueError` with a clear message if any element is not a string. Finally, it counts the occurrences of each unique fruit and returns the result as a dictionary. The example usage demonstrates the function's behavior for both valid and invalid inputs.

214 t/s, 2151 tokens, 10s, 7%
