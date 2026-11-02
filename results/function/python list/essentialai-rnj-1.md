# Rnj 1
Model: essentialai/rnj-1
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
    # Check if the list is empty and return empty dictionary.
    if not fruit_list:
        return {}
    
    # Initialize an empty dictionary for counting fruits.
    fruit_count = {}
    
    # Iterate through the list to count occurrences of each fruit.
    for item in fruit_list:
        # Check if the item is a string, otherwise raise ValueError.
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings. Found non-string item: {item}")
        
        # If the fruit is already in the dictionary, increment its count.
        if item in fruit_count:
            fruit_count[item] += 1
        # Otherwise, add the fruit to the dictionary with a count of 1.
        else:
            fruit_count[item] = 1
            
    return fruit_count

# Example usage and print statements showing the result
try:
    example_list = ["apple", "banana", "apple", "cherry"]
    print("Fruit counts:", count_fruits(example_list))
    
    # Uncomment to test error handling
    # example_list.append(123)
    # print(count_fruits(example_list))  # This will raise ValueError
except ValueError as e:
    print(f"Error: {e}")
```

This code snippet defines the `count_fruits` function that counts the occurrences of each fruit in a list. It also includes error handling for cases where the provided list is empty or contains non-string items. The example usage demonstrates how to use the function and shows an example of how it handles errors with a commented-out line.

130 t/s, 333 tokens, 3s, 3%
