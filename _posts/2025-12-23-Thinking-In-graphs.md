---
layout: post
title: Neo4j for Beginners (Part 1)- Thinking in Graphs with Banking Products
---

This tutorial is for anyone curious about graph databases, even if you have never worked with a database before.
Using simple banking examples — customers and the products they use — we will explore how Neo4j represents data as relationships rather than tables.
By the end of this article, you’ll understand what a graph database is, why it’s useful, and how it forms the foundation for building recommendation system

# Table of contents
1. [Introduction](#introduction)
2. [What Is a Graph Database?](#paragraph1)
3. [Why Relationships Are First-Class in Neo4j](#paragraph2)

## Introduction <a name="introduction"></a>
Banking systems store a lot of data — customers, accounts, cards, loans, and transactions.But what actually creates value is not the data itself, it’s how these things are connected.
- A customer owns an account.
- An account is linked to a product.
- A customer may use multiple products over time.
When we ask questions like “Which customers use both a savings account and a credit card?” or “What products do customers similar to me usually have?”
we are really asking questions about relationships, not rows of data.

## What Is a Graph Database? <a name="paragraph1"></a>
A graph database represents data as things and the connections between them.

In a graph, the things we care about are called nodes.Nodes represent real-world entities such as customers, accounts, or banking products.
The connections between nodes are called relationships.Relationships describe how two things are connected and always have a clear meaning.

For example, instead of storing a customer and a product separately, a graph explicitly stores the fact that:

a Customer USES a Product
a Customer OWNS an Account
an Account IS_LINKED_TO a Product

These connections are not implied or calculated later — they are stored directly in the database. This structure mirrors how banking relationships exist in the real world, making it easy to explore how customers, accounts, and products relate to each other.

## Why Relationships Are First-Class in Neo4j? <a name="paragraph2"></a>
In many systems, relationships are something you figure out later. In Neo4j, relationships are stored directly as part of the data.
In a graph database like Neo4j, relationships are not just references or IDs hidden inside records. They are explicit, named connections between nodes.

For example, instead of saying:
- “Customer 123 has product code SAV-001”
Neo4j stores the relationship itself:
- Customer USES Product

This might sound like a small difference, but it changes how you think about data.

**Relationships have meaning**
Each relationship in Neo4j:
    - Has a type (for example, USES, OWNS, HAS_ACCOUNT)
    - Has a direction (from customer to product)
    - Can also have properties (such as start date or status)

This means the connection itself carries meaning, not just the data on either side.

In a banking context, this allows us to clearly express ideas like:
    - A customer uses a product
    - A customer owns an account
    - An account is linked to a product
These are real-world relationships, stored exactly as they exist

**Why this matters for understanding data**

Because relationships are stored directly, Neo4j can easily answer questions that involve following connections.

For example:
    - Which products does this customer use?
    - Which other customers use the same products?
    - What products are commonly used together?

Instead of assembling these connections at query time, Neo4j simply walks the graph, moving from one node to the next through relationships.

**A foundation for recommendations**

This is what makes graph databases especially powerful for use cases like recommendations.
If customers are connected to products, and products are connected to other customers, patterns naturally emerge:
    - Customers with similar product usage
    - Products that are often used together
    - Opportunities to recommend relevant products

At this stage, you don’t need algorithms or machine learning. The structure of the graph itself already captures valuable insights.

