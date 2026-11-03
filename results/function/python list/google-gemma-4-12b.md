# Gemma 4 12B
Model: google/gemma-4-12b
Test: Function Python List
Created: 11/03/2026, 12:56:40 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here is the clean Python solution using a standard dictionary approach (or `collections.Counter` logic) along with the requested error handling and examples.

```python
def count_fruit_occurrences(fruit_list):
    """
    Takes a list of strings and returns a dictionary containing 
    the count of each unique string.
    """
    # Check if the list is empty
    if not fruit_list:
        return {}

    counts = {}
    
    for item in fruit_list:
        # Error handling for non-string items
        if not isinstance(item, str):
            raise ValueError(f"Invalid input: Expected a string, but found {type(item).__name__} ('{item}').")
        
        # Increment the count in the dictionary
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
            
    return counts

# --- Example Usage ---

# Case 1: Standard list
fruits = ["apple", "banana", "apple", "cherry"]
try:
    result = count_fruit_occurrences(fruits)
    print(f"Input: {fruits}")
    print(f"Result: {result}\n")
except ValueError as e:
    print(f"Error: {e}")

# Case 2: Empty list
empty_list = []
result_empty = count_fruit_occurrences(empty_list)
print(f"Input: {empty_list}")
print(f"Result: {result_empty}\n")

# Case 3: Invalid input (non-string)
mixed_list = ["apple", "banana", 10] # 10 is an integer
print(f"Input: {mixed_list}")
try:
    count_fruit_occurrences(mixed_list)
except ValueError as e:
    print(f"Caught Expected Error: {e}")
```

### Explanation of the Code:
1.  **Empty List Check**: The function immediately checks `if not fruit_list`. In Python, an empty list evaluates to `False`, so this handles the requirement to return `{}` if no items are provided.
2.  **Type Validation**: Inside the loop, `isinstance(item, str)` ensures that every element is a string before processing. If it encounters an integer, float, or other type, it raises a `ValueError` with a descriptive message.
3.  **Counting Logic**: We iterate through the list once (O(n) complexity). We use the dictionary to store keys as fruits and values as their respective counts. 
4.  **Error Handling in Usage**: I wrapped the "invalid input" example in a `try-except` block to demonstrate how you can catch and handle the specific error raised by the function.

82 t/s, 619 tokens, 8s
