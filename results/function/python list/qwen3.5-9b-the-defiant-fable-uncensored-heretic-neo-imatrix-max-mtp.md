# Qwen3.5 9B The Defiant Fable Uncnr Heretic NEO MAX
Model: qwen3.5-9b-the-defiant-fable-uncensored-heretic-neo-imatrix-max-mtp
Test: Function Python List
Created: 11/22/2026, 02:51:01 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list):
    """
    Count occurrences of each fruit in the list.

    Args:
        fruit_list (list[str]): List of fruit names.

    Returns:
        dict[str, int]: Dictionary mapping each unique fruit to its count.

    Raises:
        ValueError: If any item is not a string.
    """
    if not isinstance(fruit_list, list):
        raise TypeError("Input must be a list.")

    counts = {}
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(
                f"All items must be strings. Found type {type(item).__name__} "
                f"for value '{item}'.",
            )
        counts[item] = counts.get(item, 0) + 1

    return counts


# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(fruits)
    print("Fruit counts:", result)

    # Edge case: empty list
    empty_result = count_fruits([])
    print("Empty list result:", empty_result)

    # Error handling example (uncomment to test):
    # try:
    #     bad_input = ["apple", 123, "banana"]
    #     count_fruits(bad_input)
    # except ValueError as e:
    #     print("Caught error:", e)
```

100 t/s, 330 tokens, 3s, 3%
