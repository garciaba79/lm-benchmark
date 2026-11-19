# Stats

Here is the summary results.

Overall time (all models): 52:55 minutes

| Model                                         | Avg t/s | Total time    | Q1           | Q2           | Q3           | Q4           | Q5           |
| --------------------------------------------- | ------- | ------------- | ------------ | ------------ | ------------ | ------------ | ------------ |
| LFM2.5 230M                                   | 927     | 3 s           | 0 s          | 1 s          | 1 s          | 1 s          | 1 s          |
| LFM2.5 350M                                   | 741     | 5 s           | 2 s          | 1 s          | 1 s          | 1 s          | 1 s          |
| LFM2.5 1.2B Instruct                          | 544     | 8 s           | 0 s          | 1 s          | 2 s          | 3 s          | 2 s          |
| LFM2.5 1.2B Thinking                          | 546     | 10 s          | 0 s          | 2 s          | 2 s          | 3 s          | 2 s          |
| Qwen2.5 Coder 1.5B Instruct                   | 302     | 18 s          | 0 s          | 2 s          | 1 s          | 3 s          | 13 s         |
| LFM2.5 2.6B                                   | 278     | 38 s          | 2 s          | 6 s          | 5 s          | 9 s          | 15 s         |
| LFM2.5 VL 3B                                  | 271     | 8 s           | 0 s          | 2 s          | 2 s          | 2 s          | 2 s          |
| Ministral 3 3B Instruct 2512                  | 196     | 37 s          | 3 s          | 5 s          | 9 s          | 13 s         | 8 s          |
| Ministral 3 3B Reasoning 2512                 | 182     | 31 s          | 8 s          | 5 s          | 4 s          | 9 s          | 4 s          |
| Nemotron 3 Nano 4B                            | 214     | 13 s          | 0 s          | 4 s          | 2 s          | 4 s          | 3 s          |
| Qwen3.5 4B                                    | 165     | 40 s          | 2 s          | 8 s          | 4 s          | 20 s         | 6 s          |
| Falcon H1R 7B                                 | 98      | 2:48 minutes  | 6 s          | 38 s         | 43 s         | 56 s         | 24 s         |
| Qwen2.5 Coder 7B Instruct                     | 136     | 19 s          | 1 s          | 4 s          | 3 s          | 7 s          | 5 s          |
| Mamba Codestral 7B v0.1                       | 147     | 1:40 minutes  | 16 s         | 28 s         | 47 s         | 3 s          | 6 s          |
| Gemma 4 E4B                                   | 137     | 28 s          | 2 s          | 7 s          | 4 s          | 7 s          | 8 s          |
| Deepseek Coder 6.7B Instruct                  | 111     | 27 s          | 2 s          | 4 s          | 8 s          | 6 s          | 8 s          |
| Granite 4.1 8B                                | 110     | 41 s          | 6 s          | 7 s          | 8 s          | 9 s          | 10 s         |
| LFM2.5 8B A1B                                 | 367     | 17 s          | 1 s          | 4 s          | 4 s          | 4 s          | 5 s          |
| Ministral 3 8B Instruct 2512                  | 112     | 52 s          | 7 s          | 12 s         | 12 s         | 9 s          | 12 s         |
| Rnj 1                                         | 117     | 26 s          | 2 s          | 4 s          | 4 s          | 10 s         | 6 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2             | 100     | 1:10 minutes  | 5 s          | 17 s         | 18 s         | 20 s         | 10 s         |
| Ornith 1.5 9B                                 | 115     | 31 s          | 3 s          | 7 s          | 5 s          | 8 s          | 8 s          |
| Qwen3.5 9B                                    | 115     | 51 s          | 2 s          | 13 s         | 9 s          | 17 s         | 9 s          |
| Gemma 4 12B                                   | 73      | 49 s          | 2 s          | 10 s         | 7 s          | 19 s         | 10 s         |
| Qwen2.5 Coder 14B                             | 71      | 46 s          | 1 s          | 7 s          | 11 s         | 17 s         | 10 s         |
| Qwen3 14B                                     | 73      | 1:02 minutes  | 2 s          | 15 s         | 16 s         | 11 s         | 17 s         |
| Phi 4                                         | 75      | 45 s          | 8 s          | 8 s          | 8 s          | 11 s         | 11 s         |
| GPT-OSS 20B                                   | 181     | 36 s          | 1 s          | 8 s          | 8 s          | 13 s         | 7 s          |
| Lfm2 24B A2B                                  | 134     | 39 s          | 3 s          | 6 s          | 5 s          | 17 s         | 8 s          |
| LFM2.5 24B A2B                                | 127     | 1:34 minutes  | 3 s          | 12 s         | 15 s         | 44 s         | 21 s         |
| Qwen3.8 27B                                   | 15      | 7:41 minutes  | 7 s          | 2:05 minutes | 1:15 minutes | 2:47 minutes | 1:27 minutes |
| Qwen3 Coder 30B                               | 47      | 41 s          | 2 s          | 9 s          | 9 s          | 6 s          | 15 s         |
| Qwen2.5 Coder 32B Instruct                    | 5       | 23:31 minutes | 1:13 minutes | 3:14 minutes | 3:24 minutes | 8:51 minutes | 6:49 minutes |
| Gemma 4 E2B                                   | 183     | 15 s          | 0 s          | 5 s          | 4 s          | 1 s          | 5 s          |
| DeepSeek v4 Pro Qwen3.5 9B UNCENSORED Heretic | 120     | 34 s          | 4 s          | 8 s          | 6 s          | 8 s          | 8 s          |
