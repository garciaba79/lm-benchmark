# Rnj 1
Model: essentialai/rnj-1
Test: Question Python Name Function
Created: 11/02/2026, 04:51:24 AM
Exported from: LM Studio (via test script)
Context 16K

> #### 💬 User

I have a Python script that scans a folder of test scenarios. Each scenario is a subfolder. Inside the loop I already have this:

    name = item.name          # the folder name, used as the default
    if has_test:
        t = load_json(test_json_path) or {}
        display_name = t.get("name", name)
        description = t.get("description", "")

I want a small function that replaces the line:
    display_name = t.get("name", name)

The function should:
1. Look at the loaded dict `t`.
2. If the key "name" exists and is a non-empty string, return that value exactly as it is.
3. Otherwise, if the key "test" exists and is a non-empty string, return that value with the first letter of each word capitalized (title case).
4. If neither key is usable, return the original folder name that was passed in.

The function signature should be:
    def get_display_name(test_data: dict, fallback_name: str) -> str:

Example JSON that might be in t:
{
  "name": "Question Personal Advice",
  "description": "Test how different local models respond to a question about personal advice.",
  "test": "question personal advice",
  "system_prompt": true,
  "notes": ""
}

With this JSON the function should return "Question Personal Advice".
If the "name" field were missing or empty, it should return "Question Personal Advice" (title-cased from the "test" field).
If both fields were missing or empty, it should return the fallback folder name.

Write only the function. Do not reload the JSON file inside the function. Do not redefine load_json.

> #### 🤖 Assistant

```python
def get_display_name(test_data: dict, fallback_name: str) -> str:
    """
    Returns a display name based on the provided test data and fallback name.

    Args:
        test_data (dict): The loaded JSON data.
        fallback_name (str): The original folder name to use as a fallback.

    Returns:
        str: The display name, either from the "name" field, title-cased "test" field, or the fallback name.
    """
    
    # Check if the 'name' key exists and is a non-empty string
    if test_data.get("name") and isinstance(test_data["name"], str) and test_data["name"].strip():
        return test_data["name"]
    
    # If 'name' is not usable, check if the 'test' key exists and is a non-empty string
    elif test_data.get("test") and isinstance(test_data["test"], str) and test_data["test"].strip():
        # Return the 'test' value with title case
        return test_data["test"].title()
    
    # If neither 'name' nor 'test' is usable, return the fallback name
    else:
        return fallback_name

# Example usage:
test_json_path = "path/to/your/json/file.json"
t = load_json(test_json_path) or {}
display_name = get_display_name(t, "default_folder_name")
print(display_name)
```

129 t/s, 296 tokens, 2s, 4%
