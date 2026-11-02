# Mamba Codestral 7B v0.1
Model: mamba-codestral-7b-v0.1
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 32K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list):
    # Check for empty list
    if len(fruit_list) == 0:
        return {}

    fruit_dict = {}
    for fruit in fruit_list:
        # Check that all items are strings
        if not isinstance(fruit, str):
            raise ValueError("All items in the list must be strings.")

        # Count each unique fruit
        if fruit in fruit_dict:
            fruit_dict[fruit] += 1
        else:
            fruit_dict[fruit] = 1
    return fruit_dict
```
Example usage:
```python
print(count_fruits(["apple", "banana", "apple", "cherry"]))
# Output: {'apple': 2, 'banana': 1, 'cherry': 1}

try:
    print(count_fruits([1, "banana", "apple", "cherry"]))
except ValueError as e:
    print(e) # Output: All items in the list must be strings.
```

150 t/s, 258 tokens, 2s, 1%
