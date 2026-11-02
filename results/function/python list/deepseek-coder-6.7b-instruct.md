# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Here's how you can solve this problem in Python:

```python
def fruit_counter(fruit_list):
    if len(fruit_list) == 0:  # Check for empty list
        return {}  
    
    count_dict = {}
    for fruit in fruit_list:
        if not isinstance(fruit, str):  # Raise ValueError if item isn't a string
            raise ValueError("All items must be strings.")
        
        if fruit in count_dict.keys():  
            count_dict[fruit] += 1   
        else:
            count_dict[fruit] = 1     # Initialize the count for new fruits 
            
    return count_dict
```
Now, let's test this function with an example usage and print statements showing the result.

```python
# Testing fruit_counter()
print(fruit_counter(["apple", "banana", "apple", "cherry"]))  # Expected output: {'apple': 2, 'banana': 1, 'cherry': 1}
print(fruit_counter(['grape', 'pear', 'grape', 'melon']))   # Expected output: {'grape': 2, 'pear': 1, 'melon': 1}
try:
    print(fruit_counter([100, "banana", "apple"]))     # This should raise a ValueError
except Exception as e:
    print("Caught an exception: ", str(e))   # Expected output: Caught an exception:  All items must be strings.
print(fruit_counter([]))      # Testing with empty list, expected output {}
```
This function works by iterating over the input fruit_list and incrementing a count in the dictionary for each unique string it encounters. If any item is not a string, it raises an exception. It also handles the case where the input list might be empty. In such cases, it returns an empty dict.

158 t/s, 459 tokens, 3s, 4%
