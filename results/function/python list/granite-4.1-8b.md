# Granite 4.1 8B
Model: granite-4.1-8b
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
    if not fruit_list:
        return {}

    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")

    fruit_count = {}
    for fruit in fruit_list:
        fruit_count[fruit] = fruit_count.get(fruit, 0) + 1

    return fruit_count
```

Explanation:
1. The function `count_fruits` takes a single parameter `fruit_list`, which is expected to be a list of strings.
2. It first checks if the list is empty using `if not fruit_list`. If it is empty, it returns an empty dictionary `{}`.
3. It then iterates over each item in the list using a `for` loop. For each item, it checks if it is an instance of `str` using `isinstance(item, str)`. If any item is not a string, it raises a `ValueError` with a clear message: "All items in the list must be strings."
4. After validating the input, it initializes an empty dictionary called `fruit_count`.
5. It iterates over each fruit in the `fruit_list` and updates the count in the `fruit_count` dictionary using the `get` method. If the fruit is not already a key in the dictionary, `get` returns a default value of 0, and the count is incremented by 1.
6. Finally, it returns the `fruit_count` dictionary containing the unique fruits as keys and their respective counts as values.

Example usage:

```python
try:
    fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(fruits)
    print(result)  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}
    
    empty_list = []
    result_empty = count_fruits(empty_list)
    print(result_empty)  # Output: {}
    
    invalid_item = ["apple", 123, "banana"]
    result_invalid = count_fruits(invalid_item)
except ValueError as e:
    print(f"Error: {e}")  # Output: Error: All items in the list must be strings.
```

In this example usage:
1. We define a list `fruits` with some sample fruit names and call `count_fruits(fruits)`. The output is printed, showing the dictionary with each unique fruit and its count.
2. We define an empty list `empty_list` and call `count_fruits(empty_list)`. The output is printed, showing an empty dictionary `{}`.
3. We define a list `invalid_item` that contains a non-string item (an integer). When we call `count_fruits(invalid_item)`, it raises a `ValueError`, which is caught in the `except` block, and the error message is printed.

This function provides clean error handling for empty lists and invalid input types while returning the expected dictionary of fruit counts.

127 t/s, 636 tokens, 5s, 5%
