# Evaluation Results

#### Summary
This is the consolidated evaluation for the full “summary expedition” run after all batches and the accompanying stats. The test required models to stay quiet while receiving successive notes about a 2014 Ford Expedition knock diagnosis, then produce a dense three-part handoff (Core-Data, Procedural, Outcome) only when the final archivist instruction arrived. Output quality is the primary score. Instruction following (silence until the end) is weighted because early diagnostic replies violated the constraint. Speed data now comes from the provided stats.

#### Top models table

| Rank | Model | Type | Primary score | t/s | Standout trait |
|------|-------|------|---------------|-----|----------------|
1 | Ornith 1.5 9B | instruct | 85 | 142 | Cleanest standby plus densest usable handoff
2 | Qwen3.8 27B | instruct | 82 | 6 | Highest density of shops, costs, and rankings
3 | Qwen2.5 Coder 32B Instruct | instruct | 76 | 5 | Strong structure and coverage despite slow speed

#### Key takeaways
- Ornith 1.5 9B remains the strongest overall result. It followed the silence rule cleanly and still produced a handoff dense enough for a fresh session.
- Qwen3.8 27B and the larger Qwen2.5 Coder models retained the most concrete facts (Leavins, Fraser, cost bands, cause rankings, PCV layout). Their low tokens-per-second is the main practical cost.
- Several mid-size models (Gemma 4 12B, Falcon H1R 7B, LFM2.5 24B A2B) produced usable density but broke the standby rule by generating diagnostic plans mid-stream.
- Very small models (LFM2.5 230M/350M, Rnj 1) either stayed silent and produced thin output or generated early replies that still lacked concrete numbers.
- Deepseek Coder 6.7B Instruct refused the archival task as outside its expertise, so it is not usable for this scenario.

#### Practical notes from the results
For a constrained multi-document archival task, Ornith 1.5 9B offers the best combination of instruction compliance and usable density at a practical speed. The larger Qwen models are worth the wait only when maximum fact retention matters more than turn time. Models that generate diagnostic advice before the final instruction require extra cleanup even when their final handoff looks dense. Speed alone is not decisive: the fastest models (LFM2.5 230M/350M) produced the least usable handoffs.

#### Full results table

