
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

---

### review of the code on 11/23/2026 checking for any issues

No major underlying issues. The evaluation path is carefully built so the harness owns the structured state and the model is forced to return a complete, valid object each time.

A few smaller points are worth knowing.

**Token and size growth**
Each batch sends the full current results JSON plus the new transcripts, and asks for the full object back. With 30 models and longer notes or pros/cons fields, the prompt and the reply both get large. Grok can handle it at the current batch size, but bigger scenarios raise the chance of hitting an output limit. The code already treats a length-truncated reply as a failure and triggers the repair turn.

**Repair is only one attempt**
If the second reply is still missing a batch key or fails the schema, that batch stops. The previous results.json is left as it was. You can re-run later and it will resume from the models that already have records.

**No separate top-models list**
The original markdown had a short top table. The current schema has one models array that is sorted by correctness, then quality. The markdown table is generated from that sorted list. If you still want an explicit top-models section, it would need to be added to the schema and the prompt.

**Table width**
results.md puts pros, cons, and notes into table cells. Those fields can be long, so the table becomes wide. That is only a display issue; the JSON stays clean.

**Conversation is not sent back**
Each API call is a single user message that already contains the current results JSON. Earlier turns are saved for the human-readable log but are not included in later requests. That is intentional and keeps context from growing with chat history.

**Schema is strict for OpenAI-compatible backends**
Grok API and OpenAI get the JSON schema with additionalProperties false and required fields. Anthropic and the CLI do not. Those backends rely only on the prompt, so they are more likely to need the repair path.

The rest of the design (keyed upserts, update versus refresh modes, archive-before-delete, sticky used_ram, three-level prompt and inference lookup) is consistent and defensive. Nothing looks likely to silently drop results or wipe data.