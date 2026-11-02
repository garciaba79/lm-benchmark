# Deepseek Coder 6.7B Instruct
Model: deepseek-coder-6.7b-instruct
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

Here is a Python function that fulfills your requirements:

```python
def get_display_name(test_data, fallback_name):
    if "name" in test_data and test_data["name"].strip():
        return test_data["name"]
    
    elif "test" in test_data and test_data["test"].strip():
        return ' '.join(word.capitalize() for word in test_data["test"].split())
        
    else:
        return fallback_name
```
This function first checks if the key `"name"` exists in the dictionary and is a non-empty string, returning its value directly if so. If not, it then checks if the key `"test"` exists and is a non-empty string; if this is true, it splits the string into words using space as delimiter, capitalizes each word individually, joins them back together with spaces in between, and returns this value instead. Finally, if neither of these conditions are met (i.e., `"name"` or `"test"` key does not exist or is an empty string), it simply returns the fallback name passed to the function as a parameter.

154 t/s, 268 tokens, 2s, 5%
