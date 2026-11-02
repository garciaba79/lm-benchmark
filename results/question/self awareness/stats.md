# Stats

The test results show varying speeds across different models and modelsets, with overall performance generally stable but showing notable differences in speed. Some systems achieve higher throughput, especially in larger variants like LFM2.5 1.2B Instruct or LFM2.5 24B A2B.

Overall time (all models): 8:45 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 1040    | 0 s          | no       | 0 s          |
| LFM2.5 350M                       | 833     | 1 s          | no       | 1 s          |
| LFM2.5 1.2B Instruct              | 575     | 1 s          | no       | 1 s          |
| LFM2.5 1.2B Thinking              | 578     | 2 s          | no       | 2 s          |
| Qwen2.5 Coder 1.5B Instruct       | 337     | 1 s          | no       | 1 s          |
| Gemma 2 2B Instruct               | 233     | 3 s          | no       | 3 s          |
| LFM2.5 2.6B                       | 289     | 6 s          | no       | 6 s          |
| LFM2.5 VL 3B                      | 289     | 2 s          | no       | 2 s          |
| Microsoft Phi 4 Mini Instruct     | 203     | 4 s          | no       | 4 s          |
| Ministral 3 3B Instruct 2512      | 227     | 7 s          | no       | 7 s          |
| Ministral 3 3B Reasoning 2512     | 218     | 7 s          | no       | 7 s          |
| Nemotron 3 Nano 4B                | 225     | 8 s          | no       | 8 s          |
| Qwen3.5 4B                        | 175     | 16 s         | no       | 16 s         |
| Falcon H1R 7B                     | 107     | 3 s          | no       | 3 s          |
| Qwen2.5 Coder 7B Instruct         | 149     | 2 s          | no       | 2 s          |
| Mamba Codestral 7B v0.1           | 150     | 2 s          | no       | 2 s          |
| Deepseek Coder 6.7B Instruct      | 158     | 3 s          | no       | 3 s          |
| Granite 4.1 8B                    | 127     | 4 s          | no       | 4 s          |
| LFM2.5 8B A1B                     | 390     | 4 s          | no       | 4 s          |
| Ministral 3 8B Instruct 2512      | 125     | 14 s         | no       | 14 s         |
| Rnj 1                             | 130     | 3 s          | no       | 3 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 103     | 14 s         | no       | 14 s         |
| Ornith 1.5 9B                     | 113     | 15 s         | no       | 15 s         |
| Qwen3.5 9B                        | 119     | 51 s         | no       | 51 s         |
| Gemma 4 12B QAT                   | 95      | 11 s         | no       | 11 s         |
| Qwen Qwen3 14B                    | 10      | 2:45 minutes | yes      | 2:45 minutes |
| Qwen2.5 Coder 14B                 | 79      | 10 s         | no       | 10 s         |
| Phi 4                             | 82      | 6 s          | no       | 6 s          |
| GPT-OSS 20B                       | 130     | 16 s         | no       | 16 s         |
| Lfm2 24B A2B                      | 115     | 8 s          | no       | 8 s          |
| LFM2.5 24B A2B                    | 111     | 8 s          | yes      | 8 s          |
| Qwen2.5 Coder 32B Instruct        | 6       | 2:07 minutes | yes      | 2:07 minutes |
