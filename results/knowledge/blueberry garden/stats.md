# Stats

The test results show varying speeds across models, with overall performance generally lower at higher precision levels. Notable differences exist between smaller and larger language models, especially in the 3B to 8B ranges. Most systems operated within expected speed ranges.

Overall time (all models): 21:16 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           | Q2           | Q3           |
| --------------------------------- | ------- | ------------ | -------- | ------------ | ------------ | ------------ |
| LFM2.5 230M                       | 976     | 2 s          | no       | 1 s          | 1 s          | 1 s          |
| LFM2.5 350M                       | 801     | 2 s          | no       | 0 s          | 1 s          | 1 s          |
| LFM2.5 1.2B Instruct              | 572     | 2 s          | no       | 0 s          | 1 s          | 1 s          |
| LFM2.5 1.2B Thinking              | 577     | 4 s          | no       | 1 s          | 1 s          | 2 s          |
| Qwen2.5 Coder 1.5B Instruct       | 326     | 6 s          | no       | 2 s          | 2 s          | 2 s          |
| Gemma 2 2B Instruct               | 230     | 5 s          | no       | 1 s          | 2 s          | 2 s          |
| LFM2.5 2.6B                       | 282     | 12 s         | no       | 5 s          | 4 s          | 3 s          |
| LFM2.5 VL 3B                      | 286     | 12 s         | no       | 4 s          | 5 s          | 2 s          |
| Microsoft Phi 4 Mini Instruct     | 203     | 5 s          | no       | 1 s          | 1 s          | 2 s          |
| Ministral 3 3B Instruct 2512      | 229     | 9 s          | no       | 3 s          | 3 s          | 3 s          |
| Ministral 3 3B Reasoning 2512     | 215     | 6 s          | no       | 1 s          | 2 s          | 2 s          |
| Nemotron 3 Nano 4B                | 224     | 16 s         | no       | 5 s          | 6 s          | 5 s          |
| Qwen3.5 4B                        | 175     | 40 s         | no       | 15 s         | 11 s         | 14 s         |
| Falcon H1R 7B                     | 102     | 2:04 minutes | no       | 53 s         | 45 s         | 26 s         |
| Qwen2.5 Coder 7B Instruct         | 146     | 9 s          | no       | 3 s          | 2 s          | 4 s          |
| Mamba Codestral 7B v0.1           | 151     | 9 s          | no       | 2 s          | 2 s          | 4 s          |
| Deepseek Coder 6.7B Instruct      | 152     | 8 s          | no       | 1 s          | 3 s          | 4 s          |
| Granite 4.1 8B                    | 125     | 12 s         | no       | 3 s          | 4 s          | 5 s          |
| LFM2.5 8B A1B                     | 385     | 7 s          | no       | 3 s          | 2 s          | 2 s          |
| Ministral 3 8B Instruct 2512      | 125     | 19 s         | no       | 5 s          | 9 s          | 6 s          |
| Rnj 1                             | 128     | 8 s          | no       | 3 s          | 3 s          | 2 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 104     | 28 s         | no       | 10 s         | 7 s          | 10 s         |
| Ornith 1.5 9B                     | 122     | 53 s         | no       | 33 s         | 13 s         | 7 s          |
| Qwen3.5 9B                        | 120     | 1:22 minutes | no       | 38 s         | 27 s         | 17 s         |
| Gemma 4 12B QAT                   | 92      | 24 s         | no       | 6 s          | 9 s          | 9 s          |
| Qwen Qwen3 14B                    | 10      | 6:10 minutes | yes      | 2:20 minutes | 2:05 minutes | 1:46 minutes |
| Qwen2.5 Coder 14B                 | 77      | 19 s         | no       | 5 s          | 6 s          | 7 s          |
| Phi 4                             | 80      | 19 s         | no       | 5 s          | 8 s          | 6 s          |
| GPT-OSS 20B                       | 127     | 24 s         | no       | 11 s         | 7 s          | 6 s          |
| Lfm2 24B A2B                      | 114     | 11 s         | no       | 3 s          | 3 s          | 4 s          |
| LFM2.5 24B A2B                    | 109     | 41 s         | no       | 14 s         | 15 s         | 13 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 4:48 minutes | yes      | 1:09 minutes | 1:39 minutes | 1:59 minutes |
