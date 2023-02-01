---
layout: post
title: On Acceptance Criteria
---

Notes on Tech Debt: I have found this article [Patterns of effective acceptance criteria](https://brettsbabble.wordpress.com/2011/03/26/patterns-for-effective-acceptance-criteria/) useful in understanding how best to write good acceptance criteria.

**Why do we write acceptance criteria** :
Acceptance Criteria are a way of capturing the expected behaviour of the system, written in such a way that we can easily test to see if they have been met. So we have a couple of main motivations -
- *Capturing expected behaviour*: Given that the acceptance criteria are (largely) written before development starts; and because they capture expected system behaviour, they should form part of the business sign-off of the story. With this in mind they should be written in such a way that a business person can read and understand them
- *Enable Testing* : The Acceptance Criteria of the story will ultimately be used to determine when the story is done. In order to be complete all the behaviours documented in the criteria must be met so they should be clear enough to explain to a user what steps to take to ensure that the criteria are met and also unambiguous enough that anyone testing them can clearly see if their testing succeeds or fails
- *Improve developer understanding* : Acceptance criteria helps facilitate better developer understanding

**Similarity between automated testing steps & acceptance criteria**
  - Setup / Given tells us the prerequisites (what needs to be setup / done before we start this test?) – this will be the setup phase of automated testing
  - Perform the required action / When tells us the action that needs to happen in order to trigger the outcomes that we are testing for – this will be the action that the test needs to perform
  - Validate the results / Then tells us what to expect when the action is performed – this is the validation step of the automated test
  - Teardown will then clean up any persistent setup to ensure that the test can be run repeatedly without any adverse impacts

**Patterns to write good acceptance criteria**
- *Readable* : “Does this acceptance criteria read well? Is it clearly understandable?” Can the business read and sign-off on it ?
- *Testable* : “Can I easily test the results laid out in the acceptance criteria?”. 2 anti-patters are 
  - use of vague statements
  - use of a non-system outcome ( can i write an assert statement in my automated test ? )
- *Implmentation agnostic* : “Does the acceptance criteria drive the developers down a particular implementation route?” If the acceptance criteria specifies implementation detail then re-write it to remove the implementation and make it agnostic. Do this by focusing on the functionality rather than the form of the outcome
- *Actionable when statement* : “Can I automate the when statement?”. The symptoms for the anti-pattern often contain the real action in the Given statement instead of moving it to the When clause
- *Strong Verb Usage* : Avoid should etc. “Is the language used deterministic?”
- *Keep the criteria specific to the story* : Try to ensure that the When portions of the criteria are specific to the story that is being developed
- *tell a story* - Does the acceptance criteria walk the user through the scenario?
