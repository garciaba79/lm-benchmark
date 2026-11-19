**Summary**  
This evaluation covers 30 models across seven batches on a multi-turn conversation test with a strict “no code unless asked” constraint. The primary differentiator was **Instruction following**, with secondary emphasis on **Helpfulness** and overall response quality. The top models consistently respected the explicit constraint while delivering thoughtful, accurate answers. Models that provided code early were heavily penalized.

**Top models table**

| Rank | Model                        | Type      | Primary score | t/s | Standout trait                              |
|------|------------------------------|-----------|---------------|-----|---------------------------------------------|
| 1    | qwen3.5-4b                   | instruct  | 93            | 160 | Best overall compliance + quality           |
| 2    | qwen/qwen3.5-9b              | instruct  | 92            | 117 | Excellent compliance and analysis           |
| 3    | qwen/qwen3-14b               | instruct  | 92            | 75  | Outstanding new performer                   |

**Key takeaways**  
- Strict instruction following was the clearest separator; 12 models achieved ≥90 on the primary score.  
- Larger models (9B–32B) generally performed better when they respected the constraint.  
- Two models that provided code early (`qwen/qwen2.5-coder-14b` and `essentialai/rnj-1`) ranked near the bottom despite their size.

**Practical notes from the results**  
The top 12 models form a clear “elite tier” suitable for production use where users give explicit behavioral constraints. The remaining models either violated the core rule or produced significantly weaker responses. In real-world applications, the top models would be the most reliable when strict formatting or behavioral instructions are provided.

**Full results table**

| Model                                   | Instruction following | Helpfulness | t/s | Output quality | Correctness | Task understanding | Notes |
|-----------------------------------------|-----------------------|-------------|-----|----------------|-------------|--------------------|-------|
| qwen3.5-4b                              | 93                    | 88          | 160 | 87             | 89          | 90                 | Best overall |
| qwen/qwen3.5-9b                         | 92                    | 87          | 117 | 86             | 88          | 89                 | Excellent |
| qwen/qwen3-14b                          | 92                    | 87          | 75  | 86             | 88          | 89                 | Outstanding |
| qwen/qwen3.8-27b                        | 92                    | 87          | 15  | 86             | 88          | 89                 | Excellent |
| qwen2.5-coder-32b-instruct              | 92                    | 87          | 6   | 86             | 88          | 89                 | Excellent |
| liquid/lfm2-24b-a2b                     | 91                    | 86          | 133 | 85             | 87          | 88                 | Excellent |
| nvidia_nvidia-nemotron-nano-9b-v2       | 91                    | 86          | 101 | 85             | 87          | 88                 | Very strong |
| lfm2.5-2.6b                             | 91                    | 87          | 271 | 85             | 88          | 89                 | Strong |
| openai/gpt-oss-20b                      | 91                    | 86          | 184 | 85             | 87          | 88                 | Excellent |
| lfm2.5-8b-a1b                           | 90                    | 86          | 358 | 84             | 87          | 88                 | Strong |
| google/gemma-4-12b                      | 90                    | 85          | 76  | 84             | 86          | 87                 | Excellent |
| google/gemma-4-e4b                      | 89                    | 85          | 137 | 84             | 86          | 87                 | Strong |
| google/gemma-4-e2b                      | 89                    | 84          | 183 | 83             | 85          | 86                 | Excellent |
| microsoft/phi-4                         | 89                    | 84          | 76  | 83             | 85          | 86                 | Excellent |
| qwen/qwen3-coder-30b                    | 91                    | 86          | 5   | 85             | 87          | 88                 | Excellent |
| ministral-3-8b-instruct-2512            | 87                    | 83          | 117 | 82             | 84          | 85                 | Solid |
| falcon-h1r-7b                           | 82                    | 78          | 101 | 76             | 79          | 80                 | Compliant |
| qwen2.5-coder-7b-instruct               | 79                    | 76          | 132 | 74             | 77          | 78                 | Good |
| lfm2.5-1.2b-instruct                    | 82                    | 79          | 538 | 78             | 80          | 81                 | Still competitive |
| granite-4.1-8b                          | 78                    | 75          | 112 | 73             | 76          | 77                 | Compliant |
| mamba-codestral-7b-v0.1                 | 71                    | 70          | 147 | 68             | 72          | 73                 | Repetitive |
| ornith-1.5-9b                           | 70                    | 68          | 122 | 67             | 70          | 71                 | Compliant |
| ministral-3-3b-reasoning-2512           | 74                    | 72          | 168 | 70             | 73          | 75                 | Acceptable |
| nvidia/nemotron-3-nano-4b               | 68                    | 67          | 209 | 65             | 68          | 70                 | Compliant |
| deepseek-coder-6.7b-instruct            | 45                    | 52          | 120 | 48             | 50          | 52                 | Provided code early |
| essentialai/rnj-1                       | 38                    | 45          | 119 | 42             | 44          | 46                 | Provided code example |
| lfm2.5-350m                             | 61                    | 65          | 713 | 62             | 64          | 66                 | Code violations |
| lfm2.5-230m                             | 42                    | 48          | 886 | 45             | 47          | 50                 | Frequent violations |
| qwen2.5-coder-1.5b-instruct             | 28                    | 35          | 297 | 30             | 32          | 35                 | Major issues |
| qwen/qwen2.5-coder-14b                  | 35                    | 42          | 73  | 38             | 40          | 42                 | Provided code example |

**Additional notes**  
- Primary score: **Instruction following**  
- Secondary score: **Helpfulness**  
- All 30 models evaluated. The top 12 models form a clear elite tier suitable for production use with strict behavioral constraints.
