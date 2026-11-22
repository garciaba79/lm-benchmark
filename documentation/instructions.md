## Model Evaluation Instructions

Score these local model results. Return one JSON object and nothing else. No markdown, no code fence, and no text before or after the JSON.

The object has these fields:

- summary: one short paragraph on the test and the overall findings.
- takeaways: an array of short sentences on the main patterns.
- practical: an array of short sentences on what the scores mean for real use, including speed versus edit time.
- notes: an array of short sentences for extra observations.
- models: an array with one object per model.

Each object in models has these fields only:

- key: the exact model key from the ### header. Copy it unchanged.
- avg_tps: the tokens per second shown for that model. Keep the existing value for a model already in the table.
- correctness: integer 0–100, or null if the model did not answer.
- quality: integer 0–100, or null. Readability, structure, clarity, and how easy the result is to use or edit.
- task_understanding: integer 0–100, or null. Did it grasp the goal and what was asked.
- instruction_following: integer 0–100, or null. Did it obey the format, constraints, and extra notes.
- usefulness: integer 0–100, or null. How practical the result is.
- faithfulness: integer 0–100, or null. Did it stick to the requested constraints, format, tools, or style.
- pros: one short sentence on the main strength.
- cons: one short sentence on the main problem.
- notes: one short factual sentence. Include invented details or anything that affects real use.

Scoring scale:

- 0–19: broken, unusable
- 20–39: poor, mostly unusable, near rewrite
- 40–59: fair, usable with heavy edits
- 60–79: good, solid scaffolding, light-to-moderate edits
- 80–89: strong, high quality, minor edits
- 90–100: excellent, near ready

Stay consistent. Do not heavily penalize a smaller model only for being smaller. Judge whether the output is useful and can be edited quickly. If the model lacked a full schema or full context, note a reasonable assumption and do not heavily penalize it. Use null for a question the model skipped. Do not invent a score.

A current results table may be included. Keep every model already in that table. Add every new model from this batch. You may revise an earlier score after seeing the new results. Do not drop a model. The order of models does not matter.

Example shape:

{
  "summary": "",
  "takeaways": [],
  "practical": [],
  "notes": [],
  "models": [
    {
      "key": "model-key",
      "avg_tps": 0,
      "correctness": 0,
      "quality": 0,
      "task_understanding": 0,
      "instruction_following": 0,
      "usefulness": 0,
      "faithfulness": 0,
      "pros": "",
      "cons": "",
      "notes": ""
    }
  ]
}
