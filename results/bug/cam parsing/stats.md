# Stats

The test results show varying performance across different models and sizes, with overall speed ranging from around 75 to over 950 t/s. Notable differences exist between the smallest models like Ornith 1.5 9B (117 t/s) and larger ones such as LFM2.5 8B A1B (346 t/s).

Overall time (all models): 4:17 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 955     | 1 s          | no       | 1 s          |
| LFM2.5 350M                       | 759     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Instruct              | 520     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Thinking              | 539     | 1 s          | no       | 1 s          |
| Qwen2.5 Coder 1.5B Instruct       | 313     | 1 s          | no       | 1 s          |
| Gemma 2 2B Instruct               | 209     | 1 s          | no       | 1 s          |
| LFM2.5 2.6B                       | 255     | 3 s          | no       | 3 s          |
| LFM2.5 VL 3B                      | 245     | 0 s          | no       | 0 s          |
| Microsoft Phi 4 Mini Instruct     | 181     | 1 s          | no       | 1 s          |
| Ministral 3 3B Instruct 2512      | 208     | 1 s          | no       | 1 s          |
| Ministral 3 3B Reasoning 2512     | 196     | 1 s          | no       | 1 s          |
| Nemotron 3 Nano 4B                | 198     | 1 s          | no       | 1 s          |
| Qwen3.5 4B                        | 159     | 22 s         | no       | 22 s         |
| Falcon H1R 7B                     | 98      | 18 s         | no       | 18 s         |
| Qwen2.5 Coder 7B Instruct         | 133     | 1 s          | no       | 1 s          |
| Mamba Codestral 7B v0.1           | 136     | 2 s          | no       | 2 s          |
| Deepseek Coder 6.7B Instruct      | 143     | 1 s          | no       | 1 s          |
| Granite 4.1 8B                    | 115     | 2 s          | no       | 2 s          |
| LFM2.5 8B A1B                     | 346     | 1 s          | no       | 1 s          |
| Ministral 3 8B Instruct 2512      | 117     | 2 s          | no       | 2 s          |
| Rnj 1                             | 116     | 1 s          | no       | 1 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 94      | 4 s          | no       | 4 s          |
| Ornith 1.5 9B                     | 117     | 24 s         | no       | 24 s         |
| Qwen3.5 9B                        | 109     | 6 s          | no       | 6 s          |
| Gemma 4 12B QAT                   | 88      | 4 s          | no       | 4 s          |
| Qwen Qwen3 14B                    | 10      | 1:10 minutes | yes      | 1:10 minutes |
| Qwen2.5 Coder 14B                 | 73      | 3 s          | no       | 3 s          |
| Phi 4                             | 75      | 4 s          | no       | 4 s          |
| GPT-OSS 20B                       | 107     | 4 s          | yes      | 4 s          |
| Lfm2 24B A2B                      | 100     | 2 s          | yes      | 2 s          |
| LFM2.5 24B A2B                    | 97      | 14 s         | yes      | 14 s         |
| Qwen2.5 Coder 32B Instruct        | 5       | 1:01 minutes | yes      | 1:01 minutes |