| Model | Output quality | Faithfulness | t/s | Correctness | Task understanding | Instruction following | Usefulness | Notes |
|-------|----------------|--------------|-----|-------------|--------------------|-----------------------|------------|-------|
Ornith 1.5 9B (instruct) | 85 | 82 | 142 | 84 | 85 | 90 | 84 | Clean standby. Final handoff keeps shops, costs, rankings, and next-step priorities.
Qwen3.8 27B (instruct) | 82 | 80 | 6 | 83 | 80 | 75 | 80 | Slow but densest retention of concrete facts. Minor early content in some turns.
Qwen2.5 Coder 32B Instruct (instruct) | 76 | 74 | 5 | 78 | 76 | 70 | 75 | Strong structure. Slow final turn. Retains cost bands and rankings.
Qwen3 14B (instruct) | 74 | 72 | 65 | 75 | 74 | 68 | 73 | Solid density. Some intermediate summaries.
LFM2.5 24B A2B (instruct) | 72 | 70 | 117 | 73 | 72 | 55 | 70 | Usable density. Generated diagnostic content before the final instruction.
Qwen2.5 Coder 14B (instruct) | 70 | 68 | 7 | 72 | 70 | 65 | 69 | Good coverage. Slow. Minor format deviations.
Qwen3 Coder 30B (instruct) | 70 | 65 | 39 | 70 | 68 | 40 | 66 | Added extra section and early replies. Density is competitive when cleaned.
Liquid LFM2 24B A2B (instruct) | 70 | 68 | 90 | 71 | 70 | 50 | 68 | Similar pattern to LFM2.5 24B. Usable after cleanup.
Qwen3.5 9B (instruct) | 68 | 66 | 116 | 70 | 68 | 60 | 67 | Good balance of speed and density. Some early content.
Qwen2.5 Coder 7B Instruct (instruct) | 68 | 65 | 129 | 69 | 68 | 62 | 66 | Cleaner standby than many peers. Thinner than 14B/32B.
Ministral 3 8B Instruct 2512 (instruct) | 68 | 65 | 104 | 68 | 67 | 55 | 65 | Structured output. Intermediate diagnostic plans.
Qwen3.5 4B (instruct) | 65 | 62 | 146 | 66 | 64 | 50 | 63 | Usable skeleton. Drops some concrete numbers.
Gemma 4 12B (instruct) | 62 | 60 | 71 | 65 | 62 | 45 | 60 | Denser final than E4B. Generated summaries mid-stream.
GPT-OSS 20B (instruct) | 62 | 60 | 178 | 63 | 62 | 55 | 61 | Fast. Moderate density. Some early replies.
LFM2.5 8B A1B (instruct) | 60 | 58 | 342 | 61 | 60 | 50 | 59 | Fast. Usable but thinner than larger LFM variants.
Falcon H1R 7B (instruct) | 60 | 55 | 91 | 62 | 58 | 30 | 58 | Dense final. Large diagnostic tables generated early.
LFM2.5 VL 3B (instruct) | 58 | 55 | 181 | 58 | 57 | 70 | 56 | Quiet until near the end. Final output is thin.
Nvidia Nemotron Nano 9B v2 (instruct) | 58 | 55 | 101 | 59 | 58 | 45 | 57 | Moderate density. Intermediate content.
Granite 4.1 8B (instruct) | 58 | 55 | 103 | 60 | 58 | 35 | 56 | Generated diagnostic plans early. Final keeps shops and costs.
Ministral 3 3B Instruct 2512 (instruct) | 55 | 52 | 164 | 56 | 55 | 50 | 54 | Structured but drops key numbers.
Microsoft Phi 4 (instruct) | 55 | 52 | 71 | 56 | 54 | 40 | 53 | Intermediate summaries. Moderate final density.
Gemma 4 E4B (instruct) | 50 | 48 | 127 | 52 | 50 | 30 | 48 | Broke standby. Final is structured but thinner.
Ministral 3 3B Reasoning 2512 (instruct) | 50 | 48 | 158 | 51 | 50 | 45 | 49 | Reasoning variant did not improve archival density.
LFM2.5 1.2B Instruct (instruct) | 48 | 45 | 404 | 50 | 48 | 70 | 46 | Cleaner standby. Final too thin for high fidelity.
Nemotron 3 Nano 4B (instruct) | 48 | 45 | 190 | 50 | 47 | 40 | 46 | Early content. Thin final.
LFM2.5 2.6B (instruct) | 42 | 40 | 244 | 45 | 42 | 30 | 40 | Broke standby with action lists. Thinner final.
Qwen2.5 Coder 1.5B Instruct (instruct) | 42 | 40 | 136 | 44 | 42 | 55 | 41 | Quiet until end. Final incomplete.
Rnj 1 (instruct) | 38 | 35 | 100 | 40 | 35 | 75 | 35 | Clean silence. Extremely thin final handoff.
Mamba Codestral 7B v0.1 (instruct) | 38 | 35 | 150 | 40 | 38 | 45 | 37 | Early replies. Low density of concrete facts.
LFM2.5 1.2B Thinking (instruct) | 35 | 30 | 487 | 35 | 32 | 65 | 32 | Quiet until near end. Final inaccurate and thin.
LFM2.5 350M (instruct) | 32 | 28 | 572 | 32 | 30 | 60 | 30 | Fast. Minimal usable content.
LFM2.5 230M (instruct) | 28 | 25 | 755 | 28 | 26 | 55 | 26 | Fastest. Unusable density.
Deepseek Coder 6.7B Instruct (instruct) | 25 | 20 | 29 | 25 | 20 | 15 | 20 | Refused the archival task as outside expertise.

#### Additional notes
- Primary score remains Output quality of the final three-part handoff (density, structure, exact terminology, and usability for a fresh session).
- Instruction following is weighted because the test required silence until the final archivist instruction. Early diagnostic replies are noted but do not automatically zero the primary score when the final package is still usable.
- Tokens-per-second values are now taken from the provided stats.json averages for this run.
- No major score revisions were made from the batch evaluations. The complete stats mainly refine the speed column and confirm the relative ordering.
- For real use on similar multi-note archival tasks, prefer Ornith 1.5 9B or Qwen3.8 27B when fact retention matters. Prefer faster mid-size models only when light editing is acceptable and turn time is constrained.