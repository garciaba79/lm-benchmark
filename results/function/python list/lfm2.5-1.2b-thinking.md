# LFM2.5 1.2B Thinking
Model: lfm2.5-1.2b-thinking
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean and structured Python implementation that fulfills the requirements:

---

### ✅ Function Definition

```python
def count_unique_fruits(items):
    if not items:
        return {}  # Return empty dict for empty input
    
    for item in items:
        if not isinstance(item, str):
            raise ValueError("All elements in the list must be strings")
    
    counts = {}
    for fruit in items:
        counts[fruit] = counts.get(fruit, 0) + 1
    
    return counts
```

---

### 📌 Example Usage

```python
# Example usage with valid input
result = count_unique_fruits(["apple", "banana", "apple", "cherry"])
print(result)  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

# Example usage with empty list
print(count_unique_fruits([]))  # Output: {}

# Example usage with invalid input (non-string element)
try:
    count_unique_fruits([1, "apple", "banana"])
except ValueError as e:
    print(e)  # Output: All elements must be strings
```

---

### 🔍 Explanation

- **Empty List Handling**: The function immediately returns an empty dictionary if the input list is empty.
- **Type Checking**: It iterates through each element to ensure they are all of type `str`. If not, a `ValueError` is raised with a clear message.
- **Counting Logic**: Uses a dictionary comprehension-like structure to count occurrences efficiently and clearly.

---

### 📝 Summary

This function ensures robustness against invalid inputs and provides clear feedback when such inputs are present, while also delivering the desired counting functionality in an easy-to-read format.

579 t/s, 1428 tokens, 3s, 9%
