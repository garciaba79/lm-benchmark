# Qwen3.5 4B
Model: qwen3.5-4b
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
def count_fruits(fruit_list):
    """
    Count the occurrences of each unique fruit in a list.

    Args:
        fruit_list (list): A list of strings representing fruits.

    Returns:
        dict: Dictionary mapping each fruit to its occurrence count.

    Raises:
        ValueError: If any item in the list is not a string or if the input is None.
    """
    # Validate that input is not None and all items are strings
    if fruit_list is None:
        raise ValueError("Input cannot be None.")

    for i, item in enumerate(fruit_list):
        if not isinstance(item, str):
            raise ValueError(f"Item at index {i} is not a string. Expected 'str', got '{type(item).__name__}'.")

    # Handle empty list case
    if len(fruit_list) == 0:
        return {}

    # Count occurrences using dictionary comprehension
    fruit_counts = {}
    for fruit in fruit_list:
        fruit_counts[fruit] = fruit_counts.get(fruit, 0) + 1

    return fruit_counts


# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    print("Input list:", fruits)
    result = count_fruits(fruits)
    print("Fruit counts:", result)

    # Test with empty list
    print("\n--- Empty List Test ---")
    empty_list = []
    print("Input list:", empty_list)
    result_empty = count_fruits(empty_list)
    print("Fruit counts:", result_empty)

    # Test error handling - non-string item
    print("\n--- Error Handling Test ---")
    try:
        invalid_list = ["apple", 123, "banana"]
        print("Input list:", invalid_list)
        count_fruits(invalid_list)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test with None input
    print("\n--- None Input Test ---")
    try:
        result_none = count_fruits(None)
    except ValueError as e:
        print(f"Caught expected error for None input: {e}")
```

177 t/s, 577 tokens, 3s, 4%
