## Local Model Testing Workflow

This document is the manual process for testing local models in LM Studio. The same steps are what `run.py` and `evaluate.py` automate. Use this page when you run a test by hand. Use the scripts for the normal path.

### Overview

Each test uses the same prompts and questions for every model. After the conversations are complete, the results are collected and reviewed by a large cloud model that evaluates and ranks performance.

### Steps

#### Prepare the test

- Define the prompt and the questions that every model will receive.
- Keep the input identical across all models.
- In this project the questions are `question1.md`, `question2.md`, and so on, with no gaps. The scenario name and description go in `test.json`. An optional system prompt is `system.md` or the `system` field in `inference.json`.
- If a model consistently fails to follow the questions, revise the questions so the test stays the same for everyone.

#### Run the conversations

- Load each model in LM Studio.
- Run the full conversation with the same prompts and questions.
- Let the model finish every turn before you move to the next model.
- `run.py` does this load, chat, and unload loop. `update` runs models that do not already have a result file. `refresh` reruns every model on the active list. `none` skips the scenario.

#### Capture performance metrics

Record these for each reply:

- tokens per second (t/s)
- number of tokens generated
- time spent responding (seconds, then minutes or hours for a long run)
- context used so far, as a percent

The percent is how full the context window is after that reply: tokens used so far divided by the context length the model was loaded with. It is not a separate score. When LM Studio reports the loaded context, use that number. Otherwise use the context in `inference.json`. If neither is set, use 16K, which is the usual window in this project. Some models are loaded at 8K.

#### Export the results

- Save the complete turn-by-turn conversation for each model.
- A hand export can use a filename with the model name and the date.
- `run.py` writes `results/<scenario>/<model-key>.md` for reading, and `<model-key>.json` for reconstruction. The JSON object holds `system_prompt` and `context_length`. The system prompt is not a message in that file, and it is not copied into the markdown.

#### Collect the test artifacts

- Gather the chat files.
- Include tokens per second and the other test information: model key, display name, parameter size, quantization, and context length.
- The script stores those fields in `results/<scenario>/stats.json` and `models.json`. Both files are lists of records updated by key.

#### Evaluate with a cloud model

- Share the collected files and test information with a large cloud model.
- Ask it to review the results, compare the models, and rank them on the test.
- By hand, save the JSON score table as `results.json`.
- `python evaluate.py` sends the result files in batches, saves `results.json`, and writes `results.md` from that file. The default cloud backend is the Grok API.

### Consistency rules

- Every model receives the same starting prompt and the same questions.
- The full conversation is captured for each model.
- Evaluation is done by a large cloud model using the exported transcripts.
- The process is repeated for every model in the test so the inputs stay identical.

### Note

The standard path is `python run.py` for the conversations and `python evaluate.py` for the ranking. Setup, modes, and hand edits are in [get-started.md](get-started.md). A full project briefing for a cloud model is [lm-benchmark.md](lm-benchmark.md).
