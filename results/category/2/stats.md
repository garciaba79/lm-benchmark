# Stats

The test results show varying speeds across different models and platforms. Overall, performance is strong with most models exceeding the baseline of 50–100 t/s. Notable differences exist between newer or larger architectures, such as LFM2.5 8B A1B (387 t/s) versus older models like Gemm 2 2B Instruct (209 t/s).

Overall time (all models): 6:06 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 562     | 0 s          | no       | 0 s          |
| LFM2.5 350M                       | 711     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Instruct              | 529     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Thinking              | 571     | 3 s          | no       | 3 s          |
| Qwen2.5 Coder 1.5B Instruct       | 274     | 0 s          | no       | 0 s          |
| Gemma 2 2B Instruct               | 209     | 0 s          | no       | 0 s          |
| LFM2.5 2.6B                       | 288     | 4 s          | no       | 4 s          |
| LFM2.5 VL 3B                      | 251     | 0 s          | no       | 0 s          |
| Microsoft Phi 4 Mini Instruct     | 205     | 0 s          | no       | 0 s          |
| Ministral 3 3B Instruct 2512      | 207     | 0 s          | no       | 0 s          |
| Ministral 3 3B Reasoning 2512     | 144     | 3:44 minutes | no       | 3:44 minutes |
| Nemotron 3 Nano 4B                | 223     | 1 s          | no       | 1 s          |
| Qwen3.5 4B                        | 174     | 18 s         | no       | 18 s         |
| Falcon H1R 7B                     | 105     | 17 s         | no       | 17 s         |
| Qwen2.5 Coder 7B Instruct         | 143     | 0 s          | no       | 0 s          |
| Mamba Codestral 7B v0.1           | 150     | 2 s          | no       | 2 s          |
| Deepseek Coder 6.7B Instruct      | 152     | 0 s          | no       | 0 s          |
| Granite 4.1 8B                    | 119     | 0 s          | no       | 0 s          |
| LFM2.5 8B A1B                     | 387     | 1 s          | no       | 1 s          |
| Ministral 3 8B Instruct 2512      | 120     | 0 s          | no       | 0 s          |
| Rnj 1                             | 128     | 1 s          | no       | 1 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 104     | 6 s          | no       | 6 s          |
| Ornith 1.5 9B                     | 133     | 5 s          | no       | 5 s          |
| Qwen3.5 9B                        | 120     | 27 s         | no       | 27 s         |
| Gemma 4 12B QAT                   | 92      | 0 s          | no       | 0 s          |
| Qwen Qwen3 14B                    | 10      | 28 s         | yes      | 28 s         |
| Qwen2.5 Coder 14B                 | 73      | 0 s          | no       | 0 s          |
| Phi 4                             | 78      | 0 s          | no       | 0 s          |
| GPT-OSS 20B                       | 128     | 1 s          | no       | 1 s          |
| Lfm2 24B A2B                      | 107     | 1 s          | yes      | 1 s          |
| LFM2.5 24B A2B                    | 104     | 23 s         | yes      | 23 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 2 s          | yes      | 2 s          |
