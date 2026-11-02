# Lfm2 24B A2B
Model: liquid/lfm2-24b-a2b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```
def count_fruits(fruit_list):
    """
    Returns a dictionary with each unique fruit as key and its count as value.

    Args:
        fruit_list (list): A list of strings representing fruits.

    Returns:
        dict: A dictionary with fruit counts.

    Raises:
        ValueError: If the input list is empty or contains non-string items.
    """
    if not fruit_list:
        return {}

    if not all(isinstance(fruit, str) for fruit in fruit_list):
        raise ValueError("Input list must only contain strings.")

    fruit_counts = {}
    for fruit in fruit_list:
        fruit_counts[fruit] = fruit_counts.get(fruit, 0) + 1

    return fruit_counts


# Example usage
fruits = ["apple", "banana", "apple", "cherry"]
try:
    result = count_fruits(fruits)
    print(result)  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}
except ValueError as e:
    print(e)

# Test with empty list
empty_list = []
print(count_fruits(empty_list))  # Output: {}

# Test with non-string item
mixed_list = ["apple", "banana", 123, "cherry"]
try:
    count_fruits(mixed_list)
except ValueError as e:
    print(e)  # Output: Input list must only contain strings.
```

109 t/s, 325 tokens, 4s, 3%
