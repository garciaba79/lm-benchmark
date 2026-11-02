# Stats

The performance varies across models, with overall speeds generally decreasing as model size increases. Notable differences exist between LFM2.5 and other variants, especially in large models like Granite 4.1 8B and LFM2.5 24B A2B.

Overall time (all models): 25:38 minutes

| Model                             | Avg t/s | Total time    | Used RAM | Q1            |
| --------------------------------- | ------- | ------------- | -------- | ------------- |
| LFM2.5 230M                       | 1032    | 0 s           | no       | 0 s           |
| LFM2.5 350M                       | 827     | 1 s           | no       | 1 s           |
| LFM2.5 1.2B Instruct              | 573     | 2 s           | no       | 2 s           |
| LFM2.5 1.2B Thinking              | 560     | 10 s          | no       | 10 s          |
| Qwen2.5 Coder 1.5B Instruct       | 339     | 1 s           | no       | 1 s           |
| Gemma 2 2B Instruct               | 230     | 4 s           | no       | 4 s           |
| LFM2.5 2.6B                       | 284     | 17 s          | no       | 17 s          |
| LFM2.5 VL 3B                      | 289     | 3 s           | no       | 3 s           |
| Microsoft Phi 4 Mini Instruct     | 209     | 1 s           | no       | 1 s           |
| Ministral 3 3B Instruct 2512      | 230     | 3 s           | no       | 3 s           |
| Ministral 3 3B Reasoning 2512     | 187     | 57 s          | no       | 57 s          |
| Nemotron 3 Nano 4B                | 225     | 12 s          | no       | 12 s          |
| Qwen3.5 4B                        | 166     | 1:37 minutes  | no       | 1:37 minutes  |
| Falcon H1R 7B                     | 103     | 1:05 minutes  | no       | 1:05 minutes  |
| Qwen2.5 Coder 7B Instruct         | 148     | 4 s           | no       | 4 s           |
| Mamba Codestral 7B v0.1           | 150     | 3 s           | no       | 3 s           |
| Deepseek Coder 6.7B Instruct      | 155     | 2 s           | no       | 2 s           |
| Granite 4.1 8B                    | 126     | 5 s           | no       | 5 s           |
| LFM2.5 8B A1B                     | 377     | 9 s           | no       | 9 s           |
| Ministral 3 8B Instruct 2512      | 126     | 5 s           | no       | 5 s           |
| Rnj 1                             | 128     | 3 s           | no       | 3 s           |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 103     | 1:02 minutes  | no       | 1:02 minutes  |
| Ornith 1.5 9B                     | 123     | 2:05 minutes  | no       | 2:05 minutes  |
| Qwen3.5 9B                        | 118     | 1:11 minutes  | no       | 1:11 minutes  |
| Gemma 4 12B QAT                   | 84      | 9 s           | no       | 9 s           |
| Qwen Qwen3 14B                    | 10      | 13:05 minutes | yes      | 13:05 minutes |
| Qwen2.5 Coder 14B                 | 73      | 7 s           | no       | 7 s           |
| Phi 4                             | 75      | 7 s           | no       | 7 s           |
| GPT-OSS 20B                       | 122     | 9 s           | no       | 9 s           |
| Lfm2 24B A2B                      | 109     | 9 s           | yes      | 9 s           |
| LFM2.5 24B A2B                    | 100     | 49 s          | yes      | 49 s          |
| Qwen2.5 Coder 32B Instruct        | 6       | 1:42 minutes  | yes      | 1:42 minutes  |
