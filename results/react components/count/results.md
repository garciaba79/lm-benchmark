# Evaluation Results

**Summary**

This test asked every model to write a simple, fully typed React functional component in TypeScript: a counter that accepts an optional `initialCount` (default 0), displays the value in a large centered heading, and provides Increment / Decrement buttons that never go below 0. Styling had to stay inline or in a basic style object. No external CSS or libraries.

33 models were evaluated. The strongest results produced clean, near-ready components that used functional state updates and a proper floor at 0. Smaller models and a few mid-size ones failed on syntax, missing handlers, or basic requirements such as displaying the count. Quality did not strictly track size: several 3B–9B models matched or beat much larger ones.

**Top models table**

| Rank | Model | Type | Primary score | t/s | Standout trait |
|------|-------|------|---------------|-----|----------------|
| 1 | google/gemma-4-12b | instruct | 95 | 82 | Production-ready structure, functional updates, Math.max, aria-labels |
| 2 | microsoft/phi-4 | instruct | 94 | 82 | Functional updates, disabled buttons, clean styles object |
| 3 | qwen/qwen3.5-9b | instruct | 94 | 121 | Color-coded buttons, functional + Math.max, aria-labels |

**Key takeaways**

- The top tier (95–90) consistently used functional updates (`setCount(prev => …)`) and a clear floor (`Math.max` or equivalent ternary).
- Several small models (Ministral 3B, Qwen3.5 4B, Qwen2.5 Coder 7B) performed at or near the level of much larger models.
- Common failure modes were non-functional `setCount(count + 1)`, missing `onClick` handlers, invalid style objects or JSX, and forgetting to render the count value.
- The smallest models (LFM2.5 230M / 350M) did not produce working React components.
- Speed varied widely; the slowest large models (Qwen2.5 Coder 32B at ~6 t/s) still produced usable code after self-correction, but the wait was long.

**Practical notes from the results**

Models scoring 90+ can be used with only light cleanup (mainly confirming functional updates and minor style tweaks). Models in the 80–89 range are solid scaffolds that need moderate edits. Below 60 the output usually requires a rewrite. For this task, a fast 3B–9B model that scores 90+ is more practical than a slow 30B model that scores the same, because edit time dominates total time. Gemma 4 12B, Phi 4, and Qwen3.5 9B are the clearest “drop in and lightly polish” choices.

**Full results table**

