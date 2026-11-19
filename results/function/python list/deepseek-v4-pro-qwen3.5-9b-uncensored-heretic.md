# DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic
Model: deepseek-v4-pro-qwen3.5-9b-uncensored-heretic
Test: Function Python List
Created: 11/18/2026, 11:42:33 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean Python function that meets your requirements:

```python
def count_fruits(fruit_list):
 """
 Counts occurrences of each unique fruit in a list of strings.

 Args:
 fruit_list (list of str): List containing fruit names as strings.

 Returns:
 dict: Dictionary with fruits as keys and their counts as values.

 Raises:
 ValueError: If any item in the list is not a string.
 """
 # Validate input type
 if not isinstance(fruit_list, list):
 raise TypeError("Input must be a list of strings.")

 # Check each item for non-string types
 for item in fruit_list:
 if not isinstance(item, str):
 raise ValueError(f"Item '{item}' is not a string. All items must be strings.")

 # Count occurrences using dictionary comprehension or Counter
 from collections import defaultdict
 counts = defaultdict(int)
 for fruit in fruit_list:
 counts[fruit] += 1

 return dict(counts)


# Example usage
if __name__ == "__main__":
 fruits = ["apple", "banana", "apple", "cherry"]
 result = count_fruits(fruits)
 print("Fruit counts:", result)

 # Test with empty list
 empty_result = count_fruits([])
 print("Empty list result:", empty_result)

 # Test error handling (uncomment to see errors)
 # try:
 # count_fruits([1, "banana", 3])
 # except ValueError as e:
 # print(f"Caught expected error: {e}")
```

**Output:**
```
Fruit counts: {'apple': 2, 'banana': 1, 'cherry': 1}
Empty list result: {}
```

### Key features:
- **Validation**: Checks that input is a list and all items are strings.
- **Error handling**: Raises `ValueError` with clear messages for non-string items.
- **Efficiency**: Uses `defaultdict(int)` for clean counting logic.
- **Edge case**: Returns empty dict `{}` for an empty list (no error raised).

You can easily adapt this pattern to count any hashable items in a list by changing the validation condition.

131 t/s, 467 tokens, 4s
