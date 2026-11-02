# LFM2.5 1.2B Instruct
Model: lfm2.5-1.2b-instruct
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean and well-structured Python function that meets your requirements:

### ✅ Function Requirements:
1. Accepts a list of strings.
2. Returns a dictionary counting occurrences of each unique string (fruit).
3. Validates that all items in the list are strings.
4. Handles empty input by returning an empty dictionary.
5. Raises a `ValueError` if any item is not a string.

---

### ✅ Python Code:

```python
def count_fruits(fruit_list):
    # Check for empty list
    if not fruit_list:
        return {}

    # Validate each item in the list
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")

    # Initialize dictionary with all unique fruits as keys and count 0
    counts = {}
    for fruit in fruit_list:
        counts[fruit] = counts.get(fruit, 0) + 1

    return counts
```

---

### ✅ Example Usage:

```python
# Example list of fruits
fruits = ["apple", "banana", "apple", "cherry"]

# Call the function and print result
result = count_fruits(fruits)
print(result)  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

# Example with empty list
empty_result = count_fruits([])
print(empty_result)  # Output: {}

# Example with non-string item
try:
    invalid_list = ["apple", 123, "banana"]
    count_fruits(invalid_list)
except ValueError as e:
    print(e)  # Output: All items in the list must be strings.
```

---

Let me know if you'd like this function to also remove duplicates or handle case-insensitivity (e.g., treat "Apple" and "apple" as the same).

576 t/s, 424 tokens, 1s, 3%
