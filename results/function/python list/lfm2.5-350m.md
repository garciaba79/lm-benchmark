# LFM2.5 350M
Model: lfm2.5-350m
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's a clean Python function that fulfills your requirements:

```
def count_fruits(fruit_list):
    """
    Counts the occurrences of each unique fruit in the list.
    
    Args:
        fruit_list (list): A list of strings representing fruits.
        
    Returns:
        dict: A dictionary where keys are fruits and values are their counts.
    
    Raises:
        ValueError: If the input list is empty or contains non-string elements.
    """
    if not fruit_list:
        return {}
    
    fruit_counts = {}
    for fruit in fruit_list:
        if not isinstance(fruit, str):
            raise ValueError("All items in the list must be strings.")
        fruit_counts[fruit] = fruit_counts.get(fruit, 0) + 1
    
    return fruit_counts

# Example usage:
if __name__ == "__main__":
    print(count_fruits(["apple", "banana", "apple", "cherry"])))
    # Output: {'apple': 2, 'banana': 1, 'cherry': 1}
```

This function first checks if the input list is empty. If so, it returns an empty dictionary. Then, it iterates through each fruit in the list and updates its count in the dictionary. Any non-string items raise a `ValueError`. Finally, it prints the resulting dictionary using example usage.

830 t/s, 299 tokens, 0s, 3%
