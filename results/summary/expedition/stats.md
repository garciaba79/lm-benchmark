# Stats

Here is the summary results.

Overall time (all models): 1:30 hours

| Model                             | Avg t/s | Total time    | Q1   | Q2           | Q3           | Q4           | Q5           | Q6           | Q7           | Q8           | Q9   | Q10          | Q11          | Q12          |
| --------------------------------- | ------- | ------------- | ---- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ---- | ------------ | ------------ | ------------ |
| LFM2.5 230M                       | 755     | 9 s           | 0 s  | 0 s          | 1 s          | 1 s          | 1 s          | 1 s          | 1 s          | 1 s          | 1 s  | 1 s          | 1 s          | 0 s          |
| LFM2.5 350M                       | 572     | 3 s           | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s  | 0 s          | 0 s          | 0 s          |
| LFM2.5 1.2B Instruct              | 404     | 12 s          | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 2 s          | 3 s  | 3 s          | 2 s          | 1 s          |
| LFM2.5 1.2B Thinking              | 487     | 15 s          | 3 s  | 2 s          | 1 s          | 2 s          | 1 s          | 1 s          | 1 s          | 0 s          | 1 s  | 1 s          | 1 s          | 1 s          |
| Qwen2.5 Coder 1.5B Instruct       | 136     | 5 s           | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s  | 0 s          | 0 s          | 4 s          |
| LFM2.5 2.6B                       | 244     | 1:10 minutes  | 3 s  | 10 s         | 4 s          | 4 s          | 4 s          | 4 s          | 5 s          | 5 s          | 4 s  | 5 s          | 7 s          | 14 s         |
| LFM2.5 VL 3B                      | 181     | 4 s           | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s  | 0 s          | 0 s          | 3 s          |
| Ministral 3 3B Instruct 2512      | 164     | 48 s          | 0 s  | 1 s          | 2 s          | 3 s          | 1 s          | 2 s          | 4 s          | 4 s          | 6 s  | 7 s          | 9 s          | 9 s          |
| Ministral 3 3B Reasoning 2512     | 158     | 47 s          | 0 s  | 2 s          | 4 s          | 4 s          | 1 s          | 2 s          | 2 s          | 4 s          | 7 s  | 7 s          | 7 s          | 6 s          |
| Nemotron 3 Nano 4B                | 190     | 38 s          | 1 s  | 6 s          | 4 s          | 7 s          | 3 s          | 2 s          | 5 s          | 0 s          | 2 s  | 1 s          | 3 s          | 5 s          |
| Qwen3.5 4B                        | 146     | 25:03 minutes | 11 s | 3:34 minutes | 3:24 minutes | 3:24 minutes | 3:28 minutes | 3:24 minutes | 28 s         | 3:04 minutes | 25 s | 2:36 minutes | 23 s         | 42 s         |
| Falcon H1R 7B                     | 91      | 7:02 minutes  | 3 s  | 1:21 minutes | 21 s         | 32 s         | 8 s          | 8 s          | 1:14 minutes | 32 s         | 30 s | 22 s         | 51 s         | 1:00 minutes |
| Qwen2.5 Coder 7B Instruct         | 129     | 11 s          | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 1 s          | 1 s  | 1 s          | 1 s          | 6 s          |
| Mamba Codestral 7B v0.1           | 150     | 29 s          | 1 s  | 3 s          | 3 s          | 3 s          | 2 s          | 2 s          | 2 s          | 2 s          | 2 s  | 2 s          | 2 s          | 5 s          |
| Deepseek Coder 6.7B Instruct      | 29      | 5:21 minutes  | 1 s  | 12 s         | 18 s         | 41 s         | 31 s         | 52 s         | 54 s         | 1:09 minutes | 13 s | 10 s         | 8 s          | 12 s         |
| Granite 4.1 8B                    | 103     | 1:47 minutes  | 1 s  | 5 s          | 5 s          | 6 s          | 4 s          | 7 s          | 8 s          | 9 s          | 15 s | 16 s         | 14 s         | 16 s         |
| LFM2.5 8B A1B                     | 342     | 21 s          | 1 s  | 1 s          | 2 s          | 1 s          | 1 s          | 2 s          | 0 s          | 2 s          | 1 s  | 4 s          | 1 s          | 6 s          |
| Ministral 3 8B Instruct 2512      | 104     | 1:34 minutes  | 0 s  | 5 s          | 9 s          | 7 s          | 2 s          | 5 s          | 6 s          | 8 s          | 9 s  | 11 s         | 15 s         | 15 s         |
| Rnj 1                             | 100     | 6 s           | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 1 s  | 0 s          | 0 s          | 3 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 101     | 2:28 minutes  | 1 s  | 11 s         | 14 s         | 13 s         | 10 s         | 13 s         | 13 s         | 15 s         | 14 s | 19 s         | 16 s         | 9 s          |
| Ornith 1.5 9B                     | 142     | 5:03 minutes  | 1 s  | 9 s          | 2:52 minutes | 9 s          | 8 s          | 4 s          | 5 s          | 7 s          | 19 s | 15 s         | 20 s         | 35 s         |
| Qwen3.5 9B                        | 116     | 6:38 minutes  | 16 s | 41 s         | 39 s         | 40 s         | 29 s         | 22 s         | 58 s         | 37 s         | 24 s | 5 s          | 33 s         | 54 s         |
| Qwen2.5 Coder 14B                 | 7       | 1:59 minutes  | 0 s  | 2 s          | 1 s          | 1 s          | 0 s          | 1 s          | 1 s          | 1 s          | 2 s  | 1 s          | 1 s          | 1:49 minutes |
| Gemma 4 E4B                       | 127     | 43 s          | 0 s  | 3 s          | 6 s          | 3 s          | 1 s          | 2 s          | 2 s          | 4 s          | 6 s  | 6 s          | 5 s          | 5 s          |
| Gemma 4 12B                       | 71      | 1:31 minutes  | 0 s  | 0 s          | 12 s         | 10 s         | 2 s          | 3 s          | 1 s          | 9 s          | 14 s | 15 s         | 14 s         | 11 s         |
| Qwen3 14B                         | 65      | 15 s          | 0 s  | 0 s          | 0 s          | 1 s          | 0 s          | 0 s          | 0 s          | 1 s          | 1 s  | 1 s          | 1 s          | 9 s          |
| Phi 4                             | 71      | 2:11 minutes  | 0 s  | 6 s          | 11 s         | 11 s         | 7 s          | 11 s         | 10 s         | 15 s         | 17 s | 16 s         | 17 s         | 10 s         |
| GPT-OSS 20B                       | 178     | 19 s          | 0 s  | 1 s          | 1 s          | 0 s          | 0 s          | 1 s          | 0 s          | 2 s          | 1 s  | 4 s          | 5 s          | 4 s          |
| Lfm2 24B A2B                      | 90      | 1:00 minutes  | 0 s  | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 9 s          | 11 s | 15 s         | 15 s         | 8 s          |
| LFM2.5 24B A2B                    | 117     | 8:14 minutes  | 18 s | 27 s         | 53 s         | 40 s         | 17 s         | 40 s         | 58 s         | 55 s         | 50 s | 33 s         | 42 s         | 1:02 minutes |
| Qwen3.8 27B                       | 6       | 2:07 minutes  | 1 s  | 1 s          | 1 s          | 2 s          | 1 s          | 1 s          | 1 s          | 3 s          | 3 s  | 2 s          | 2 s          | 1:47 minutes |
| Qwen3 Coder 30B                   | 39      | 5:21 minutes  | 1 s  | 2 s          | 2 s          | 2 s          | 2 s          | 3 s          | 3 s          | 37 s         | 54 s | 1:16 minutes | 1:34 minutes | 43 s         |
| Qwen2.5 Coder 32B Instruct        | 5       | 6:25 minutes  | 2 s  | 4 s          | 7 s          | 10 s         | 5 s          | 8 s          | 8 s          | 25 s         | 43 s | 24 s         | 26 s         | 3:44 minutes |
| Gemma 4 E2B                       | 131     | 8 s           | 2 s  | 0 s          | 1 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s          | 0 s  | 0 s          | 0 s          | 4 s          |
