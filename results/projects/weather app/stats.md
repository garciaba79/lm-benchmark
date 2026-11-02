# Stats

The test results show varying performance levels across different models and versions, with overall speeds generally aligning closely to expected benchmarks. Some models maintained similar outputs despite minor differences in architecture or version updates. Notable differences were observed between high-end and more recent variants.

Overall time (all models): 52:33 minutes

| Model                             | Avg t/s | Total time    | Used RAM | Q1           | Q2           | Q3           | Q4           | Q5           |
| --------------------------------- | ------- | ------------- | -------- | ------------ | ------------ | ------------ | ------------ | ------------ |
| LFM2.5 230M                       | 915     | 6 s           | no       | 1 s          | 1 s          | 2 s          | 2 s          | 1 s          |
| LFM2.5 350M                       | 743     | 6 s           | no       | 2 s          | 1 s          | 1 s          | 1 s          | 1 s          |
| LFM2.5 1.2B Instruct              | 545     | 9 s           | no       | 0 s          | 2 s          | 2 s          | 3 s          | 2 s          |
| LFM2.5 1.2B Thinking              | 551     | 10 s          | no       | 1 s          | 2 s          | 3 s          | 3 s          | 2 s          |
| Qwen2.5 Coder 1.5B Instruct       | 305     | 18 s          | no       | 0 s          | 1 s          | 1 s          | 2 s          | 13 s         |
| Gemma 2 2B Instruct               | 207     | 18 s          | no       | 3 s          | 3 s          | 4 s          | 4 s          | 4 s          |
| LFM2.5 2.6B                       | 278     | 36 s          | no       | 2 s          | 7 s          | 6 s          | 10 s         | 12 s         |
| LFM2.5 VL 3B                      | 274     | 6 s           | no       | 0 s          | 1 s          | 1 s          | 2 s          | 2 s          |
| Microsoft Phi 4 Mini Instruct     | 185     | 11 s          | no       | 1 s          | 2 s          | 3 s          | 2 s          | 2 s          |
| Ministral 3 3B Instruct 2512      | 201     | 30 s          | no       | 4 s          | 6 s          | 6 s          | 7 s          | 7 s          |
| Ministral 3 3B Reasoning 2512     | 191     | 24 s          | no       | 8 s          | 5 s          | 4 s          | 5 s          | 3 s          |
| Nemotron 3 Nano 4B                | 218     | 18 s          | no       | 1 s          | 5 s          | 3 s          | 5 s          | 3 s          |
| Qwen3.5 4B                        | 170     | 59 s          | no       | 5 s          | 14 s         | 12 s         | 16 s         | 13 s         |
| Falcon H1R 7B                     | 100     | 3:01 minutes  | no       | 9 s          | 37 s         | 47 s         | 1:15 minutes | 14 s         |
| Qwen2.5 Coder 7B Instruct         | 140     | 17 s          | no       | 1 s          | 4 s          | 3 s          | 6 s          | 4 s          |
| Mamba Codestral 7B v0.1           | 151     | 34 s          | no       | 19 s         | 3 s          | 4 s          | 3 s          | 4 s          |
| Deepseek Coder 6.7B Instruct      | 112     | 26 s          | no       | 3 s          | 5 s          | 8 s          | 4 s          | 6 s          |
| Granite 4.1 8B                    | 112     | 43 s          | no       | 6 s          | 8 s          | 9 s          | 12 s         | 8 s          |
| LFM2.5 8B A1B                     | 371     | 13 s          | no       | 1 s          | 1 s          | 3 s          | 4 s          | 4 s          |
| Ministral 3 8B Instruct 2512      | 115     | 47 s          | no       | 7 s          | 11 s         | 9 s          | 13 s         | 8 s          |
| Rnj 1                             | 118     | 33 s          | no       | 1 s          | 4 s          | 6 s          | 15 s         | 7 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 102     | 1:26 minutes  | no       | 5 s          | 19 s         | 17 s         | 34 s         | 11 s         |
| Ornith 1.5 9B                     | 116     | 1:37 minutes  | no       | 8 s          | 43 s         | 15 s         | 23 s         | 8 s          |
| Qwen3.5 9B                        | 118     | 1:05 minutes  | no       | 3 s          | 15 s         | 8 s          | 24 s         | 15 s         |
| Gemma 4 12B QAT                   | 83      | 41 s          | no       | 4 s          | 11 s         | 9 s          | 10 s         | 9 s          |
| Qwen Qwen3 14B                    | 9       | 13:35 minutes | yes      | 2:05 minutes | 3:26 minutes | 3:09 minutes | 4:05 minutes | 50 s         |
| Qwen2.5 Coder 14B                 | 72      | 50 s          | no       | 1 s          | 10 s         | 7 s          | 22 s         | 10 s         |
| Phi 4                             | 75      | 40 s          | no       | 8 s          | 6 s          | 6 s          | 10 s         | 10 s         |
| GPT-OSS 20B                       | 119     | 51 s          | no       | 2 s          | 12 s         | 10 s         | 17 s         | 10 s         |
| Lfm2 24B A2B                      | 103     | 1:12 minutes  | yes      | 4 s          | 9 s          | 9 s          | 32 s         | 19 s         |
| LFM2.5 24B A2B                    | 98      | 2:28 minutes  | yes      | 6 s          | 22 s         | 17 s         | 1:14 minutes | 29 s         |
| Qwen2.5 Coder 32B Instruct        | 5       | 17:24 minutes | yes      | 1:34 minutes | 2:31 minutes | 3:13 minutes | 6:29 minutes | 3:37 minutes |
