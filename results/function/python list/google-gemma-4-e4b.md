# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Function Python List
Created: 11/03/2026, 12:33:42 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here is the clean, robust Python function that meets all your requirements.

```python
from typing import List, Dict, Any

def count_fruit_occurrences(fruits: List[Any]) -> Dict[str, int]:
    """
    Counts the occurrences of each unique string (fruit) in a list.

    Args:
        fruits: A list expected to contain only strings (fruit names).

    Returns:
        A dictionary where keys are the unique fruits and values are their counts.
        Returns an empty dictionary if the input list is empty.

    Raises:
        ValueError: If any item in the input list is not a string.
    """
    # 1. Handle empty list case
    if not fruits:
        return {}

    fruit_counts: Dict[str, int] = {}

    # 2. Iterate and perform type checking/counting
    for item in fruits:
        # Error Handling: Check if the item is a string
        if not isinstance(item, str):
            raise ValueError(
                f"Invalid input type found: Expected all elements to be strings, "
                f"but received element of type {type(item).__name__}."
            )
        
        # Core Logic: Counting
        fruit_counts[item] = fruit_counts.get(item, 0) + 1
    
    return fruit_counts

# --- Example Usage ---

print("--- Test Case 1: Normal operation ---")
fruit_list_1 = ["apple", "banana", "apple", "cherry"]
try:
    result_1 = count_fruit_occurrences(fruit_list_1)
    print(f"Input: {fruit_list_1}")
    print(f"Result: {result_1}")
except ValueError as e:
    print(f"Error caught: {e}")


print("\n--- Test Case 2: Empty list (Should return empty dict) ---")
fruit_list_2 = []
try:
    result_2 = count_fruit_occurrences(fruit_list_2)
    print(f"Input: {fruit_list_2}")
    print(f"Result: {result_2}")
except ValueError as e:
    print(f"Error caught: {e}")


print("\n--- Test Case 3: Invalid item type (Should raise ValueError) ---")
# This list contains an integer, which should trigger the error handling
fruit_list_3 = ["apple", "banana", 123, "cherry"]
try:
    result_3 = count_fruit_occurrences(fruit_list_3)
    print(f"Result (SHOULD NOT REACH): {result_3}") # This line won't print if error is raised correctly
except ValueError as e:
    print("Successfully caught expected error:")
    print(f"Error Message: {e}")

```

144 t/s, 641 tokens, 4s
