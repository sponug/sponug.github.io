---
layout: post
title: On Strangler Fig Pattern
---

Understanding the strangler fig pattern . If you are wondering what the tree looks like -

![latency](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/Strangler-Fig.jpg)


# Table of contents
1. [Introduction](#introduction)
2. [Motivating Example: API Migration](#motivate1)
    1. [Technical Benefits](##benefits)
    2. [No Free Lunches](##free)
3. [Another paragraph](#paragraph2)


## This is the introduction <a name="introduction"></a>
Imagine you have an old, wobbly LEGO castle you built years ago. It’s still standing, but pieces fall off every time you try to fix or add to it. Instead of smashing it and starting over (which could leave you with no castle for a while), you start building a new, stronger castle around the old one, piece by piece. At first, the old castle is still there, but as you keep adding new parts, you slowly take away the old bricks and replace them with shiny, new ones. Eventually, the old castle disappears, and you’re left with a much better, sturdier LEGO fortress. That’s basically how the strangler fig pattern works in software. You build a new system around an old one, gradually replacing bits until the old system isn’t needed anymore. It’s like upgrading your castle without knocking it down all at once.

Incrementally migrate a legacy system by gradually replacing specific pieces of functionality with new applications and services. As features from the legacy system are replaced, the new system eventually replaces all of the old system's features, strangling the old system and allowing you to decommission it


## Motivating Example : API Migration <a name="motivate1"></a>
Let's work through a motivating example of using strangler fig pattern to migrate.

Migrating a GET Endpoint
Step 1: Legacy API - GET /users
Your legacy system has a simple GET /users endpoint that fetches a list of all users from a database. This endpoint might be slow or built with outdated technologies, but it's still crucial to your application. You don’t want to shut it down or risk downtime, so you start migrating it to a new version using the strangler fig pattern.

Step 2: New API - GET /users
Now, you create a new GET /users endpoint in your new API stack, perhaps built with faster, more modern technologies like GraphQL, a cloud service, or an optimized database query. This new endpoint is designed to be more efficient, handle more complex queries, and scale better.

Step 3: Set Up a Proxy or API Gateway
You introduce a proxy or API gateway to route requests between the old and new systems. Initially, all requests to GET /users still hit the legacy API, but the proxy has the ability to send a portion of the requests to the new API for testing. Over time, you increase the traffic directed to the new API as confidence in its stability grows.

Step 4: Gradual Traffic Shift
You can use techniques like canary releases or feature flags to slowly send some percentage of traffic (e.g., 10% or 25%) to the new GET /users endpoint. This allows you to test how the new API performs without fully migrating the users yet. Meanwhile, the old GET /users endpoint continues to serve the majority of the traffic, so there’s no disruption to your users.

Step 5: Full Migration
Once you’re confident the new API is stable, you gradually increase the traffic to the new GET /users endpoint. You keep testing it against production traffic, fixing any issues along the way, until eventually, all requests go to the new endpoint and the old API can be decommissioned.

### Technical Benefits <a name="benefits"></a>  
- Zero Downtime: No need for a “big bang” release.
- Incremental Risk Management: Roll back or forward easily.
- Modernization Without Disruption: Business operations continue uninterrupted.
### No Free Lunches <a name="lunch"></a> 

While the strangler fig pattern is a great strategy for migrating APIs with minimal risk, it does come with some downsides and challenges to consider:

1. Increased Complexity in Maintenance
During the migration process, you’ll have both the old and new APIs running in parallel. This can increase the complexity of managing both systems at the same time. You’ll need to ensure that the proxy layer or API gateway handles routing correctly, and debugging can be more challenging when there are two versions of an API working simultaneously.

2. Potential for Inconsistent Behavior
As you gradually migrate endpoints, there’s a risk of having different behavior between the old and new API versions. This can confuse developers or consumers of the API, especially if there are inconsistencies in how errors are handled or how certain features are implemented. It’s crucial to ensure that both versions adhere to similar standards, but that can be harder to maintain over time.

3. Increased Latency and Overhead
Routing traffic through an API gateway adds an extra layer between the client and the server. While this is necessary for switching between the old and new systems, it can add some latency. Additionally, handling versioning and routing logic may lead to slight overhead in processing requests, especially if there are many endpoints to manage.

4. Risk of Feature Gaps or Duplication
If the migration isn’t well-planned, there might be gaps in functionality between the old and new APIs. For example, some features might not be fully migrated, or some edge cases might not have been accounted for in the new version. Additionally, you might end up duplicating work, where both the old and new systems need updates or bug fixes during the migration period.

5. Longer Migration Timeline
The gradual nature of the strangler fig pattern means that migration can take time—often much longer than a big-bang approach. If you have a large API with many endpoints, it can take months or even years to fully replace the old system. This might delay the benefits of the new system or cause friction if business needs demand faster results.

6. Resource Drain
Because you're running two systems in parallel, you need to allocate additional resources—both human and computational—to support both the old and new API during the transition. This can increase costs and require more ongoing attention from your development and operations teams.

7. Testing and Version Compatibility
When migrating incrementally, testing can be more complicated. You’ll need to test both versions of the API, ensure compatibility with consumers, and validate that the proxy layer is routing correctly. This can lead to longer testing cycles, especially when dependencies across different parts of the system aren’t clear.

8. Technical Debt
During migration, the old system is often left in a "zombie" state—still functional but not actively maintained. Over time, this can accumulate technical debt, especially if the legacy system requires bug fixes or updates to work with the new version. You might find yourself spending time patching the old system while also investing in the new one.

Despite these downsides, the strangler fig pattern is a useful, low-risk strategy, especially when you're dealing with complex systems where a full migration would be too risky or disruptive. However, it’s important to weigh these trade-offs and ensure that you have the resources and time to handle them effectively.



## Another paragraph <a name="paragraph2"></a>
The second paragraph text
