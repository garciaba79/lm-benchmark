# Qwen3 14B
Model: qwen/qwen3-14b
Test: Function Python List
Created: 11/03/2026, 01:06:07 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean and well-documented Python function that fulfills your requirements:

```python
def count_fruits(fruit_list):
    """
    Counts occurrences of each unique fruit in a list.

    Args:
        fruit_list (list): A list of strings representing fruits.

    Returns:
        dict: A dictionary with unique fruits as keys and their counts as values.

    Raises:
        ValueError: If any element in the list is not a string.
    """
    if not isinstance(fruit_list, list):
        raise TypeError("Input must be a list.")

    if not fruit_list:
        return {}

    fruit_count = {}
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")
        fruit_count[item] = fruit_count.get(item, 0) + 1

    return fruit_count


# Example usage
if __name__ == "__main__":
    sample_fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(sample_fruits)
    print("Fruit counts:", result)

    empty_list = []
    print("Empty list result:", count_fruits(empty_list))

    try:
        invalid_list = ["apple", 123, "cherry"]
        count_fruits(invalid_list)
    except ValueError as e:
        print("Error:", e)
```

### Output Example
When running the above code:

```text
Fruit counts: {'apple': 2, 'banana': 1, 'cherry': 1}
Empty list result: {}
Error: All items in the list must be strings.
```

This implementation ensures:
- Proper handling of empty lists (returns an empty dict).
- Ensures all items are strings and raises a `ValueError` otherwise.
- Uses dictionary’s `.get()` method for clean counting.

80 t/s, 387 tokens, 5s
