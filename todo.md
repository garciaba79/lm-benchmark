
### todo

#### These are the open items from the last round

- Save or leave the three hand-written evaluation-grok-4.3.md files. The next evaluate.py run for grok-4.3 will replace them, because those folders have no matching JSON.
- Leave old result transcripts as they are, or run those models again so each one gets a <model-key>.json with the system prompt and context length.
- Leave the already written test.md files for fetch weather and validate email. They still show the old React description until a later run rewrites them.
- Try the Grok CLI plugin again. The --prompt-file change has not been run.
- Leave scenarios/info.md as it is. The helper text still says 43 scenarios.
- Decide later whether an unknown scenario mode should keep acting like refresh.
- Decide later whether to keep documentation/plugin.md and documentation/summary-app.md.

---

Fix the Grok evaluation prompt. Grok does a great job evaluating and ranking but by the time the evaluation is done the table is missing numerous results.
The conversation shows that Grok has evaluated the missing models, but they get dropped and not sure why.
The project now uses json, it might be easier for Grok to evaluate them more accurately. Grok should be able to handle the structured data in the JSON files better than it does with markdown.

---

- test the scripts, run at least one scenario, evaluation, cleanup, etc.
- verify the scripts are working as planned
- test Grok CLI plugin again. The --prompt-file change has not been run.

---

* make sure that all scripts are writing data to json files with structured data and keys
* this is more reliable for code, maintenance, debugging and transition to using a database
- it's fine if there are unstructured markdown files for humans to read
* plan to move all data to a DB, maylbe MongoDB
- then stop using json and md files
- I might leave the md files around, that makes it easy to examine in VS Code and GitHub

---

* plan a user interface that makes it lovely to operate the test harness
- runs scripts
- manages tests and results
- able to run all, some or a few tests
- other features like viewing results, editing scenarios, etc.
- I can move all data to the DB
- I might leave the scenarios as md for human readability, agents, etc.
- add dashboard
- add reports and analytics
- think of other nice ideas like a leaderboard or ranking system
- add scenario categories, filtering, etc.

---

- add unit testing to ensure that all scripts are working as expected
- tests for the scripts, plugins and project
