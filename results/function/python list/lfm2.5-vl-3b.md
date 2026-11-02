# LFM2.5 VL 3B
Model: lfm2.5-vl-3b
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
def count_fruits(fruit_list):
    """
    Return a dictionary mapping each unique fruit (as a string) to its
    total count in *fruit_list*.

    Parameters
    ----------
    fruit_list : list[str]
        A list of strings representing the fruits.

    Returns
    -------
    dict
        A dictionary with fruit names as keys and their counts as values.
        If the input list is empty, an empty dict is returned.

    Raises
    ------
    ValueError
        If any element in *fruit_list* is not a string.
    """
    # Guard against an empty input
    if not fruit_list:
        return {}

    # Validate that every item is a string
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(
                f"All items must be strings. Found non‑string: '{item}'"
            )

    counts = {}
    for fruit in fruit_list:
        counts[fruit] = fruit_list.count(fruit)

    return counts


# ----------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(fruits)
    print(result)          # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

    empty_list = []
    print(count_fruits(empty_list))   # Output: {}

    bad_input = ["apple", 123, "banana"]
    try:
        count_fruits(bad_input)
    except ValueError as e:
        print(e)               # Output: All items must be strings. Found non‑string: '123'
```

**Explanation**

1. **Empty list handling** – The function checks `if not fruit_list:` and returns an empty dictionary immediately.
2. **Type validation** – A simple loop (`for item in fruit_list`) verifies that every element is a string; if any fails, a `ValueError` with a clear message is raised.
3. **Counting** – For each unique fruit we call `fruit_list.count(fruit)` and store the result in a dictionary.
4. **Example usage** – Demonstrates normal operation, an empty list, and error handling.

290 t/s, 491 tokens, 2s, 4%
