---
layout: post
title: Neo4j for Beginners (Part 1): Thinking in Graphs with Banking Products
---

This tutorial is for anyone curious about graph databases, even if you have never worked with a database before.
Using simple banking examples — customers and the products they use — we will explore how Neo4j represents data as relationships rather than tables.
By the end of this article, you’ll understand what a graph database is, why it’s useful, and how it forms the foundation for building recommendation system

# Table of contents
1. [Introduction](#introduction)
2. [What Is a Graph Database?](#paragraph1)
    1. [Sub paragraph](#subparagraph1)
3. [Another paragraph](#paragraph2)

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

These connections are not implied or calculated later — they are stored directly in the database

(:Customer) ──USES──▶ (:Product)
     │
     └──OWNS──▶ (:Account) ──IS_LINKED_TO──▶ (:Product)
     
This structure mirrors how banking relationships exist in the real world, making it easy to explore how customers, accounts, and products relate to each other.


### Sub paragraph <a name="subparagraph1"></a>
This is a sub paragraph, formatted in heading 3 style

## Another paragraph <a name="paragraph2"></a>
The second paragraph text

