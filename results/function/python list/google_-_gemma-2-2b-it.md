# Gemma 2 2B Instruct
Model: google_-_gemma-2-2b-it
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 8K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

```python
def count_fruits(fruit_list):
  """Counts the occurrences of each unique fruit in a list.

  Args:
    fruit_list: A list of strings representing fruits.

  Returns:
    A dictionary where keys are unique fruits and values are their counts. 
    Returns an empty dictionary if the input is invalid.
  Raises:
    ValueError: If any item in the input list is not a string or if the list is empty.
  """

  if not fruit_list:  # Check for empty list
    return {}

  fruit_counts = {} 
  for fruit in fruit_list:
    if isinstance(fruit, str):
      if fruit in fruit_counts:
        fruit_counts[fruit] += 1
      else:
        fruit_counts[fruit] = 1
    else:
      raise ValueError("Input list must contain only strings.")

  return fruit_counts


# Example usage
fruits = ["apple", "banana", "apple", "cherry"]
result = count_fruits(fruits)
print(f"Fruits and their counts:\n {result}") 

empty_list = []
try:
    result = count_fruits(empty_list) 
    print(f"Result for empty list: {result}") 
except ValueError as e:
    print(e) # Print error message if the input is invalid. 
```



**Explanation:**

1. **Function Definition and Docstring:**
   - The code defines a function `count_fruits` that takes a single argument (`fruit_list`).
   - It includes a docstring explaining the purpose, arguments, return value, potential errors, and usage examples. This makes the code more understandable and maintainable.

2. **Error Handling (Empty List):**
    - The function starts with an `if not fruit_list:` check to handle the case when the input list is empty. If it's empty, it directly returns an empty dictionary (`{}`). 

3. **Input Validation:**
   -  `for fruit in fruit_list:`: This loop iterates through each item in the input list.
     - `isinstance(fruit, str):`: Inside the loop, this line checks if the current `fruit` is a string using `isinstance`. If it's not a string (e.g., an integer or float), it raises a `ValueError` with a message explaining that only strings should be in the input list.

4. **Counting Occurrences:**
   -  If the item is a string, we check if it exists as a key in our `fruit_counts` dictionary: 
      - If it does exist, increment its count (`fruit_counts[fruit] += 1`).
      - If not, create a new entry in the dictionary with a value of 1 (`fruit_counts[fruit] = 1`).

5. **Returning the Result:**
   -  After processing all items in the list, the function returns the `fruit_counts` dictionary containing the counts for each unique fruit.



Let me know if you'd like to explore any other aspects of this code or have more examples!

234 t/s, 685 tokens, 3s, 10%
