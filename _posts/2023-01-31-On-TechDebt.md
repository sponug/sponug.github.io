---
layout: post
title: On Tech Debt
---

Notes on Tech Debt: I have found this article [A Taxonomy Of Tech Debt](https://technology.riotgames.com/news/taxonomy-tech-debt) very useful in understanding tech debt

Below are my favourite highlights -
- Considering that all tech debt needs to be fixed at some point , the key decision is what to fix *now* Vs what to fix *eventually*
- It is vital to measure a piece of tech debt to make this decision . 3 possible dimensions to measure tech debt are - *impact , Cost To Fix , and Contagion*
- **Impact**
  - Can be at two levels - customer or engineering 
    - Customer impacts can be missed features , bugs or unexpected behavior 
    - Engineering impacts can slower implementation, workflow issues, random useless shit to remember
- **Cost To Fix** : The second axis has to do with the cost to fix the tech debt. If we decide to fix an issue in our code or data, 
it will require someone’s measurable time to fix. If it’s a deeply rooted assumption that affects every line of code in the game, 
it may take weeks or months of engineering time. If it’s a dumb error in a single function, it may be fixable in a matter of minutes. 
Regardless of the time to implement a fix, though, we also must consider the risk of actually deploying that fix
- **Contagion**
