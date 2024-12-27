---
layout: post
title: On Strangler Fig Pattern
---

Understanding the strangler fig pattern . If you are wondering what the tree looks like -

![latency](https://raw.githubusercontent.com/sponug/sponug.github.io/master/images/Strangler-Fig.jpg)


# Table of contents
1. [Introduction](#introduction)
2. [Motivating Example: API Migration](#motivate1)
       1.[Technical Benefits](##benefits)   
4. [Another paragraph](#paragraph2)

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


## Another paragraph <a name="paragraph2"></a>
The second paragraph text
