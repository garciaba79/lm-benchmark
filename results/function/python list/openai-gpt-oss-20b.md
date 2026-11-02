# GPT-OSS 20B
Model: openai/gpt-oss-20b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
from collections import Counter
from typing import List, Dict

def count_fruits(fruit_list: List[str]) -> Dict[str, int]:
    """
    Count how many times each fruit appears in *fruit_list*.

    Parameters
    ----------
    fruit_list : list of str
        The list containing fruit names.  Items that are not strings will cause a ValueError.

    Returns
    -------
    dict
        A dictionary where the keys are the unique fruit names and the values are the counts.
        If *fruit_list* is empty, an empty dictionary is returned.

    Raises
    ------
    ValueError
        If any element in *fruit_list* is not a string.
    """
    # Return early for an empty list – no error handling needed here.
    if not fruit_list:
        return {}

    # Validate that every item is a string.
    for idx, item in enumerate(fruit_list):
        if not isinstance(item, str):
            raise ValueError(
                f"Element at index {idx} is not a string: {repr(item)}"
            )

    # Use Counter (a subclass of dict) to count the items.
    return dict(Counter(fruit_list))


# --------------------------------------------------------------------------- #
# Example usage
if __name__ == "__main__":
    sample = ["apple", "banana", "apple", "cherry"]
    print("Input list:", sample)
    result = count_fruits(sample)
    print("Fruit counts:", result)

    # Demonstrate the empty‑list case
    print("\nEmpty list test:")
    print(count_fruits([]))  # should print {}

    # Demonstrate error handling
    print("\nError handling test (should raise ValueError):")
    try:
        count_fruits(["apple", 42, "banana"])
    except ValueError as e:
        print("Caught exception:", e)
```

### Output

```
Input list: ['apple', 'banana', 'apple', 'cherry']
Fruit counts: {'apple': 2, 'banana': 1, 'cherry': 1}

Empty list test:
{}

Error handling test (should raise ValueError):
Caught exception: Element at index 1 is not a string: 42
```

The function `count_fruits` performs the required counting while guarding against non‑string items and gracefully handling an empty input.

134 t/s, 507 tokens, 4s, 4%
