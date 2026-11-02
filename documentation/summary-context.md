This is the reconstructed context from a previous session.  
Carefully review this summary to fully load the context for our upcoming discussion.  
Do not generate any new information or continue the discussion yet.  

**1. Core-Data Summary (Semantic Units)**
- User: Software engineer testing local LLMs in LM Studio.
- Goal: Automate manual model testing workflow.
- Manual process: Load identical prompt + follow-up questions per model; capture full conversation, tokens/s; export as markdown; later feed files + stats to a cloud model for evaluation.
- Automation components decided: `get_models.py` (writes `models.json` from LM Studio `/api/v1/models`), `run_tests.py`, `config.json` (base_url + optional API token), `test.json` (name, description), `questions.json` (ordered string array), results written to `results/` folder.
- Result format: One markdown per model (`Model Name - YYYY-MM-DD HH.MM.md`) matching LM Studio export style, plus per-turn stats line (e.g. “831 t/s, 894 tokens, 17s, 34%”), header with context size, `test_summary.md`, and empty `results.md` for cloud evaluation.
- Behavior: Load model → full turn-based chat → unload → next model; overwrite existing files; use LM Studio model defaults; Python on Git Bash; `requests` only external dependency.
- Workflow: Copy scripts into per-test folder (e.g. “test 1”), edit configs, run scripts, manually paste cloud evaluation into `results.md`; store all test folders in a git project.
- React/Docker app discussed as future option (UI for models/questions, zip download, optional cloud evaluation) but not chosen for first version.
- Deliverables produced: `config.json`, `test.json`, `questions.json`, `get_models.py`, `run_tests.py`, `README.md`.

**2. Procedural Summary (Event Milestones)**
- User described full manual LM Studio testing workflow and asked for confirmation of understanding.
- Confirmed understanding; researched LM Studio OpenAI-compat and native v1/v0 APIs (models list, load/unload, chat completions with stats).
- User expanded requirements: overwrite files, load-run-unload loop, per-response stats (t/s, tokens, time, context %), context size in header, Python/Git Bash, prefer model defaults, first message = first question.
- User floated React + Docker app idea (UI editing, zip results, evaluation instructions, later cloud eval feature, persistent tests) and asked for thoughts.
- Recommended starting with Python scripts (faster, lower scope); React deferred.
- User added `test.json` (name + description), `results/` folder, empty `results.md`, and git-friendly per-test folder workflow.
- Generated and delivered the six files matching the final spec.
- User requested two plain-language summaries of the overall testing process and the automation project.
- Final request: three structured summaries (this response) for internal reconstruction.

**3. Outcome Summary (Goal & State)**
- Primary objective achieved: Clear, implementable Python script design and files delivered that automate the exact LM Studio test loop the user described.
- User state: Satisfied with the script approach; workflow is resolved and ready to use; React app remains an optional future enhancement.
- Most critical next action: User copies the files into a test folder, configures `questions.json`/`test.json`/`config.json`, runs a small end-to-end test, and reports any adjustments needed to stats format, filenames, or API handling.
 
Here are more summaries for what I am working on from several chats.

You are testing local models in LM Studio to see how well they handle real work.

You pick a task, such as planning a small app. You load the same starting prompt and the same follow-up questions for every model. You run the full conversation, note the speed (tokens per second), and export the chat as a markdown file. You repeat this for each model you want to compare. Then you take those files, along with the speed numbers, and give them to a cloud model. The cloud model reads the results and writes an evaluation so you can see which local model did the best job.

The manual steps take time, so you are building a small set of Python scripts that do the testing for you.

You keep a few simple files in a test folder. One file lists the models you want to test. Another holds the questions in order. A third holds the name and description of the test. A script talks to LM Studio, loads each model, asks every question in a turn-based chat, captures the replies and speed numbers, then unloads the model. It writes one markdown file per model into a results folder, plus a short summary and an empty results file. You later paste the cloud model’s evaluation into that empty file. The whole folder can live in a git repo so you can keep every test.

The scripts use the model settings you already chose in LM Studio. You run them from Git Bash. After a test finishes you still send the results to a cloud model by hand for the evaluation. A React app that does the same work inside Docker is an idea for later, once the scripts feel solid.

**Summary of the lm-benchmark project**

You are testing local models in LM Studio to compare their capability and usefulness on consistent tasks.

**How you test the models**

1. Prepare a fixed prompt and set of questions.
2. Run the same conversation with every model.
3. Capture performance metrics (tokens per second, token count, response time, context used).
4. Export the full turn-based chat as a markdown file.
5. Collect the chat files plus the metrics for all models.

**How the results are evaluated**

You share the exported chats and metrics with a large cloud model. The cloud model scores each local model on a 0–100 scale across relevant categories (output quality, correctness, task understanding, instruction following, usefulness, and others depending on the test type). It returns a summary, top models, key takeaways, practical notes, and a full ranked table.

The workflow is generic and can be used for coding, chat, data formatting, troubleshooting, or other task types. The goal is consistent, comparable rankings that help you decide which local models are worth using.

---

Here are some documents I have put together for my project.

instructions.md
workflow.md

The instructions will be used to tell the model how to evaluate the results.
The workflow describes my workflow.

Now I am automating the testing by creating a project with scripts, configurations, etc.

---

Provide me a simple summary of what I am working on and what is next.