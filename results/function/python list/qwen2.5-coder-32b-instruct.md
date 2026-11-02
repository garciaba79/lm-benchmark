# Qwen2.5 Coder 32B Instruct
Model: qwen2.5-coder-32b-instruct
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Certainly! Below is a Python function that meets your requirements:

```python
def count_fruits(fruit_list):
    # Check if the list is empty
    if not fruit_list:
        return {}
    
    fruit_count = {}
    
    for item in fruit_list:
        # Check if each item is a string
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")
        
        # Count the occurrence of each fruit
        if item in fruit_count:
            fruit_count[item] += 1
        else:
            fruit_count[item] = 1
    
    return fruit_count

# Example usage
try:
    fruits = ["apple", "banana", "apple", "cherry"]
    result = count_fruits(fruits)
    print("Fruit Count:", result)

    # Uncomment the lines below to test error handling
    # empty_list = []
    # print("Empty List Result:", count_fruits(empty_list))

    # mixed_list = ["apple", 1, "banana"]
    # print("Mixed List Result:", count_fruits(mixed_list))

except ValueError as e:
    print("Error:", e)
```

### Explanation:

- **Function Definition**: The `count_fruits` function takes a list of strings as input.
- **Empty List Check**: If the input list is empty, it returns an empty dictionary immediately.
- **String Validation**: It iterates through each item in the list and checks if the item is a string. If not, it raises a `ValueError`.
- **Counting Logic**: If the item is a valid string, it updates the count of that fruit in the `fruit_count` dictionary.
- **Example Usage**: The example shows how to use the function and handle potential errors with try-except blocks.

### Example Output:
For the provided example list `["apple", "banana", "apple", "cherry"]`, the output will be:
```
Fruit Count: {'apple': 2, 'banana': 1, 'cherry': 1}
```

You can uncomment the lines to test the error handling cases.

6 t/s, 440 tokens, 77s, 4%
