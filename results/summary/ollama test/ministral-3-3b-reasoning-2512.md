# Ministral 3 3B Reasoning 2512
Model: ministral-3-3b-reasoning-2512
Test: Summary Ollama Test Harness
Created: 11/02/2026, 11:49:39 AM
Exported from: LM Studio (via test script)
Context unknown

> #### 💬 User

Here is either a conversation summary or an instruction.

Provide me a simple summary of what this is for and what it is doing?

Do you think it's a summary, instruction or both?

---

1. Highly Condensed, Core-Data Summary (Key Semantic Units)

test.sh → recursive models.txt + question.txt search → results/ creation → Ollama API test → model_times.csv + _response.txt → skip if CSV exists → JSON build → curl → time calc → grep/sed fallback → color output (blue, yellow, green) → server.js API /files → auto-load → no jq → results.html title from path → no borders → symlinks.

2. Event Specifications Summary (Short, Precise Language)

Script: test.sh in tests/
Action: find subfolders → models.txt + question.txt
Skip: results/model_times.csv exists
Run: ollama run → curl /generate → time → save CSV + response
JSON: printf + sed escape → no jq
Output: blue = test, yellow = warning, green = finish
Server: server.js → /files JSON → results.html auto-load
Title: Name (path/) → small path line
Chart: no borders, solid fill
Links: symlinks in subfolders → main files

3. Outcome-Oriented Summary (NLP Style)

You now own a fully automated, self-healing test system that effortlessly discovers and executes every model challenge across any folder depth — skipping only completed work, never failing on missing tools, and delivering crystal-clear, color-coded feedback in real time.
Your single source of truth lives in tests/, while every subfolder runs as if it had the full system — thanks to invisible symlinks.
The results speak instantly: clean CSVs, rich responses, and a visual dashboard that highlights performance at a glance — no borders, no noise, just pure signal.
You press one command, and the entire ecosystem aligns — accurate, fast, and future-proof.
Confidence is now automatic.

> #### 🤖 Assistant

This is both a summary and an instruction.

**Summary:**
The document describes a script called `test.sh` that automates the process of testing models in a directory structure. It recursively searches for subfolders containing `models.txt` and `question.txt`, runs them using the Ollama API, and generates results in CSV format and response files. If the CSV file already exists, it skips the run. The output is processed to create JSON, sent via curl, and time calculations are performed. Fallback mechanisms use grep and sed for processing. The final output is color-coded (blue for tests, yellow for warnings, green for finishes) and displayed in a server-generated HTML file with no borders or noise.

**Instruction:**
The script performs the following actions:
1. Recursively searches for subfolders containing `models.txt` and `question.txt`.
2. Skips execution if `results/model_times.csv` already exists.
3. Runs the models using the Ollama API, generates responses, and saves them to CSV and response files.
4. Processes the output with JSON (using printf and sed), curl, time calculations, and fallback mechanisms (grep/sed).
5. Displays color-coded output in a server-generated HTML file without borders or noise.
6. Uses symlinks for subfolders and auto-loads results from `server.js` to create `results.html`.
7. The title of the HTML is derived from the path, and links are created using symlinks.

**Outcome-Oriented Summary (NLP Style):**
The script creates an automated test system that can discover and execute model challenges across any folder depth, skipping completed work and missing tools. It delivers real-time, color-coded feedback in a clean HTML dashboard with no borders or noise, ensuring accurate, fast, and future-proof results. The entire ecosystem aligns with one command, and confidence is automatic.

194 t/s, 388 tokens, 2s
