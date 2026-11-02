# Stats

The test results show varying speeds across models, with overall performance being moderate to fast depending on the model and task type. Notable differences exist between smaller and larger models, especially for specialized tasks like reasoning or code generation. Overall speed is generally consistent but has noticeable gaps in certain configurations.

Overall time (all models): 2:59 minutes

| Model                             | Avg t/s | Total time | Used RAM | Q1   |
| --------------------------------- | ------- | ---------- | -------- | ---- |
| LFM2.5 230M                       | 839     | 0 s        | no       | 0 s  |
| LFM2.5 350M                       | 323     | 0 s        | no       | 0 s  |
| LFM2.5 1.2B Instruct              | 492     | 0 s        | no       | 0 s  |
| LFM2.5 1.2B Thinking              | 544     | 5 s        | no       | 5 s  |
| Qwen2.5 Coder 1.5B Instruct       | 175     | 0 s        | no       | 0 s  |
| Gemma 2 2B Instruct               | 203     | 0 s        | no       | 0 s  |
| LFM2.5 2.6B                       | 272     | 10 s       | no       | 10 s |
| LFM2.5 VL 3B                      | 242     | 0 s        | no       | 0 s  |
| Microsoft Phi 4 Mini Instruct     | 172     | 0 s        | no       | 0 s  |
| Ministral 3 3B Instruct 2512      | 189     | 0 s        | no       | 0 s  |
| Ministral 3 3B Reasoning 2512     | 196     | 19 s       | no       | 19 s |
| Nemotron 3 Nano 4B                | 214     | 3 s        | no       | 3 s  |
| Qwen3.5 4B                        | 165     | 34 s       | no       | 34 s |
| Falcon H1R 7B                     | 101     | 9 s        | no       | 9 s  |
| Qwen2.5 Coder 7B Instruct         | 131     | 0 s        | no       | 0 s  |
| Mamba Codestral 7B v0.1           | 142     | 1 s        | no       | 1 s  |
| Deepseek Coder 6.7B Instruct      | 5       | 4 s        | no       | 4 s  |
| Granite 4.1 8B                    | 113     | 0 s        | no       | 0 s  |
| LFM2.5 8B A1B                     | 364     | 3 s        | no       | 3 s  |
| Ministral 3 8B Instruct 2512      | 112     | 0 s        | no       | 0 s  |
| Rnj 1                             | 121     | 1 s        | no       | 1 s  |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 99      | 4 s        | no       | 4 s  |
| Ornith 1.5 9B                     | 144     | 3 s        | no       | 3 s  |
| Qwen3.5 9B                        | 113     | 23 s       | no       | 23 s |
| Gemma 4 12B QAT                   | 87      | 0 s        | no       | 0 s  |
| Qwen Qwen3 14B                    | 11      | 26 s       | yes      | 26 s |
| Qwen2.5 Coder 14B                 | 55      | 0 s        | no       | 0 s  |
| Phi 4                             | 73      | 0 s        | no       | 0 s  |
| GPT-OSS 20B                       | 126     | 1 s        | yes      | 1 s  |
| Lfm2 24B A2B                      | 100     | 1 s        | yes      | 1 s  |
| LFM2.5 24B A2B                    | 105     | 28 s       | yes      | 28 s |
| Qwen2.5 Coder 32B Instruct        | 6       | 3 s        | yes      | 3 s  |
