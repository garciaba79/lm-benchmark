# Phi 4
Model: microsoft/phi-4
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a Python function that accomplishes the task described:

```python
def count_fruits(fruit_list):
    """
    Takes a list of strings representing fruits and returns a dictionary 
    with each unique fruit as key and its count as value.

    Args:
        fruit_list (list): A list of strings where each string represents a fruit.

    Returns:
        dict: A dictionary with fruits as keys and their counts as values.

    Raises:
        ValueError: If any item in the list is not a string.
    """
    
    if not isinstance(fruit_list, list):
        raise ValueError("Input should be a list of strings.")
        
    fruit_count = {}
    
    for fruit in fruit_list:
        if not isinstance(fruit, str):
            raise ValueError("All items in the list must be strings.")
            
        if fruit in fruit_count:
            fruit_count[fruit] += 1
        else:
            fruit_count[fruit] = 1
    
    return fruit_count

# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    
    try:
        result = count_fruits(fruits)
        print("Fruit counts:", result)
        
        # Test with an empty list
        empty_result = count_fruits([])
        print("Empty list result:", empty_result)

        # Test with a non-string in the list
        mixed_list = ["apple", 123, "banana"]
        try:
            mixed_result = count_fruits(mixed_list)
        except ValueError as e:
            print("Error:", e)
            
    except ValueError as e:
        print("Error:", e)
```

### Explanation:

- **Function Definition**: The function `count_fruits` takes a list of strings and returns a dictionary with each fruit's count.
  
- **Type Checking**:
  - It first checks if the input is indeed a list, raising a `ValueError` if it's not.
  - It then iterates through each item in the list, checking whether each item is a string. If an element is found that is not a string, it raises a `ValueError`.

- **Counting Logic**: The function uses a dictionary to keep track of counts for each fruit.

- **Example Usage**:
  - Demonstrates normal usage with a sample list.
  - Shows handling for an empty list which should return an empty dictionary.
  - Attempts processing a mixed list containing a non-string, triggering error handling.

82 t/s, 516 tokens, 6s, 4%
