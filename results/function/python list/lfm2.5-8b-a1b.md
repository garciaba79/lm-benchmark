# LFM2.5 8B A1B
Model: lfm2.5-8b-a1b
Test: Function Python List
Created: 11/02/2026, 01:02:53 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

Write a clean Python function that takes a list of strings (like ["apple", "banana", "apple", "cherry"]) and returns a dictionary with each unique fruit as key and its count as value (e.g., {"apple": 2, "banana": 1, "cherry": 1}). 

Then add error handling: if the list is empty, return an empty dict; if any item is not a string, raise a ValueError with a clear message.

Finally, write a short example usage with print statements showing the result.

> #### 🤖 Assistant

def count_fruits(fruit_list):
    if not isinstance(fruit_list, list):
        raise TypeError("Input must be a list")
    if len(fruit_list) == 0:
        return {}
    for item in fruit_list:
        if not isinstance(item, str):
            raise ValueError(f"All items must be strings, found {type(item).__name__} at position {fruit_list.index(item)}")
    counts = {}
    for item in fruit_list:
        counts[item] = counts.get(item, 0) + 1
    return counts

# Example usage
if __name__ == "__main__":
    fruits = ["apple", "banana", "apple", "cherry"]
    print(count_fruits(fruits))
    # {'apple': 2, 'banana': 1, 'cherry': 1}
    
    empty_list = []
    print(count_fruits(empty_list))  # {}
    
    invalid_items = ["apple", 123, "orange"]
    try:
        count_fruits(invalid_items)
    except ValueError as e:
        print(e)  # All items must be strings, found int at position 1

390 t/s, 746 tokens, 2s, 5%
