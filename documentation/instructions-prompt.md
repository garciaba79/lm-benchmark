## Manual Evaluation

The scoring rules and the JSON shape are in [instructions.md](instructions.md). Paste that file at the start of the conversation.

## Each batch

Send this with the current results JSON and the new transcripts:

Here is the current results JSON. Score the new transcripts. Return the full JSON object, including every model already in the JSON and every new model.

On the first batch, use an empty table:

```json
{
  "summary": "",
  "takeaways": [],
  "practical": [],
  "notes": [],
  "models": []
}
```

Put each transcript under a `### model-key` heading. Save the JSON object the model returns, and send that object back as the current results with the next batch.

`python evaluate.py` does this itself. It keeps any model the reply leaves out, then writes `results.json` and `results.md`.
