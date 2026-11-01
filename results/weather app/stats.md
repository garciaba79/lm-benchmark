# Stats

The test results show varying speeds across different models, with overall performance generally high but showing differences in individual run times. Some devices processed queries faster than others, especially at higher speeds.

Overall time (all models): 40:43 minutes

| Model                             | Avg t/s | Total time    | Q1           | Q2           | Q3           | Q4           |
| --------------------------------- | ------- | ------------- | ------------ | ------------ | ------------ | ------------ |
| LFM2.5 230M                       | 906     | 3 s           | 1 s          | 1 s          | 1 s          | 1 s          |
| LFM2.5 350M                       | 739     | 4 s           | 1 s          | 1 s          | 1 s          | 1 s          |
| LFM2.5 1.2B Instruct              | 528     | 7 s           | 0 s          | 1 s          | 2 s          | 3 s          |
| Qwen2.5 Coder 1.5B Instruct       | 281     | 7 s           | 0 s          | 3 s          | 1 s          | 3 s          |
| LFM2.5 2.6B                       | 252     | 27 s          | 2 s          | 8 s          | 6 s          | 10 s         |
| LFM2.5 1.2B Thinking              | 523     | 8 s           | 1 s          | 2 s          | 2 s          | 3 s          |
| Gemma 2 2B Instruct               | 190     | 14 s          | 3 s          | 3 s          | 4 s          | 4 s          |
| LFM2.5 VL 3B                      | 243     | 8 s           | 0 s          | 3 s          | 3 s          | 3 s          |
| Microsoft Phi 4 Mini Instruct     | 175     | 12 s          | 2 s          | 4 s          | 2 s          | 4 s          |
| Ministral 3 3B Instruct 2512      | 195     | 25 s          | 3 s          | 7 s          | 9 s          | 7 s          |
| Ministral 3 3B Reasoning 2512     | 182     | 23 s          | 8 s          | 5 s          | 3 s          | 7 s          |
| Nemotron 3 Nano 4B                | 206     | 18 s          | 2 s          | 6 s          | 5 s          | 6 s          |
| Falcon H1R 7B                     | 95      | 2:41 minutes  | 7 s          | 35 s         | 44 s         | 1:16 minutes |
| Qwen2.5 Coder 7B Instruct         | 131     | 16 s          | 1 s          | 4 s          | 3 s          | 8 s          |
| Mamba Codestral 7B v0.1           | 141     | 37 s          | 19 s         | 7 s          | 7 s          | 3 s          |
| Deepseek Coder 6.7B Instruct      | 109     | 19 s          | 3 s          | 5 s          | 6 s          | 5 s          |
| LFM2.5 8B A1B                     | 353     | 12 s          | 1 s          | 3 s          | 2 s          | 6 s          |
| Meta Llama 3.1 8B Instruct        | 124     | 12 s          | 1 s          | 4 s          | 3 s          | 4 s          |
| Ministral 3 8B Instruct 2512      | 109     | 1:03 minutes  | 6 s          | 15 s         | 23 s         | 19 s         |
| Qwen3 VL 8B Instruct              | 114     | 43 s          | 1 s          | 13 s         | 16 s         | 14 s         |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 96      | 1:04 minutes  | 6 s          | 19 s         | 17 s         | 23 s         |
| Ornith 1.5 9B                     | 113     | 1:12 minutes  | 6 s          | 24 s         | 18 s         | 24 s         |
| Qwen3.5 9B                        | 112     | 1:08 minutes  | 6 s          | 14 s         | 19 s         | 29 s         |
| Qwen Qwen3 14B                    | 10      | 10:33 minutes | 32 s         | 3:30 minutes | 3:23 minutes | 3:08 minutes |
| Qwen2.5 Coder 14B                 | 66      | 56 s          | 8 s          | 11 s         | 14 s         | 22 s         |
| GPT-OSS 20B                       | 114     | 38 s          | 2 s          | 12 s         | 12 s         | 12 s         |
| Lfm2 24B A2B                      | 107     | 44 s          | 3 s          | 8 s          | 10 s         | 23 s         |
| LFM2.5 24B A2B                    | 97      | 1:20 minutes  | 7 s          | 16 s         | 15 s         | 41 s         |
| Qwen2.5 Coder 32B Instruct        | 5       | 14:29 minutes | 1:49 minutes | 3:04 minutes | 3:24 minutes | 6:12 minutes |
