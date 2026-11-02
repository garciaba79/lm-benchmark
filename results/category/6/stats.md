# Stats

The performance varied widely across models, with overall speeds ranging from around 75 to over 600 t/s. Some systems showed significant differences in execution speed and instruction throughput. Notably, the LFM2.5 at 1.2B Instruct achieved the highest rates, while others lagged behind by several orders of magnitude.

Overall time (all models): 6:30 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 296     | 0 s          | no       | 0 s          |
| LFM2.5 350M                       | 523     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Instruct              | 505     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Thinking              | 543     | 3 s          | no       | 3 s          |
| Qwen2.5 Coder 1.5B Instruct       | 303     | 0 s          | no       | 0 s          |
| Gemma 2 2B Instruct               | 218     | 0 s          | no       | 0 s          |
| LFM2.5 2.6B                       | 271     | 10 s         | no       | 10 s         |
| LFM2.5 VL 3B                      | 264     | 0 s          | no       | 0 s          |
| Microsoft Phi 4 Mini Instruct     | 191     | 1 s          | no       | 1 s          |
| Ministral 3 3B Instruct 2512      | 208     | 0 s          | no       | 0 s          |
| Ministral 3 3B Reasoning 2512     | 177     | 56 s         | no       | 56 s         |
| Nemotron 3 Nano 4B                | 213     | 2 s          | no       | 2 s          |
| Qwen3.5 4B                        | 165     | 27 s         | no       | 27 s         |
| Falcon H1R 7B                     | 99      | 41 s         | no       | 41 s         |
| Qwen2.5 Coder 7B Instruct         | 136     | 0 s          | no       | 0 s          |
| Mamba Codestral 7B v0.1           | 144     | 3 s          | no       | 3 s          |
| Deepseek Coder 6.7B Instruct      | 136     | 3 s          | no       | 3 s          |
| Granite 4.1 8B                    | 118     | 6 s          | no       | 6 s          |
| LFM2.5 8B A1B                     | 354     | 6 s          | no       | 6 s          |
| Ministral 3 8B Instruct 2512      | 115     | 1 s          | no       | 1 s          |
| Rnj 1                             | 116     | 1 s          | no       | 1 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 96      | 9 s          | no       | 9 s          |
| Ornith 1.5 9B                     | 146     | 20 s         | no       | 20 s         |
| Qwen3.5 9B                        | 112     | 40 s         | no       | 40 s         |
| Gemma 4 12B QAT                   | 86      | 1 s          | no       | 1 s          |
| Qwen Qwen3 14B                    | 11      | 1:19 minutes | yes      | 1:19 minutes |
| Qwen2.5 Coder 14B                 | 72      | 1 s          | no       | 1 s          |
| Phi 4                             | 75      | 4 s          | no       | 4 s          |
| GPT-OSS 20B                       | 123     | 1 s          | no       | 1 s          |
| Lfm2 24B A2B                      | 104     | 2 s          | no       | 2 s          |
| LFM2.5 24B A2B                    | 98      | 54 s         | yes      | 54 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 17 s         | yes      | 17 s         |
