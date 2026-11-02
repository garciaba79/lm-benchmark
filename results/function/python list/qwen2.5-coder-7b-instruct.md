# Qwen2.5 Coder 7B Instruct
Model: qwen2.5-coder-7b-instruct
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's how you can solve this problem:

```python
def count_fruits(fruit_list):
    # Check if list is empty
    if len(fruit_list) == 0:
        return {}

    fruit_dict = {}
    
    for item in fruit_list:
        # Check if item is a string
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")
        
        # Count each unique fruit
        if item in fruit_dict:
            fruit_dict[item] += 1
        else:
            fruit_dict[item] = 1

    return fruit_dict


# Example usage
try:
    fruits = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(fruits))  # Output: {'apple': 2, 'banana': 1, 'cherry': 1}

    empty_list = []
    print(count_fruits(empty_list))  # Output: {}

    mixed_items = ["apple", "banana", 3]
    print(count_fruits(mixed_items))  
except ValueError as e:
    print(e)  # Output: All items in the list must be strings.
```

In this code, we first check if the input list is empty. If it is, we return an empty dictionary.

Then, for each item in the list, we check whether it's a string using `isinstance(item, str)`. If not, we raise a ValueError with a clear message.

If the item is indeed a string, we count its occurrences by adding them to our fruit_dict. If the fruit isn't already in the dictionary, we add it and set its value to 1; if it's already there, we increment its value by 1.

Finally, we return the resulting dictionary.

149 t/s, 369 tokens, 3s, 3%
