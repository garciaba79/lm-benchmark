# Microsoft Phi 4 Mini Instruct
Model: microsoft_phi-4-mini-instruct
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Certainly! Below you will find clean Python code that achieves what you've described:

```python
def count_fruits(fruit_list):
    # Check for empty list at first to handle this specific case efficiently.
    if not fruit_list:
        return {}
    
    counts = {}  # Initialize an empty dictionary.

    for item in fruit_list:  
        try:
            assert isinstance(item, str), f"Item {item} is not a string."
            
            counts[item] = counts.get(item, 0) + 1
        except AssertionError as e:
            raise ValueError(e)
    
    return counts

# Example usage with print statements.
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    try:
        result = count_fruits(fruits) 
        print(result)  # Expected output: {'apple': 2, 'banana': 1, 'cherry': 1}
    
    except ValueError as e:
        print(e)
```

This function `count_fruits` takes a list of strings and returns the counts in dictionary format. If any item is not string it raises an exception with helpful message due to assertion error inside try-except block.

If you want more elaborate handling for non-string items (e.g., if there are other types like integers, lists), please let me know!

209 t/s, 285 tokens, 1s, 2%
