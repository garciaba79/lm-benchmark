# Gemma 4 E4B
Model: google/gemma-4-e4b
Test: Question Python Name Function
Created: 11/03/2026, 12:36:17 AM
Exported from: LM Studio (via test script)
Context unknown

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
    Determines the display name based on rules applied to test data.

    Args:
        test_data: The loaded dictionary from the JSON file.
        fallback_name: The original folder name to use if no other field is suitable.

    Returns:
        The determined display name string.
    """
    # 1. Check for "name" key (Rule 1)
    if isinstance(test_data, dict):
        name = test_data.get("name")
        if name and isinstance(name, str) and name.strip():
            return name

    # 2. Check for "test" key (Rule 2)
    if isinstance(test_data, dict):
        test_value = test_data.get("test")
        if test_value and isinstance(test_value, str) and test_value.strip():
            return test_value.title()

    # 3. Fallback to original folder name (Rule 3)
    return fallback_name
```

143 t/s, 254 tokens, 2s