| Model | Correctness | Output quality | t/s | Task understanding | Instruction following | Usefulness | Faithfulness | Notes |
|-------|-------------|----------------|-----|--------------------|-----------------------|------------|--------------|-------|
| google/gemma-4-12b (instruct) | 95 | 90 | 82 | 95 | 95 | 92 | 95 | Excellent: functional updates, Math.max, typed styles, aria-labels, clean structure. Near ready. |
| microsoft/phi-4 (instruct) | 94 | 88 | 82 | 95 | 95 | 92 | 95 | Excellent: functional + Math.max, default handled, disabled buttons, clean styles. Near ready. |
| qwen/qwen3.5-9b (instruct) | 94 | 90 | 121 | 95 | 95 | 92 | 95 | Excellent: functional + Math.max, color-coded buttons, aria-labels, polished styles. Near ready. |
| openai/gpt-oss-20b (instruct) | 93 | 90 | 132 | 95 | 95 | 91 | 95 | Excellent: functional updates, ternary floor, working hover via state, clean typed styles. |
| qwen2.5-coder-7b-instruct (instruct) | 93 | 85 | 149 | 95 | 95 | 90 | 95 | Clean and correct. Functional + Math.max, default in destructuring, centered layout. |
| qwen/qwen3-coder-30b (instruct) | 93 | 88 | 62 | 95 | 95 | 91 | 95 | Strong functional + Math.max, clean styles, working hover. Minor leave-color inconsistency on Decrement. |
| qwen/qwen3.8-27b (instruct) | 93 | 87 | 23 | 95 | 95 | 91 | 95 | Excellent: functional ternary floor, disabled button, distinct colors, card layout. Slow but near ready. |
| liquid/lfm2-24b-a2b (instruct) | 92 | 88 | 111 | 95 | 95 | 90 | 95 | Excellent: functional + Math.max, default handled, count displayed, clean centered styles. |
| qwen3.5-4b (instruct) | 92 | 87 | 176 | 95 | 92 | 90 | 92 | Strong: functional + Math.max, nice styles object, large heading. Near ready. |
| ministral-3-3b-reasoning-2512 (reasoning) | 91 | 86 | 214 | 95 | 92 | 89 | 92 | Clean and correct. Functional updates, ternary floor, full-height centered layout. |
| deepseek-coder-6.7b-instruct (instruct) | 90 | 85 | 157 | 95 | 90 | 88 | 90 | Clean and correct. Functional updates + Math.max. Minimal but solid styling. |
| ministral-3-3b-instruct-2512 (instruct) | 90 | 85 | 232 | 95 | 90 | 88 | 90 | Strong: functional + Math.max, nice card-style styles. Button colors swapped but functional. |
| qwen/qwen2.5-coder-14b (instruct) | 88 | 82 | 79 | 95 | 90 | 86 | 90 | Solid. Functional increment; if-check + functional decrement. Clean styles object. |
| qwen2.5-coder-32b-instruct (instruct) | 88 | 80 | 6 | 90 | 80 | 85 | 80 | First version referenced undefined hover (won’t compile). Self-corrected with clean final version. Very slow. |
| nvidia_nvidia-nemotron-nano-9b-v2 (instruct) | 85 | 82 | 103 | 90 | 88 | 83 | 85 | Solid and complete. Functional increment; if-check + functional decrement. Good color coding. |
| lfm2.5-vl-3b (instruct) | 82 | 78 | 289 | 90 | 85 | 80 | 85 | Complete and correct. Non-functional setCount(count + 1). Good colors and layout. |
| ministral-3-8b-instruct-2512 (instruct) | 82 | 80 | 127 | 90 | 85 | 80 | 80 | Good structure and disabled button. Mixed update style; invalid `':hover'` key in style object. |
| qwen/qwen3-14b (instruct) | 82 | 80 | 79 | 90 | 85 | 80 | 85 | Works and is complete. Non-functional setCount(count + 1). Nice colored buttons. |
| qwen2.5-coder-1.5b-instruct (instruct) | 82 | 72 | 324 | 90 | 85 | 80 | 85 | Works and is complete. Functional updates, disabled button, basic styles. Fast. |
| granite-4.1-8b (instruct) | 80 | 75 | 127 | 90 | 85 | 80 | 85 | Works and is complete. Non-functional setCount(count + 1). Adds disabled button. Verbose but clear. |
| mamba-codestral-7b-v0.1 (instruct) | 80 | 70 | 150 | 90 | 85 | 78 | 85 | Concise and correct enough. Non-functional updates. Minimal styles. Easy to edit. |
| lfm2.5-1.2b-instruct (instruct) | 78 | 80 | 580 | 90 | 85 | 78 | 85 | Works and is complete. Non-functional update; redundant Math.max. Nice styling. Very fast. |
| nvidia/nemotron-3-nano-4b (instruct) | 65 | 70 | 225 | 80 | 75 | 60 | 70 | Logic good (functional + Math.max) but `Number(undefined)` yields NaN when prop omitted. |
| lfm2.5-24b-a2b (instruct) | 55 | 80 | 108 | 75 | 70 | 50 | 65 | Logic correct (functional + Math.max) but heading never shows the count value. Major omission. |
| essentialai/rnj-1 | 40 | 20 | 129 | 10 | 5 | 15 | 10 | Completely misunderstood the task. Output a Python string containing TS code instead of the component. |
| lfm2.5-2.6b (instruct) | 40 | 55 | 287 | 75 | 50 | 35 | 50 | Functional updates good, but syntax error in styles object, no default on useState(undefined), wrong button labels. |
| ornith-1.5-9b (instruct) | 40 | 75 | 145 | 70 | 55 | 35 | 50 | Decrement button has no onClick handler. Increment works (non-functional). Nice styles but core feature missing. |
| lfm2.5-1.2b-thinking (instruct) | 35 | 50 | 568 | 60 | 40 | 30 | 45 | Invalid interface syntax. Does not render the count at all. Functional updates present but incomplete. |
| falcon-h1r-7b (instruct) | 30 | 60 | 106 | 70 | 50 | 35 | 40 | Major bugs: no default on useState(undefined), broken increment logic, invalid CSS (onHover). Needs rewrite. |
| google/gemma-4-e4b (instruct) | 25 | 40 | 142 | 70 | 40 | 20 | 30 | Syntax errors in styles object (invalid nested const, malformed object). Will not compile. |
| lfm2.5-8b-a1b (instruct) | 25 | 60 | 390 | 70 | 45 | 25 | 40 | References undefined `props`. Invalid CSS (`justifyContent: 'middle'`). Logic otherwise sound. Will not compile. |
| lfm2.5-350m | 15 | 25 | 828 | 40 | 20 | 15 | 20 | Invalid JSX (adjacent elements without fragment). Decrement can go below 0. Incomplete. |
| lfm2.5-230m | 5 | 15 | 1029 | 10 | 5 | 5 | 5 | No useState, mutates const, functions outside component, count never updates or displays. Unusable. |

**Additional notes**

- Primary score is Correctness (code correctness). Secondary is Output quality.
- Scores reflect the usable code delivered, not model size. Smaller models were not heavily penalized for being smaller when the output was functional.
- Models that shipped broken first versions and then self-corrected (e.g. Qwen2.5 Coder 32B) received partial credit for the final usable result, but the initial error lowered the score relative to models that got it right the first time.
- The LFM2.5 family showed wide variance: the 1.2B Instruct and VL 3B were usable, while the 230M/350M and several mid-size variants were not.
- Overall run time was about 7.5 minutes across all 33 models. The practical bottleneck for real use is edit time, not generation speed, once Correctness drops below ~85.
