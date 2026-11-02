# LFM2.5 24B A2B
Model: lfm2.5-24b-a2b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here’s a compact, well‑documented implementation with the required error handling and a short demo.

```python
from typing import List, Dict


def count_fruit_counts(fruits: List[str]) -> Dict[str, int]:
    """
    Count occurrences of each unique fruit name in the list.

    Parameters
    ----------
    fruits : List[str]
        A list where every element should be a string (e.g., fruit names).

    Returns
    -------
    Dict[str, int]
        Mapping from fruit → how many times it appears.
        An empty list yields an empty dictionary.

    Raises
    ------
    ValueError
        If any item in the list is not a string.
    """
    # Empty input → early exit
    if not fruits:
        return {}

    # Ensure every element is a string; raise a clear error otherwise
    for idx, item in enumerate(fruits):
        if not isinstance(item, str):
            raise ValueError(
                f"Non‑string element found at index {idx}: "
                f"{repr(item)} (type: {type(item).__name__})."
            )

    # Simple manual counting (you could also use collections.Counter)
    counts = {}
    for fruit in fruits:
        counts[fruit] = counts.get(fruit, 0) + 1

    return counts


# ----------------------------------------------------------------------
# Example usage
if __name__ == "__main__":
    # Normal case
    sample = ["apple", "banana", "apple", "cherry"]
    result = count_fruit_counts(sample)
    print("Fruit counts:", result)          # {'apple': 2, 'banana': 1, 'cherry': 1}

    # Edge‑case: empty list
    empty_res = count_fruit_counts([])
    print("Empty input →", empty_res)       # {}

    # Demonstrating the error handling for a non‑string element
    try:
        bad_list = ["pear", 42, "grape"]
        count_fruit_counts(bad_list)
    except ValueError as e:
        print("Caught expected error:", e)
```

**What happens**

* `count_fruit_counts(["apple","banana","apple","cherry"])` returns  
  `{'apple': 2, 'banana': 1, 'cherry': 1}`.
* An empty list yields an empty dictionary.
* If the list contains a non‑string (e.g., `42`), a `ValueError` is raised with a descriptive message.  

The example block prints each scenario so you can see the behavior directly.

110 t/s, 2130 tokens, 20s, 14%
