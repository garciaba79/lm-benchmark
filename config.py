"""
Shared configuration for the LM Studio model test harness.

All scripts import paths, connection settings, and defaults from here.
"""

from pathlib import Path

# ==========================================
# CONNECTION (formerly config.json)
# ==========================================
BASE_URL = "http://localhost:1234"
API_TOKEN = ""
HELPER_MODEL = "lfm2.5-1.2b-thinking"                          # Optional helper model used for short summaries

# ==========================================
# PROMPTS
#
# Helper model prompt (optional, used only if a helper model is set and available)
# Helper summaries are generated at the end of the full run, after all test models are unloaded.
# ==========================================
RUN_SUMMARY_PROMPT = """Write a short simple summary of these test results. Mention overall speed and any notable differences."""
SCENARIOS_SUMMARY_PROMPT = """Provide a simple summary for the test scenarios. Mention how many tests are complete, partial, or not started."""

# ==========================================
# PATHS
# ==========================================
SCENARIOS_DIR = Path("scenarios")                       # Folder containing one subfolder per test scenario
RESULTS_DIR = Path("results")                           # Folder where per-scenario results, stats, and snapshots are written
ARCHIVE_DIR = Path("archive")

TEST_JSON = "test.json"                                 # Per scenario metadata (name, description, system_prompt flag, notes)

MODELS_PATH = SCENARIOS_DIR / "models.json"             # Master list of models to test (created by get_models.py)
SCENARIOS_JSON = SCENARIOS_DIR / "scenarios.json"       # List of scenarios with ready/status/mode (created by get_scenarios.py)
SCENARIOS_MD = SCENARIOS_DIR / "scenarios.md"

ROOT_STATS_JSON = RESULTS_DIR / "stats.json"            # System-wide model stats (VRAM/spill, times, scenarios)
ROOT_STATS_MD = RESULTS_DIR / "stats.md"                # Readable system-wide stats

INFERENCE_PATH = SCENARIOS_DIR / "inference.json"       # Optional inference settings (context, temperature, top_p, etc.) used when USE_CUSTOM_INFER is True
SYSTEM_PROMPT_PATH = SCENARIOS_DIR / "system.md"        # Fallback system prompt used if a scenario does not have its own system.md

HARDWARE_PATH = Path("meta/hardware.json")              # Static hardware snapshot written at the start of each run

# ==========================================
# RUN SETTINGS
# ==========================================
DRY_RUN = False                                         # Set to true to print what would run without loading models or writing results
FORCE_MODE = None                                       # Overrides the mode in scenarios.json: None | "update" | "refresh" | "none"
USE_CUSTOM_INFER = True                                 # Set to true to use inference settings from inference.json (or scenario override), set to false to use LM Studio defaults
CHAT_TIMEOUT = 900                                      # Max seconds to wait for a single chat response before timing out (default is 900 seconds, which is 15 minutes)

# Hardware spill detection
INSTALLED_RAM_GB = 32                                   # Total system RAM in GB (used to calculate spill threshold)
INSTALLED_VRAM_GB = 16                                  # Total GPU VRAM in GB (reference only)
RAM_SPILL_THRESHOLD_PERCENT = 25                        # If RAM usage rises by this percent during a test, then let's assume the model spilled into VRAM

# ==========================================
# CLEAN SETTINGS (defaults; CLI can override)
# ==========================================
ARCHIVE = True
CLEAN = True
RESULTS = True
STATS = True

# ==========================================
# SCENARIOS SETTINGS
# ==========================================
DEFAULT_MODE = "update"
REQUIRE_TEST_JSON = True
REQUIRE_AT_LEAST_ONE_QUESTION = True

# ==========================================
# MODELS SORTING
# ==========================================
REVERSE_PARAMS = False     # Smallest params first (e.g., 230M, 4B, 8B, 24B)
REVERSE_NAME = False       # Descending name tie breaker (Z -> A / apple, banana order)
REVERSE_SIZE = False       # Smallest file size catch-all

# ==========================================
# EVALUATION SETTINGS
# ==========================================
# Backend used by evaluate.py.
# Options: "grok_cli", "openai", "anthropic", "gemini", "grok_api"
# Default is the Grok CLI (uses your SuperGrok subscription, no extra API fees).
EVAL_BACKEND = "grok_api"

# How many model result files to send in each batch.
# Example: 5
EVAL_BATCH_SIZE = 5

# Path to the long scoring instructions, loaded once at the start.
EVAL_INSTRUCTIONS_PATH = Path("documentation/instructions.md")

# Prompts used by the evaluator (short strings the script sends).
EVAL_INITIAL_PROMPT = """Read these evaluation instructions carefully. I will send the test results in several batches. After each batch, score the models in that batch using the same scale and categories. You may revise earlier scores after seeing later batches. Keep all intermediate scores in context. Acknowledge that you are ready and wait for the first batch."""

EVAL_BATCH_PROMPT = """Here are some test results. Score the models in this batch and keep the scores in context."""

EVAL_FINAL_PROMPT = """All results have been provided. Produce the final ranked results using your intermediate scores and any revisions, in the format required by the instructions."""

# Optional model name override for the chosen backend.
# Examples:
#   "grok-4.3"                      Grok API or CLI
#   "grok-4.7"                      Grok API or CLI
#   "gpt-4o"                        OpenAI
#   "claude-3-5-sonnet-20241022"    Anthropic
#   "gemini-1.5-pro"                Gemini
EVAL_MODEL = "grok-4.3"

# Base URL for OpenAI-compatible backends (openai, gemini, grok_api).
# Examples:
#   "https://api.openai.com/v1"
#   "https://api.x.ai/v1"
#   "https://generativelanguage.googleapis.com/v1beta/openai"
EVAL_BASE_URL = "https://api.x.ai/v1"

# Dry run flag (can also be passed on the command line).
EVAL_DRY_RUN = False
