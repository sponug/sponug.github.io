---
layout: post
title: On Testing
---

Key question answered in the above article is "what to test and what to avoid"
- General guidelines for testing - unit , integration or end-t0-end testing
  - **Keep it simple** - the intent of the test should be clear in the first glance
  - Each test case should test one aspect of functionality or feature
  - It should be easy to understand what went wrong with a test when you read the test results
  - **Meaningful tests** - Write tests that are meaningful and have a purpose and not for coverage
  - **Dont test implementation details** - Implementation details refer to things that users cant see or use
  - Can lead to false positives ( test cases pass even when code is wrong ) and false negatives ( test cases fail even when code is right)
  - Can be because of refactoring
  - Critical to consider what the users will see and use and design the testing accordngly
  - **Use mocking carefully** - Helps in isloating testing and gives more control over items you would not typically have control
  - At the same time it doesnt give the real experience . use carefully
  - In general avoid mocking end-to-end tests . But sometimes they can be a lifesaver
- **Unit Testing**
- **Integration testing**
- **End to end Testing**
- [Reference](https://web.dev/ta-what-to-test/)
