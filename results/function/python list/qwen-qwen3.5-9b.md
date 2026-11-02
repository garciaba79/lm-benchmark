# Qwen3.5 9B
Model: qwen/qwen3.5-9b
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
    Count occurrences of each unique fruit in a list of strings.

    Parameters:
        fruit_list (list of str): A list containing fruit names as strings.

    Returns:
        dict: A dictionary with fruits as keys and their counts as values.

    Raises:
        ValueError: If any item in the list is not a string.
        ValueError: If the list is empty, an empty dictionary will be returned instead (per requirement).
    """
    if not fruit_list:
        return {}

    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(f"Invalid input: {repr(item)} is not a string.")

    counts = {}
    for fruit in fruit_list:
        counts[fruit] = counts.get(fruit, 0) + 1

    return counts


# Example usage
if __name__ == "__main__":
    fruits1 = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(fruits1))
    # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

    fruits2 = []
    print(count_fruits(fruits2))
    # Output: {}

    fruits3 = ["apple", "banana", 1, "cherry"]
    try:
        count_fruits(fruits3)
    except ValueError as e:
        print(f"Error: {e}")
    # Output: Error: Invalid input: 1 is not a string.
```

122 t/s, 446 tokens, 4s, 3%
