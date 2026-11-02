# Gemma 4 12B QAT
Model: google/gemma-4-12b-qat
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here is the clean Python solution using a standard dictionary approach.

```python
def count_fruit_occurrences(fruit_list):
    """
    Takes a list of strings and returns a dictionary with counts of each unique string.
    
    Args:
        fruit_list (list): A list of strings.
        
    Returns:
        dict: A dictionary mapping strings to their frequency.
        
    Raises:
        ValueError: If an item in the list is not a string.
    """
    # Error handling for empty list
    if not fruit_list:
        return {}

    fruit_counts = {}
    
    for item in fruit_list:
        # Error handling for non-string items
        if not isinstance(item, str):
            raise ValueError(f"All items in the list must be strings. Found: {type(item).__name__} ('{item}')")
        
        # Logic to populate the dictionary
        if item in fruit_counts:
            fruit_counts[item] += 1
        else:
            fruit_counts[item] = 1
            
    return fruit_counts

# --- Example Usage ---

# Case 1: Standard valid input
fruits = ["apple", "banana", "apple", "cherry", "banana", "apple"]
try:
    result = count_fruit_occurrences(fruits)
    print(f"Input: {fruits}")
    print(f"Result: {result}")
except ValueError as e:
    print(f"Error: {e}")

print("-" * 30)

# Case 2: Empty list
empty_fruits = []
result_empty = count_fruit_occurrences(empty_fruits)
print(f"Input: {empty_fruits}")
print(f"Result: {result_empty}")

print("-" * 30)

# Case 3: Error handling (non-string item)
bad_fruits = ["apple", 123, "banana"]
try:
    print(f"Input: {bad_fruits}")
    count_fruit_occurrences(bad_fruits)
except ValueError as e:
    print(f"Caught expected error: {e}")
```

### Key Features of this implementation:
1.  **Time Complexity**: $O(n)$, where $n$ is the number of items in the list (we iterate through the list once).
2.  **Space Complexity**: $O(k)$, where $k$ is the number of unique strings stored in the dictionary.
3.  **Type Safety**: It explicitly checks `isinstance(item, str)` to ensure the data matches the requirements before processing.
4.  **Readability**: It uses a standard `if/else` block for dictionary counting, which is highly readable for beginners, though it could also be achieved using `collections.Counter`.

95 t/s, 633 tokens, 7s, 5%
