---
layout: post
title: On Tech Debt
---

Notes on Tech Debt: I have found this article [A Taxonomy Of Tech Debt](https://technology.riotgames.com/news/taxonomy-tech-debt) very useful in understanding tech debt and various strategies to deal with it 

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
- **Contagion** If this tech debt is allowed to continue to exist, how much will it spread? That spreading can result from other systems interfacing with the afflicted system. If a piece of tech debt is well-contained, the cost to fix it later compared to now is basically identical. You can weigh how much impact it has today when determining when a fix makes sense. If, on the other hand, a piece of tech debt is highly contagious, it will steadily become harder and harder to fix. What’s particularly gross about contagious tech debt is that its impact tends to increase as more and more systems become infected by the technical compromise at its core

**Types Of Tech Debt**

- **Local Debt** Resembles the black box of testing. The local system (spell, network layer, script engine) works pretty reliably. No one needs to keep the debt in mind as they develop around the system. But if anyone opens the lid and looks inside, they’ll be horrified, disgusted, or completely confused by what they see 
  - **Tactics** In general, local debt is defined by a low contagion score. If the impact is higher than the cost to fix, it tends to get fixed by a good citizen before too long. When considering whether to fix local debt, first ask yourself if it’s worth it. If the debt is truly not contagious, it should be safe to leave alone for as long as necessary.  If you do decide to make a fix, it’s usually easy to confirm the fix and regression test, due to the locality of the change
- **Duct Tape Code** this means two conflicting systems are “duct-taped” together at their interface points throughout the codebase.Good example is  usage of C++’s std::string vs. our custom AString class , which has been optimised for memory usage.They are not necessarily find and replace fixes.
  - **Tactics** Fixes during day today work . Or a brute force large-scale refactors are good ways to fix this 
- **Foundational Debt** Foundational debt is when some assumption lies deep in the heart of your system and has been baked into the way the entire thing works. Foundational debt is sometimes hard to recognize for experienced users of a system because it’s seen as “just the way it is.” Example - measurement system used in US
  - **Tactics** Foundational debt tends to index highly on all three axes. The high cost encourages sticking with the janky system, which is often the right call, but the high impact and high contagion mean that fixing egregious foundational debt can have a huge payoff. The most common strategy for fixing foundational debt that I’ve observed at Riot is to stand up the new system alongside the old one. If possible, I recommend then converting the foundational debt to duct tape debt by slowly porting systems over to using the new system with conversion operations available to cross between new and old. This allows you to start reaping the benefits in targeted areas easily while limiting exposure to risk.
- **Data Debt** - Data debt starts with a piece of tech debt from one of the other categories. Perhaps it’s a bug in the scripting system, a less-than-desirable file format for items, or two systems that don’t play very well with each other. But then a ton of content (art, scripts, sounds, etc.) gets built on top of that code deficiency. Before too long, fixing the initial tech debt becomes extremely risky and it becomes painfully hard to tell what you’ll break if you try to fix anything.
  - **Tactics** In general, data debt indexes high on cost to fix since it makes changes hard to evaluate. More worryingly, it’s almost always extraordinarily contagious due to a few properties of data (as opposed to code). First, it’s generally acceptable to create a new piece of data with a copy/paste of an existing piece of data. When fixing data debt, I’ve observed two main approaches. The first I call the “do it right checkbox.” This means making a toggle between the old “broken” behavior and the new “fixed” behavior for data creators. Ideally, you make the fixed version default while you make sure old content uses the broken version. Then, like with Duct Tape debt, you can do a slow and steady replacement to get things onto the new version. This has a permanent cost of adding more and more crap to your editing UI. The second approach is the “just fix the damn thing” approach, like NoopMoney used on the parameter naming bug. This means fixing the bug and then trying to repair all the data that’s meaningfully affected. Several techniques can make this less terrifying. First is doing a lot of greps and regex searching to try to understand the theoretical impact. Second is a bunch of targeted testing. Finally, you can prepare a toggle to enable reverting to the old behavior once the fix ships in case you missed something worse than the bug you’re fixing. It’s worth noting that Determinism helps us a lot with testing for these types of changes by letting us confirm that the server produces the same results before and after a change.

**Summary** When measuring a piece of tech debt, you can use impact (to customers and to developers), fix cost (time and risk), and contagion. I believe most developers regularly consider impact and fix cost, while I’ve rarely encountered discussions of contagion. Contagion can be a developer’s worst enemy as a problem burrows in and becomes harder and harder to dislodge. It is possible, however, to turn contagion into a weapon by making your fix more contagious than the problem.

Working on League, most of the tech debt I’ve seen falls into one of the 4 categories I’ve presented here. Local debt, like a black box of gross. Duct Tape debt, where 2 or more systems are duct-taped together with conversion functions. Foundational debt, when the entire structure is built on some unfortunate assumptions. Data debt, when enormous quantities of data are piled on some other type of debt, making it risky and time-consuming to fix.

**Edit 1** : My friend Ram asked a valid question on reading the original entry , which in retrospect should have been the original entry point to any discussion around tech debt 

I found the treatment [here](https://kellanem.com/notes/towards-an-understanding-of-technical-debt) on point to the question which was "what do we consider as tech debt?" . Notes from the article below -

> All Code Is Liability 
>> Peter Norvig

> Technical debt exists. But it’s relatively rare. When you start arguing with someone about technical debt, you’ll generally encounter a definition like: Technical debt is the choices we made in our code, intentionally, to speed up development today, knowing we’d have to change them later. Hard coding a variable because currently there is no plan to change it is a common example of technical debt. Similarly not modularizing a function

How then do we explain the overwhelming prevalence of technical debt we encounter when we talk to people about code? The term is being abused, or at least dangerously overloaded.

**Tech Debt as an overloaded term**
There are at least *5 distinct things* we mean we say “technical debt”.

- Maintenance work: Necessary ongoing maintenance work a codebase needs but we use the term tech debt as a shorthand.
- Features of the codebase that resist change: Therefore the second common meaning of “technical debt” is the features of the codebase we encounter in our work that make it resist change. Examples of features that can make a codebase resist change include: poor modularization, poor documentation or poor test coverage.
- Operability choices that resist change: Related to the code choices we’ve made that resist change: what are the operability choices we’ve made in the design of our systems that put downward pressure on change? If the site goes down every time you make a change, you stop making changes. If you don’t have metrics you can’t deploy changes confidently. Similarly if your tests are flakey, if extensive coordination is required for a release, if you don’t have staging environments, if you can’t run product and operational experiments, if people don’t have access to the information they need to make decisions, if incentives are misaligned
- Code choices that suck the will to live: We often describe this code with the suck-the-will-to-live quality as messy (spaghetti), unmaintainable, or amateurish. Often what we’re describing under the surface is fear and confusion. We don’t understand the code, and when we don’t understand things, as human, we tend to get scared, tired, and angry. Often we find this pattern in teams who’ve inherited a codebase. The code that was originally written by a small tight knit team with a clear vision of the problem is now being worked on by (often much more senior) separate teams working in some degree of silo. What was a productive lack of indirection to the code becomes a poorly considered lack of abstraction resisting change
- Dependencies that resist upgrading: Finally we use technical debt to describe technical decisions that bind a codebase to a technology that due to the passage of time has become a liability: it has stopped receiving updates, expertise are difficult to find, upgrade paths become convoluted. Often a single dependency pegged to an older technology cascades across your infrastructure holding back important upgrades. Archaic dependencies are often a symptom that we weren’t able to prioritize ongoing investment and maintenance of the codebase (see #1), and is the thing most reasonable to refer to as technical debt.

In summary - And finally you should especially worry if your team believes they’re “fixing” or “paying off” technical debt. All code is technical debt. All code is, to varying degrees, an incorrect bet on what the future will look like. You can address issues that are damaging to productivity, operability and morale, but only way to “fix technical debt” is “rm -rf”.

