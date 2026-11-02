# Stats

The test results show varying performance levels across different models, with overall speed generally increasing in larger parameter counts. Notable differences exist between smaller and more advanced models like LFM2.5 8B A1B (388 t/s) versus smaller ones such as Falcon H1R 7B (106 t/s).

Overall time (all models): 12:50 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 1028    | 0 s          | no       | 0 s          |
| LFM2.5 350M                       | 833     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Instruct              | 579     | 1 s          | no       | 1 s          |
| LFM2.5 1.2B Thinking              | 564     | 10 s         | no       | 10 s         |
| Qwen2.5 Coder 1.5B Instruct       | 341     | 2 s          | no       | 2 s          |
| Gemma 2 2B Instruct               | 234     | 1 s          | no       | 1 s          |
| LFM2.5 2.6B                       | 286     | 16 s         | no       | 16 s         |
| LFM2.5 VL 3B                      | 290     | 1 s          | no       | 1 s          |
| Microsoft Phi 4 Mini Instruct     | 161     | 1:41 minutes | no       | 1:41 minutes |
| Ministral 3 3B Instruct 2512      | 231     | 3 s          | no       | 3 s          |
| Ministral 3 3B Reasoning 2512     | 215     | 9 s          | no       | 9 s          |
| Nemotron 3 Nano 4B                | 226     | 5 s          | no       | 5 s          |
| Qwen3.5 4B                        | 176     | 18 s         | no       | 18 s         |
| Falcon H1R 7B                     | 106     | 18 s         | no       | 18 s         |
| Qwen2.5 Coder 7B Instruct         | 149     | 3 s          | no       | 3 s          |
| Mamba Codestral 7B v0.1           | 151     | 2 s          | no       | 2 s          |
| Deepseek Coder 6.7B Instruct      | 160     | 2 s          | no       | 2 s          |
| Granite 4.1 8B                    | 127     | 4 s          | no       | 4 s          |
| LFM2.5 8B A1B                     | 388     | 4 s          | no       | 4 s          |
| Ministral 3 8B Instruct 2512      | 127     | 6 s          | no       | 6 s          |
| Rnj 1                             | 129     | 2 s          | no       | 2 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 104     | 23 s         | no       | 23 s         |
| Ornith 1.5 9B                     | 155     | 12 s         | no       | 12 s         |
| Qwen3.5 9B                        | 120     | 41 s         | no       | 41 s         |
| Gemma 4 12B QAT                   | 95      | 6 s          | no       | 6 s          |
| Qwen Qwen3 14B                    | 10      | 4:40 minutes | yes      | 4:40 minutes |
| Qwen2.5 Coder 14B                 | 79      | 8 s          | no       | 8 s          |
| Phi 4                             | 82      | 9 s          | no       | 9 s          |
| GPT-OSS 20B                       | 134     | 7 s          | no       | 7 s          |
| Lfm2 24B A2B                      | 115     | 7 s          | no       | 7 s          |
| LFM2.5 24B A2B                    | 108     | 29 s         | no       | 29 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 2:20 minutes | yes      | 2:20 minutes |
