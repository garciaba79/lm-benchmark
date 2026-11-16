# Gemma 4 E2B
Model: google/gemma-4-e2b
Test: Question Python Name Function
Created: 11/15/2026, 09:42:59 PM
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
    Determines the display name based on data in test_data and a fallback name.

    Args:
        test_data: The dictionary loaded from the JSON file (t).
        fallback_name: The original folder name used as a default.

    Returns:
        The determined display name.
    """
    # 1. Check if "name" exists and is a non-empty string
    if "name" in test_data and isinstance(test_data["name"], str) and test_data["name"]:
        return test_data["name"]

    # 2. Check if "test" exists and is a non-empty string
    if "test" in test_data and isinstance(test_data["test"], str) and test_data["test"]:
        # Return the value with the first letter of each word capitalized (title case)
        return test_data["test"].title()

    # 3. Otherwise, return the original folder name
    return fallback_name
```

195 t/s, 250 tokens, 1s
