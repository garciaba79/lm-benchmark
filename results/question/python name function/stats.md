# Stats

The test results show varying performance across models, with overall speed differences evident. Some models perform significantly better than others, especially in the LFM2.5 range. Notable delays were observed at higher model sizes and complexity levels.

Overall time (all models): 3:40 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 990     | 0 s          | no       | 0 s          |
| LFM2.5 350M                       | 754     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Instruct              | 568     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Thinking              | 579     | 2 s          | no       | 2 s          |
| Qwen2.5 Coder 1.5B Instruct       | 333     | 0 s          | no       | 0 s          |
| Gemma 2 2B Instruct               | 231     | 1 s          | no       | 1 s          |
| LFM2.5 2.6B                       | 289     | 3 s          | no       | 3 s          |
| LFM2.5 VL 3B                      | 287     | 0 s          | no       | 0 s          |
| Microsoft Phi 4 Mini Instruct     | 207     | 1 s          | no       | 1 s          |
| Ministral 3 3B Instruct 2512      | 233     | 0 s          | no       | 0 s          |
| Ministral 3 3B Reasoning 2512     | 216     | 1 s          | no       | 1 s          |
| Nemotron 3 Nano 4B                | 226     | 2 s          | no       | 2 s          |
| Qwen3.5 4B                        | 175     | 14 s         | no       | 14 s         |
| Falcon H1R 7B                     | 106     | 15 s         | no       | 15 s         |
| Qwen2.5 Coder 7B Instruct         | 145     | 1 s          | no       | 1 s          |
| Mamba Codestral 7B v0.1           | 150     | 1 s          | no       | 1 s          |
| Deepseek Coder 6.7B Instruct      | 154     | 2 s          | no       | 2 s          |
| Granite 4.1 8B                    | 124     | 1 s          | no       | 1 s          |
| LFM2.5 8B A1B                     | 386     | 1 s          | no       | 1 s          |
| Ministral 3 8B Instruct 2512      | 128     | 1 s          | no       | 1 s          |
| Rnj 1                             | 129     | 2 s          | no       | 2 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 103     | 9 s          | no       | 9 s          |
| Ornith 1.5 9B                     | 146     | 4 s          | no       | 4 s          |
| Qwen3.5 9B                        | 120     | 34 s         | no       | 34 s         |
| Gemma 4 12B QAT                   | 93      | 1 s          | no       | 1 s          |
| Qwen Qwen3 14B                    | 10      | 1:32 minutes | yes      | 1:32 minutes |
| Qwen2.5 Coder 14B                 | 78      | 1 s          | no       | 1 s          |
| Phi 4                             | 81      | 1 s          | no       | 1 s          |
| GPT-OSS 20B                       | 131     | 2 s          | no       | 2 s          |
| Lfm2 24B A2B                      | 115     | 2 s          | yes      | 2 s          |
| LFM2.5 24B A2B                    | 111     | 12 s         | yes      | 12 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 13 s         | yes      | 13 s         |
