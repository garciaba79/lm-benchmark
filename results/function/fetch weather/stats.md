# Stats

The test results show varying performance across different models, with overall speed generally increasing at higher model sizes. Notable differences are seen between smaller and larger variants, especially in the LFM2.5 series.

Overall time (all models): 8:02 minutes

| Model                             | Avg t/s | Total time   | Used RAM | Q1           |
| --------------------------------- | ------- | ------------ | -------- | ------------ |
| LFM2.5 230M                       | 1022    | 0 s          | no       | 0 s          |
| LFM2.5 350M                       | 842     | 0 s          | no       | 0 s          |
| LFM2.5 1.2B Instruct              | 581     | 1 s          | no       | 1 s          |
| LFM2.5 1.2B Thinking              | 570     | 6 s          | no       | 6 s          |
| Qwen2.5 Coder 1.5B Instruct       | 339     | 1 s          | no       | 1 s          |
| Gemma 2 2B Instruct               | 233     | 3 s          | no       | 3 s          |
| LFM2.5 2.6B                       | 287     | 9 s          | no       | 9 s          |
| LFM2.5 VL 3B                      | 289     | 2 s          | no       | 2 s          |
| Microsoft Phi 4 Mini Instruct     | 209     | 1 s          | no       | 1 s          |
| Ministral 3 3B Instruct 2512      | 231     | 2 s          | no       | 2 s          |
| Ministral 3 3B Reasoning 2512     | 215     | 9 s          | no       | 9 s          |
| Nemotron 3 Nano 4B                | 225     | 4 s          | no       | 4 s          |
| Qwen3.5 4B                        | 177     | 4 s          | no       | 4 s          |
| Falcon H1R 7B                     | 105     | 30 s         | no       | 30 s         |
| Qwen2.5 Coder 7B Instruct         | 149     | 3 s          | no       | 3 s          |
| Mamba Codestral 7B v0.1           | 150     | 2 s          | no       | 2 s          |
| Deepseek Coder 6.7B Instruct      | 158     | 4 s          | no       | 4 s          |
| Granite 4.1 8B                    | 127     | 5 s          | no       | 5 s          |
| LFM2.5 8B A1B                     | 390     | 3 s          | no       | 3 s          |
| Ministral 3 8B Instruct 2512      | 127     | 4 s          | no       | 4 s          |
| Rnj 1                             | 129     | 4 s          | no       | 4 s          |
| Nvidia NVIDIA Nemotron Nano 9B v2 | 104     | 22 s         | no       | 22 s         |
| Ornith 1.5 9B                     | 139     | 10 s         | no       | 10 s         |
| Qwen3.5 9B                        | 122     | 6 s          | no       | 6 s          |
| Gemma 4 12B QAT                   | 95      | 9 s          | no       | 9 s          |
| Qwen Qwen3 14B                    | 10      | 2:47 minutes | yes      | 2:47 minutes |
| Qwen2.5 Coder 14B                 | 79      | 8 s          | no       | 8 s          |
| Phi 4                             | 82      | 7 s          | no       | 7 s          |
| GPT-OSS 20B                       | 133     | 7 s          | no       | 7 s          |
| Lfm2 24B A2B                      | 115     | 8 s          | yes      | 8 s          |
| LFM2.5 24B A2B                    | 109     | 27 s         | yes      | 27 s         |
| Qwen2.5 Coder 32B Instruct        | 6       | 1:53 minutes | yes      | 1:53 minutes |
