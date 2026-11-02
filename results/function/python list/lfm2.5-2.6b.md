# LFM2.5 2.6B
Model: lfm2.5-2.6b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here’s a compact, well‑documented solution:

```python
def count_fruits(fruits):
    """
    Count how many times each fruit appears in the given list.

    Parameters
    ----------
    fruits : list[str]
        A list containing only string elements (e.g., ["apple", "banana"]).

    Returns
    -------
    dict[str, int]
        A dictionary where keys are the distinct fruits and values are their counts.
    
    Raises
    ------
    ValueError
        If any element of ``fruits`` is not a string or if ``fruits`` is empty
        (the function returns an empty dict for an empty list).
    """
    # Empty input → empty dictionary
    if not fruits:
        return {}

    result = {}
    for item in fruits:
        # Ensure every element is a string; raise a clear error otherwise.
        if not isinstance(item, str):
            raise ValueError("All items must be strings")
        # Increment the count for this fruit
        result[item] = result.get(item, 0) + 1

    return result


# --------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    # Normal case
    fruits = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(fruits))   # → {'apple': 2, 'banana': 1, 'cherry': 1}

    # Empty list – should return an empty dict
    print(count_fruits([]))       # → {}

    # Invalid input – will raise a ValueError
    try:
        bad_fruit = ["apple", 3, "banana"]
        count_fruits(bad_fruit)
    except ValueError as e:
        print(f"Error: {e}")      # → Error: All items must be strings
```

**Explanation**

1. **Empty list handling** – If `fruits` is empty we immediately return `{}`.
2. **Type checking** – Before counting, each element is verified with `isinstance(item, str)`.  
   If any item isn’t a string, a `ValueError` is raised with a descriptive message.
3. **Counting** – We build the dictionary by incrementing the count for each fruit (using `dict.get` to start at 0 on first occurrence).
4. **Example usage** – The script prints the result for a normal list, shows that an empty list yields `{}`, and demonstrates the error when a non‑string is present.

288 t/s, 1198 tokens, 4s, 8%
