# Qwen Qwen3 14B
Model: qwen_qwen3-14b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean and well-documented Python function that fulfills all the requirements:

---

### ✅ **Function Description**

The `count_fruits` function takes a list of strings and returns a dictionary where each unique string (fruit) is a key, and its count in the list is the value. It includes error handling for:
- Empty lists: return an empty dictionary.
- Non-string elements: raise a `ValueError`.

---

### 🧠 **Implementation**

```python
def count_fruits(fruit_list):
    """
    Count occurrences of each unique string in the given list.

    Parameters:
        fruit_list (list): A list of strings to be counted.

    Returns:
        dict: Dictionary with unique strings as keys and their counts as values.

    Raises:
        ValueError: If any element in the list is not a string.
    """
    if not fruit_list:
        return {}

    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")

    counts = {}
    for fruit in fruit_list:
        counts[fruit] = counts.get(fruit, 0) + 1

    return counts
```

---

### 📌 **Example Usage**

```python
# Example usage with print statements
if __name__ == "__main__":
    sample_data = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(sample_data))
    # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

    empty_list = []
    print(count_fruits(empty_list))
    # Output: {}

    try:
        invalid_list = ["apple", 123]
        count_fruits(invalid_list)
    except ValueError as e:
        print(e)
    # Output: All items in the list must be strings.
```

---

### 📝 **Notes**

- The function assumes that the input is a list. If it's not (e.g., a string or integer), it may raise an error during iteration, but this case is not explicitly handled as per the problem statement.
- This implementation uses basic Python dictionary operations for clarity and avoids external libraries like `collections.Counter`.

10 t/s, 3722 tokens, 385s, 47%
