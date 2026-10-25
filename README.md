# lm-benchmark

LM Studio Local Model Test Scripts  

Simple Python scripts that automate running the same set of questions against every model you select in LM Studio. Results are written as markdown files that match the style of a manual LM Studio export.

## Files

- `config.json` — LM Studio address and optional API token
- `test.json` — name and description for this test run
- `questions.json` — array of questions (asked in order)
- `models.json` — created by `get_models.py` (edit to keep only the models you want)
- `get_models.py` — fetches models from LM Studio and writes `models.json`
- `run_tests.py` — loads each model, runs the questions, writes results

## Setup

1. Make sure the LM Studio local server is running (Developer tab or `lms server start`).
2. Copy these files into a test folder (example: `tests/weather-app/`).
3. Edit `config.json` if your server is not on `localhost:1234`. Add an API token if you enabled one.
4. Edit `test.json` and `questions.json` for the test you want to run.

## Run

```bash
python get_models.py
# edit models.json if needed
python run_tests.py
```

## Output

Everything lands in a `results/` folder:

- One markdown file per model (named `Model Name - 2026-10-24 23.07.md`)
- `test_summary.md` with the test name, description, and list of models
- `results.md` (empty, ready for you to paste the cloud evaluation)

The model markdown files include the conversation turns plus a short stats line on each assistant reply (tokens/s, token count, time, context percent).

## Notes

- The scripts use the model defaults you already set in LM Studio.
- Files are overwritten if they already exist.
- After a run you can start a cloud chat, paste your evaluation instructions, and save the answer into `results.md`.
- The whole test folder is easy to keep in git.
