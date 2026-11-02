# Qwen2.5 Coder 14B
Model: qwen/qwen2.5-coder-14b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

Certainly! Below is the Python function that meets your requirements, along with error handling and an example usage:

```python
def count_fruits(fruit_list):
    if not fruit_list:
        return {}
    
    fruit_count = {}
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")
        
        if item in fruit_count:
            fruit_count[item] += 1
        else:
            fruit_count[item] = 1
    
    return fruit_count

# Example usage with print statements
if __name__ == "__main__":
    try:
        fruits = ["apple", "banana", "apple", "cherry"]
        result = count_fruits(fruits)
        print("Fruit counts:", result)
        
        empty_list_result = count_fruits([])
        print("Empty list result:", empty_list_result)
        
        invalid_list = ["apple", 123, "cherry"]
        invalid_result = count_fruits(invalid_list)  # This will raise an error
    except ValueError as e:
        print("Error:", e)
```

### Explanation:
- **Function `count_fruits`:**
  - It first checks if the input list is empty. If so, it returns an empty dictionary.
  - It iterates over each item in the list, checking if it is a string. If any item is not a string, it raises a `ValueError`.
  - It counts the occurrences of each unique fruit and stores them in a dictionary.

- **Example Usage:**
  - The function is called with a valid list of fruits, an empty list, and a list containing a non-string element to demonstrate error handling.
  - The results are printed to show the output of valid inputs and the error message for invalid inputs.

79 t/s, 375 tokens, 5s, 3%
