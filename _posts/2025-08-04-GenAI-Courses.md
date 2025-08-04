---
layout: post
title: Intro To Gen AI
---


# Table of contents
1. [Introduction](#introduction)
2. [Notes](#paragraph1)


   
## Introduction <a name="introduction"></a>
45 minute introduction to Gen AI from Google. [Link](https://www.cloudskillsboost.google/paths/118/course_templates/536)

## Notes from the course <a name="paragraph1"></a>
- **Be concise with prompts**
  - bad : prompt = "What do you think could be a good name for a flower shop that specializes in selling bouquets of dried flowers more than fresh flowers?"
  - good : prompt = "Suggest a name for a flower shop that sells bouquets of dried flowers"
- **Be specific and well-defined**
  - Bad : The prompt below might be a bit too generic (which is certainly OK if you'd like to ask a generic question!)
  - Good:  "Generate a list of ways that makes Earth unique compared to other planets"
-  **Ask for one task at a time**
   - Bad: "What's the best method of boiling water and why is the sky blue?"
   - Good  "What's the best method of boiling water?"
- **Watch out for hallucinations**: Although LLMs have been trained on a large amount of data, they can generate text containing statements not grounded in truth or reality; these responses from the LLM are often referred to as "hallucinations" due to their limited memorization capabilities. Note that simply prompting the LLM to provide a citation isn't a fix to this problem, as there are instances of LLMs providing false or inaccurate citations. Dealing with hallucinations is a fundamental challenge of LLMs and an ongoing research area, so it is important to be cognizant that LLMs may seem to give you confident, correct-sounding statements that are in fact incorrect.
- **How can we attempt to reduce the chances of irrelevant responses and hallucinations**?One way is to provide the LLM with system instructions.
- **Generative tasks lead to higher output variability**
    - The prompt below results in an open-ended response, useful for brainstorming, but response is highly variable.
    - prompt = "I'm a high school student. Recommend me a programming activity to improve my skills."
​- **Classification tasks reduces output variability**
    - The prompt below results in a choice and may be useful if you want the output to be easier to control.
    - prompt = """I'm a high school student. Which of these activities do you suggest and why:
        a) learn Python
        b) learn JavaScript
        c) learn Fortran
    """
- **Improve response quality by including examples**:Another way to improve response quality is to add examples in your prompt. The LLM learns in-context from the examples on how to respond. Typically, one to five examples (shots) are enough to improve the quality of responses. Including too many examples can cause the model to over-fit the data and reduce the quality of responses.Similar to classical model training, the quality and distribution of the examples is very important. Pick examples that are representative of the scenarios that you need the model to learn, and keep the distribution of the examples (e.g. number of examples per class in the case of classification) aligned with your actual distribution.
- **Zero-shot prompt**: Below is an example of zero-shot prompting, where you don't provide any examples to the LLM within the prompt itself.
prompt = """Decide whether a Tweet's sentiment is positive, neutral, or negative.
​Tweet: I loved the new YouTube video you made!
Sentiment:
"""
- **One-shot prompt**
Below is an example of one-shot prompting, where you provide one example to the LLM within the prompt to give some guidance on what type of response you want.
prompt = """Decide whether a Tweet's sentiment is positive, neutral, or negative.
​Tweet: I loved the new YouTube video you made!
Sentiment: positive
​Tweet: That was awful. Super boring 😠
Sentiment:
"""
- **Few-shot prompt**
Below is an example of few-shot prompting, where you provide a few examples to the LLM within the prompt to give some guidance on what type of response you want.
prompt = """Decide whether a Tweet's sentiment is positive, neutral, or negative.
​
Tweet: I loved the new YouTube video you made!
Sentiment: positive
​
Tweet: That was awful. Super boring 😠
Sentiment: negative
​
Tweet: Something surprised me about this video - it was actually original. It was not the same old recycled stuff that I always see. Watch it - you will not regret it.
Sentiment:
"""
​- **Choosing between zero-shot, one-shot, few-shot prompting methods**: Which prompt technique to use will solely depends on your goal. The zero-shot prompts are more open-ended and can give you creative answers, while one-shot and few-shot prompts teach the model how to behave so you can get more predictable answers that are consistent with the examples provided.



    

