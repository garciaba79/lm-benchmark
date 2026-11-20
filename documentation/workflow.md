## Local Model Testing Workflow

This document describes the standard process for testing local models in LM Studio. The workflow is designed to be generic so it can be used for code, task, or conversation based evaluations.

### Overview

Each test uses the same prompts and questions for every model. After the conversations are complete, the results are collected and reviewed by a large cloud model that evaluates and ranks performance.

### Steps

 #### Prepare the test 
   - Define the prompt and set of questions that every model will receive.
   - Keep the input identical across all models.
   - If a model consistently fails to follow the questions, revise the questions so the test remains consistent for everyone.

 #### Run the conversations 

   - Load each model in LM Studio.
   - Execute the full conversation using the same prompts and questions.
   - Allow the model to complete every turn before moving to the next model.

 #### Capture performance metrics 

   Record conversation metrics.

   - tokens per second (t/s)
   - number of tokens used (number)
   - time spend to respond (seconds, minutes, hours)
   - context used so far (%)

 #### Export the results 

   - Export the complete turn based conversation for each model as a markdown file.
   - Use a clear filename that includes the model name and date.

 #### Collect the test artifacts 

   - Gather the exported chat files.
   - Include the tokens per second values and any other relevant test information (model names, versions, quantization, etc.).

 #### Evaluate with a cloud model

   - Share the collected files and test information with a large cloud model.
   - Ask the cloud model to review the results, compare the models, and rank their capability and performance on the test.

### Consistency Rules

- Every model receives the same starting prompt and the same set of questions.
- The full conversation is captured for each model.
- Evaluation is always performed by a large cloud model using the exported transcripts.
- The process is repeated for every model in the test so the inputs remain identical.

### Note

This is the manual workflow. The project still keeps it for evaluations you run by hand. The standard path is `python run.py` for the conversations and `python evaluate.py` for the cloud ranking. Script result files are named with the model key (`<model-key>.md`). A manual export can still use a name and a date.