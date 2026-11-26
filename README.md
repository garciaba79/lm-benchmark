# LM Benchmark

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)

LM Benchmark tests local models by asking them a series of questions across topics and categories. It saves each model's answers, then evaluates, ranks, and scores them. You get a set of small-model results you can read through. They show how different models respond, behave, and perform, and they help you understand their capability and decide which model to use for a task.

## Test Example

Here is an example of a test that tests the local models on a code completion task.  

This test is interesting. It simulates the model's ability to fill in the middle (FIM) while writing code.  
Only certain models have the capability for FIM, but the test is a question and the model should be able to respond reasonably well.  

| Model | t/s | Time | Correctness | Quality |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5 Coder 32B Instruct | 6 | 51s | 85 | 75 |
| Qwen3.6 35B A3B | 43 | 16s | 85 | 70 |
| Qwen3 Coder 30B | 61 | 8s | 80 | 70 |
| Gemma 4 E2B | 193 | 5s | 70 | 65 |
| LFM2.5 2.6B | 253 | 13s | 60 | 65 |
| Nemotron 3 Nano 4B | 225 | 3s | 55 | 60 |
| Qwen2.5 Coder 1.5B Instruct | 297 | 2s | 45 | 50 |
| LFM2.5 230M | 962 | 1s | 10 | 15 |

#### Evaluation Example

The top model with the best score performed the slowest. Qwen2.5 Coder 32B took 51s at 6 t/s, and the evaluation called it the closest to something you could use without a major rewrite.

A few of the smaller models stood out.

Gemma 4 E2B scored 70 for correctness, in the same range as models several times its size, and it finished in 5s at 193 t/s. The evaluation called it fast and reasonably correct. It still added extra error handling the question did not ask for.

LFM2.5 2.6B scored 60 for correctness and 65 for quality. That sits near several 8B to 14B results. It still wrote a full docstring, which this question did not want.

Nemotron 3 Nano 4B scored 55. It was not the most correct model. The evaluation said it came the closest to returning only the function.

Qwen2.5 Coder 1.5B scored 45. The evaluation called it the least broken of the small models, and the best attempt at the user filter. Quite a few larger models skipped that filter.

LFM2.5 230M ran at 962 t/s and finished in 1s. Correctness was 10. The code was syntactically broken.

See the test [question](scenarios/code/fim%201/question1.md)  
See the test [results](results/code/fim%201/results.md)  

## Get Started

See the documentation to [get started](documentation/get-started.md)

## Documentation

| Document | Description |
| --- | --- |
| [Get Started](documentation/get-started.md) | Instructions on how to get started with the benchmark |
| [Evaluation information](documentation/evaluation.md) | Instructions on how to evaluate models |
| [Evaluation instructions](documentation/instructions.md) | Instructions for the cloud model evaluation |
| [Example scenario](documentation/example/examples.md) | An example of a question |
| [Project briefing](documentation/lm-benchmark.md) | The full description for a model that cannot open the repo i.e. chat agent |
| [Short briefing](documentation/summary-app.md) | The short form of the project briefing |
| [Manual evaluation](documentation/workflow.md) | Evaluate the results with a cloud model chat in the browser |
| [Manual evaluation instructions](documentation/instructions-prompt.md) | The prompt to paste if you score a batch yourself |
| [Plugins](documentation/plugin.md) | Information for adding new plugins |
| [Grok CLI](documentation/grok-cli.md) | Evaluate the results with the Grok CLI |
| [Changelog](CHANGE.md) | What changed |
| [AGENTS.md](AGENTS.md) | Notes for a coding agent working in this repo |

## License

Copyright (c) 2026 BillyJoe Garcia  
[garciaba79](https://github.com/garciaba79)  
[MIT](LICENSE)  
