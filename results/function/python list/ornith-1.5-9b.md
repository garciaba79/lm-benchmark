# Ornith 1.5 9B
Model: ornith-1.5-9b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean implementation:

```python
from collections import Counter


def count_fruits(fruits):
    """Count occurrences of each unique fruit in the list.

    Args:
        fruits: A list of strings representing fruit names.

    Returns:
        A dictionary mapping each unique fruit to its count.

    Raises:
        ValueError: If the input is not a list, or if any item is not a string.
    """
    if not isinstance(fruits, list):
        raise ValueError("Input must be a list of strings.")

    for item in fruits:
        if not isinstance(item, str):
            raise ValueError(
                f"All items must be strings, but got {type(item).__name__}: {item!r}"
            )

    return dict(Counter(fruits))


# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    counts = count_fruits(fruits)
    print("Fruit counts:", counts)  # {'apple': 2, 'banana': 1, 'cherry': 1}

    # Empty list returns an empty dict
    empty_counts = count_fruits([])
    print("Empty list ->", empty_counts)  # {}

    # Demonstrating error handling for a non-string item
    try:
        count_fruits(["apple", 42, "banana"])
    except ValueError as e:
        print(f"ValueError raised: {e}")  # All items must be strings...
```

**Key design choices:**

- **`Counter` + `dict()`**: `collections.Counter` is the idiomatic tool for counting hashable items. Wrapping it in `dict()` gives you a plain dictionary with insertion-order preserved (Python 3.7+).
- **Validate before counting**: The type check runs *before* building the counter, so a bad item raises an error instead of being silently counted as its own key.
- **Empty list → `{}`**: `Counter([])` produces an empty counter, and `dict()` of that is simply `{}`, satisfying your requirement naturally.

You can drop the explicit type check on `fruits` itself if you're confident callers always pass a list — but keeping it makes the function more robust against misuse like passing a tuple or generator.

148 t/s, 1194 tokens, 8s, 8%
