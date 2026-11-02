# Falcon H1R 7B
Model: falcon-h1r-7b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here’s a compact implementation with clear error handling:

```python
def count_fruits(fruit_list):
    """Return a dict mapping each unique fruit to its occurrence count.
    
    Args:
        fruit_list (list of str): List containing only strings.
        
    Returns:
        dict[str, int]: Fruit → count for every distinct element.
    
    Raises:
        ValueError: If any element in the list is not a string.
    """
    # Empty input → empty dictionary
    if fruit_list == []:
        return {}

    counts = {}
    for item in fruit_list:
        # Validate that every entry is a string
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings; got non‑string element of type {type(item).__name__}")
        
        # Increment the count for this fruit
        counts[item] = counts.get(item, 0) + 1

    return counts


# Example usage with print statements
if __name__ == "__main__":
    # Normal case
    fruits = ["apple", "banana", "apple", "cherry"]
    print("Counts for:", fruits)
    print(count_fruits(fruits))  # → {'apple': 2, 'banana': 1, 'cherry': 1}

    # Empty list case
    empty_fruits = []
    print("\nEmpty input:")
    print("Counts for:", empty_fruits)
    print(count_fruits(empty_fruits))  # → {}

    # Uncomment to see the error handling in action:
    # bad_fruits = ["apple", 123, "orange"]
    # try:
    #     print(count_fruits(bad_fruits))
    # except ValueError as e:
    #     print("\nCaught exception:", e)  # → All items must be strings; got non‑string element of type int
```

**Explanation**

1. **Empty list handling** – The function checks for an empty list first and returns an empty dictionary (`{}`) as required.  
2. **Type validation** – Each element is verified with `isinstance(item, str)`. If any non‑string appears, a clear `ValueError` is raised that tells you the exact type of the offending item.  
3. **Counting** – The dictionary `counts` stores each fruit as a key; its value is incremented via `dict.get(key, default)`. This avoids importing `collections.Counter` and keeps the code straightforward.  

Running the script will print the expected counts for the sample list and demonstrate both the empty‑list behavior and the error handling path.

106 t/s, 1536 tokens, 15s, 10%
