---
layout: post
title: AI Fluency Framework 
---

I completed the [AI Fluency : Framework and Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) from Anthropic. Here are my notes

# Intro to AI Fluency

* AI can be a trusted partner for creative and innovative problem-solving.
* Aim to be **effective, efficient, ethical, and safe**.
* Three distinct ways we interact with AI:

  * **Automation**: AI does work for humans (e.g., summarising emails).
  * **Augmentation**: you and AI work together.
  * **Agency**: AI works independently on your behalf.
* **Generative AI** creates new content rather than only analysing existing content.
* A simple evaluation lens for LLMs: **Helpful, Honest, Harmless**.

# Weaknesses of Generative AI

* Knowledge cut-off dates.
* Doesn’t verify training data; prone to mistakes.
* **Hallucinations** (misinformation).
* Limited by context-window size.
* Non-deterministic outputs.

# The 4D Fluency Framework

## D1 — Delegation: Human vs AI — who does what?

**Three aspects:**

* **Problem awareness**

  * Clearly define goals and the work required.
  * Specify what “success” looks like.
  * Identify the kind of thinking and work needed.

* **Platform awareness**

  * Working knowledge of capabilities and limitations.
  * Choose models that fit the task.
  * Prioritise what matters most: speed, creativity, depth, or accuracy.

* **Task delegation**

  * What can be usefully automated?
  * Where would augmentation add more value?
  * What should be done by a human alone?
  * What could an agent do on your behalf?


## D2 — Description: Communicating with AI

* Don’t just write prompts—**explain tasks, ask questions, provide context, and guide the interaction**.
* Build a **shared thinking environment**.

**Three aspects:**

* **Product description**

  * Describe the characteristics of the desired output.
  * Be clear about what you want.
  * Include context, format, audience, style, and constraints.
  * Give AI all the information it needs to deliver.

* **Process description**

  * Guide the AI’s thought process; the “how” can matter more than the “what”.
  * Provide training specific to your problem.
  * Specify data, key tasks, and preferred order.

* **Performance description**

  * Define behavioural expectations.
  * Note that AI may behave differently by context.
  * State how you want the AI to behave.


## D3 — Discernment: Evaluate what AI produces, how it produces it, and how it behaves

* Use domain expertise.
* Understand how AI systems work and their typical shortcomings.

**Three aspects:**

* **Product discernment**

  * Factually accurate?
  * Appropriate for the audience and purpose?
  * Coherent and well-structured?
  * Meets requirements?
  * Adds value?

* **Process discernment**

  * Look for logical inconsistencies.
  * Watch for lapses in attention or inappropriate steps.
  * Note when it gets stuck in small details or circular reasoning.

* **Performance discernment**

  * Is the communication style appropriate?
  * Is the information at the right level?
  * Does it respond appropriately to feedback?
  * Is the interaction efficient?

**Feedback and correction**

* Specify the problem.
* Clearly explain what’s wrong.
* Offer concrete suggestions for improvement.
* Revise instructions or examples as needed.


## D4 — Diligence: Taking responsibility for your AI interactions

* Be **rigorous, transparent, and accountable**.
* Consider broader ethical and practical questions.
* Responsibility starts with awareness.

**Three aspects:**

* **Creation diligence**: Which AI systems you choose and how you use them.

  * The AI system(s) you use.
  * How you work with them.
  * The impacts from interaction.

* **Transparency diligence**: Be open and accurate about AI use with stakeholders.

  * Who needs to know.
  * How to communicate it.
  * What level of detail is needed.

* **Deployment diligence**: Informed responsibility for outputs you use.

  * Verify facts.
  * Check for biases.
  * Ensure accuracy.
  * Confirm usage rights.


# Foundational Prompting Techniques

* **Provide context**: what you want, why you want it, and who you are.
* **Offer examples** (n-shot prompting): show what “good” looks like; cover a range of cases or styles.

  * Use step-by-step (chain-of-thought) when helpful.
* **Specify output constraints**: set format, sections, length, and other limits.
* **Break complex tasks into steps**: use step-by-step where it adds clarity.
* **Ask the AI to think first**: e.g., “Before answering, think this through carefully.”
* **Define role, style, or tone**.

**Make it iterative**

* Ask the AI for help with prompting.
* Effective prompting is iterative:
  **Preliminary prompt → AI response → Refine prompt → Final output**.
* Ask for variations.
* Request different formats.
* Check confidence.
* Reset the conversation when needed.

