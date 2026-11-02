# Nemotron 3 Nano 4B
Model: nvidia/nemotron-3-nano-4b
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
def count_fruits(fruits):
    """Return a dictionary mapping each unique fruit to its count."""
    if not fruits:                     # empty list → empty dict
        return {}

    counts = {}
    for item in fruits:
        if not isinstance(item, str):  # non‑string element → error
            raise ValueError("All items must be strings.")
        counts[item] = counts.get(item, 0) + 1
    return counts


# Example usage
if __name__ == "__main__":
    sample = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(sample))   # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

    empty = []
    print(count_fruits(empty))    # Output: {}
```

226 t/s, 424 tokens, 2s, 3%
