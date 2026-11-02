# Stats

The test results show varying processing speeds across different models, with overall speed generally decreasing at higher configurations. Notable differences exist between smaller and larger models, especially in the range of 1.2B to 8B. Overall, performance is consistent but diminishes as model size increases.

Overall time (all models): 20:22 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 993     | 1 s          | no       | 1 s          |
| LFM2.5 350M                       | 799     | 1 s          | no       | 1 s          |
| LFM2.5 1.2B Instruct              | 560     | 2 s          | no       | 2 s          |
| LFM2.5 1.2B Thinking              | 551     | 5 s          | no       | 5 s          |
| Qwen2.5 Coder 1.5B Instruct       | 317     | 1 s          | no       | 1 s          |
| Gemma 2 2B Instruct               | 219     | 4 s          | no       | 4 s          |
| LFM2.5 2.6B                       | 265     | 17 s         | no       | 17 s         |
| LFM2.5 VL 3B                      | 269     | 4 s          | no       | 4 s          |
| Microsoft Phi 4 Mini Instruct     | 190     | 6 s          | no       | 6 s          |
| Ministral 3 3B Instruct 2512      | 216     | 5 s          | no       | 5 s          |
| Ministral 3 3B Reasoning 2512     | 193     | 26 s         | no       | 26 s         |
| Nemotron 3 Nano 4B                | 209     | 11 s         | no       | 11 s         |
| Qwen3.5 4B                        | 161     | 20 s         | no       | 20 s         |
| Falcon H1R 7B                     | 96      | 1:12 minutes | no       | 1:12 minutes |
| Qwen2.5 Coder 7B Instruct         | 138     | 4 s          | no       | 4 s          |
| Mamba Codestral 7B v0.1           | 139     | 8 s          | no       | 8 s          |
| Deepseek Coder 6.7B Instruct      | 143     | 5 s          | no       | 5 s          |
| Granite 4.1 8B                    | 115     | 8 s          | no       | 8 s          |
| LFM2.5 8B A1B                     | 347     | 9 s          | no       | 9 s          |
| Ministral 3 8B Instruct 2512      | 114     | 16 s         | no       | 16 s         |
| Rnj 1                             | 119     | 5 s          | no       | 5 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 95      | 36 s         | no       | 36 s         |
| Ornith 1.5 9B                     | 121     | 1:15 minutes | no       | 1:15 minutes |
| Qwen3.5 9B                        | 110     | 15 s         | no       | 15 s         |
| Gemma 4 12B QAT                   | 86      | 17 s         | no       | 17 s         |
| Qwen Qwen3 14B                    | 10      | 9:56 minutes | yes      | 9:56 minutes |
| Qwen2.5 Coder 14B                 | 72      | 12 s         | no       | 12 s         |
| Phi 4                             | 75      | 11 s         | no       | 11 s         |
| GPT-OSS 20B                       | 123     | 14 s         | no       | 14 s         |
| Lfm2 24B A2B                      | 110     | 13 s         | yes      | 13 s         |
| LFM2.5 24B A2B                    | 103     | 44 s         | yes      | 44 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 2:40 minutes | yes      | 2:40 minutes |
