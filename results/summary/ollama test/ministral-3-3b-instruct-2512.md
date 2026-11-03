# Ministral 3 3B Instruct 2512
Model: ministral-3-3b-instruct-2512
Test: Summary Ollama Test Harness
Created: 11/02/2026, 11:47:14 AM
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

This is **both** a summary *and* an instruction.

### **Summary:**
The system automates testing of AI models (likely via Ollama) by:
- Recursively searching for model configurations (`models.txt`) and questions (`question.txt`).
- Skipping already completed tests (if `model_times.csv` exists).
- Running tests, capturing timing, responses, and formatting results.
- Generating a dashboard (`results.html`) with color-coded feedback (blue/yellow/green).

### **Instruction Breakdown:**
1. **Script Execution** – Runs `test.sh`, which:
   - Loads models/questions from subfolders.
   - Skips existing CSV logs.
   - Uses Ollama API to generate responses, records timing, and saves data.
   - Processes JSON output (no `jq`).
   - Formats results in HTML with colored statuses.

2. **Key Features:**
   - Auto-loads server (`server.js`) for `/files` endpoint.
   - Dynamically generates `results.html` from paths (e.g., "Name (path/)").
   - Uses symlinks to simulate subfolder isolation.
   - Outputs clean visuals (no borders, solid fills).

### **Why Both?**
- The first two are **technical specs** (how it works).
- The third is a **high-level overview** (what it achieves).

210 t/s, 285 tokens, 1s
