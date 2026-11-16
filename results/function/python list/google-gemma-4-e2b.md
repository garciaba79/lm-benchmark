# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Function Python List
Created: 11/15/2026, 09:41:09 PM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here is the clean Python function incorporating the required logic and error handling, followed by the example usage.

```python
from typing import List, Dict

def count_string_occurrences(fruits: List[str]) -> Dict[str, int]:
    """
    Takes a list of strings and returns a dictionary with each unique string 
    as a key and its frequency (count) as the value.

    Args:
        fruits: A list of strings to count.

    Returns:
        A dictionary where keys are unique strings and values are their counts.

    Raises:
        ValueError: If any item in the input list is not a string.
    """
    # 1. Error Handling: Check if any item is not a string
    for fruit in fruits:
        if not isinstance(fruit, str):
            raise ValueError(f"Input list must contain only strings. Found non-string item: {fruit} (Type: {type(fruit).__name__})")

    # 2. Error Handling: Check if the list is empty
    if not fruits:
        return {}

    # 3. Core Logic: Count occurrences using a dictionary or collections.Counter
    fruit_counts = {}
    for fruit in fruits:
        # If the fruit is already a key, increment its count; otherwise, initialize it to 1
        fruit_counts[fruit] = fruit_counts.get(fruit, 0) + 1
        
    return fruit_counts

# --- Example Usage ---

print("--- Test Case 1: Standard List ---")
input_list_1 = ["apple", "banana", "apple", "cherry", "banana"]
try:
    result1 = count_string_occurrences(input_list_1)
    print(f"Input: {input_list_1}")
    print(f"Result: {result1}\n")
except ValueError as e:
    print(f"Error encountered: {e}\n")

print("--- Test Case 2: Empty List ---")
input_list_2 = []
try:
    result2 = count_string_occurrences(input_list_2)
    print(f"Input: {input_list_2}")
    print(f"Result: {result2}\n")
except ValueError as e:
    print(f"Error encountered: {e}\n")


print("--- Test Case 3: List with Mixed Types (Error Handling Test) ---")
input_list_3 = ["grape", "kiwi", 123, "mango"]
try:
    result3 = count_string_occurrences(input_list_3)
    print(f"Result: {result3}\n")
except ValueError as e:
    print(f"Successfully caught expected error:")
    print(f"Error: {e}\n")
```

190 t/s, 635 tokens, 3s
