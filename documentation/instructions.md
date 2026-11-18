## Model Evaluation Instructions

These instructions are for evaluating local model results on any type of test (coding, code chat, general conversation, data formatting, search/summarization, troubleshooting, log analysis, or other tasks). The goal is consistent, useful rankings across models.

### Scoring rules

- Score every model on a 0–100 scale for each category.
- Stay consistent and realistic about model size. Do not heavily penalize smaller models simply for being smaller.
- Focus on whether the output is useful and can be quickly edited or used, not on perfect production quality.
- If a model was not given complete information (for example, an exact schema or full context), do not heavily penalize reasonable assumptions. Note them, but treat them as secondary.
- If a model did not answer a question or skipped a turn, mark that category as “—” and do not invent a score.
- Annotate model type (instruct, thinking/reasoning, agentic, or other) in the Model column when known.

### Recommended scoring scale (0–100)

- 0–19: Broken — unusable
- 20–39: Poor — mostly unusable, near rewrite
- 40–59: Fair — usable with heavy edits
- 60–79: Good — solid scaffolding, light-to-moderate edits
- 80–89: Strong — high quality, minor edits
- 90–100: Excellent — near ready

### Categories to score

When evaluation models use the categories that fit the test.  

For most tests, include these core categories.

- Output quality — readability, structure, clarity, and how easy the response is to use or edit
- Correctness — does the logic, content, or answer match the request without obvious errors
- Task understanding — does it grasp the overall goal and what was asked
- Instruction following — obeys format, constraints, and any extra notes given
- Usefulness — how practical or actionable the result is for the intended task
- Faithfulness — sticks to the requested constraints, format, tools, or style

Add or substitute task specific categories when needed.

- Code tests — Code quality, Code correctness, Faithfulness to the requested stack
- Chat or conversation tests — Coherence, Helpfulness, Tone appropriateness
- Data or formatting tests — Accuracy, Completeness, Format compliance
- Troubleshooting or log analysis — Issue identification, Clarity of explanation, Actionable next steps
- Search or summarization — Relevance, Coverage, Conciseness

### Output format

Return the results in this order.  

All tables must be valid standard Markdown tables. Every table needs a header row, a separator row of dashes, and pipe-delimited data rows. Do not output bare pipe-separated lines.

#### Summary

A short overview of the test and the overall findings.

#### Top models table

A compact table of the top 3 models with these columns:  
Rank | Model | Type | Primary score | t/s | Standout trait

(Use the most relevant primary score for the test, such as Output quality or Correctness.)

#### Key takeaways

The main patterns and standout results.

#### Practical notes from the results

What the scores mean for real use, including speed versus edit time or other practical trade-offs.

#### Full results table

One table sorted by the primary score (highest first), then by the secondary score.  
Columns: Model | [Primary score] | [Secondary score] | t/s | [Remaining categories] | Notes  

The full results table must include every model that was evaluated across all batches. Do not omit any model. Sort the complete list by the primary score, then by the secondary score.

- Annotate the model type in the Model column when known.  
- Keep Notes short and factual. Mention major strengths, critical issues, any invented details, and anything that would affect real use.  
- Mark unanswered categories as “—”.

#### Additional notes

Extra context, observations, or model-specific comments that did not fit above.

### What will be provided

- Tokens per second for each model (average or what you feel is a consistent baseline)
- Full chat transcripts (one per model)
- Brief description of the test type and any special constraints

Evaluate the models using the rules above and return the results in the format listed. Adjust the specific categories to match the test while keeping the overall structure and scoring approach consistent.